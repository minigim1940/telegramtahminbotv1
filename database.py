"""
Veritabanı Modelleri
SQLAlchemy ile kullanıcı, abonelik ve tahmin kayıtları
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, timedelta
import os

Base = declarative_base()


class User(Base):
    """Kullanıcı modeli"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(100))
    first_name = Column(String(100))
    last_name = Column(String(100))
    is_premium = Column(Boolean, default=False)
    subscription_end = Column(DateTime, nullable=True)
    free_predictions_used = Column(Integer, default=0)
    last_free_reset = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    total_spent = Column(Float, default=0.0)
    
    # İlişkiler
    subscriptions = relationship("Subscription", back_populates="user")
    predictions_received = relationship("PredictionLog", back_populates="user")
    
    def is_subscription_active(self):
        """Aboneliğin aktif olup olmadığını kontrol et"""
        if self.subscription_end and self.subscription_end > datetime.utcnow():
            return True
        return False
    
    def can_get_free_prediction(self, limit: int = 2):
        """Ücretsiz tahmin hakkı var mı?"""
        # Her gün sıfırlanır
        if self.last_free_reset.date() < datetime.utcnow().date():
            return True
        return self.free_predictions_used < limit
    
    def use_free_prediction(self):
        """Ücretsiz tahmin hakkını kullan"""
        now = datetime.utcnow()
        if self.last_free_reset.date() < now.date():
            self.free_predictions_used = 1
            self.last_free_reset = now
        else:
            self.free_predictions_used += 1


class Subscription(Base):
    """Abonelik geçmişi"""
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subscription_type = Column(String(20))  # daily, weekly, monthly
    price = Column(Float)
    payment_method = Column(String(50))
    payment_id = Column(String(200))
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # İlişkiler
    user = relationship("User", back_populates="subscriptions")


class PredictionLog(Base):
    """Tahmin kayıtları"""
    __tablename__ = 'prediction_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    fixture_id = Column(Integer)
    match_info = Column(Text)  # JSON string
    prediction = Column(Text)  # Tahmin detayları (JSON)
    confidence = Column(Float)  # Tahmin güven skoru
    match_date = Column(DateTime, nullable=True)  # Maç tarihi
    prediction_made_at = Column(DateTime, default=datetime.utcnow)  # Tahmin yapıldığı zaman
    created_at = Column(DateTime, default=datetime.utcnow)
    result = Column(String(20), nullable=True)  # won, lost, draw (sonuç belli olduğunda)
    match_result = Column(String(50), nullable=True)  # Gerçek maç sonucu (örn: "2-1")
    is_correct = Column(Boolean, nullable=True)  # Tahmin doğru mu?
    
    # İlişkiler
    user = relationship("User", back_populates="predictions_received")


class MatchCache(Base):
    """Maç verilerini cache'leme (API çağrılarını azaltmak için)"""
    __tablename__ = 'match_cache'
    
    id = Column(Integer, primary_key=True)
    fixture_id = Column(Integer, unique=True)
    fixture_data = Column(Text)  # JSON string
    statistics = Column(Text)  # JSON string
    h2h_data = Column(Text)  # JSON string
    predictions = Column(Text)  # JSON string
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    def is_expired(self, hours: int = 1):
        """Cache'in süresi doldu mu?"""
        return datetime.utcnow() > self.last_updated + timedelta(hours=hours)


class AdminLog(Base):
    """Admin işlem logları"""
    __tablename__ = 'admin_logs'
    
    id = Column(Integer, primary_key=True)
    admin_telegram_id = Column(Integer)
    action = Column(String(100))
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


# Veritabanı yönetimi
class DatabaseManager:
    """Veritabanı işlemlerini yöneten sınıf"""
    
    def __init__(self, database_url: str = None):
        if database_url is None:
            database_url = os.getenv('DATABASE_URL', 'sqlite:///football_bot.db')
        
        self.engine = create_engine(database_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def get_session(self):
        """Yeni session oluştur"""
        return self.Session()
    
    def get_or_create_user(self, telegram_id: int, username: str = None, 
                          first_name: str = None, last_name: str = None):
        """Kullanıcı getir veya oluştur"""
        session = self.get_session()
        try:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            
            if not user:
                user = User(
                    telegram_id=telegram_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
                session.add(user)
                session.commit()
                session.refresh(user)
            else:
                # Kullanıcı bilgilerini güncelle
                if username:
                    user.username = username
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name
                session.commit()
                session.refresh(user)
            
            # User nesnesini session'dan ayır
            session.expunge(user)
            return user
        finally:
            session.close()
    
    def add_subscription(self, user_id: int, subscription_type: str, 
                        price: float, payment_id: str = None):
        """Yeni abonelik ekle"""
        session = self.get_session()
        try:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return None
            
            # Abonelik süresini hesapla
            duration_map = {
                'daily': timedelta(days=1),
                'weekly': timedelta(days=7),
                'monthly': timedelta(days=30)
            }
            
            duration = duration_map.get(subscription_type, timedelta(days=1))
            start_date = datetime.utcnow()
            end_date = start_date + duration
            
            # Abonelik oluştur
            subscription = Subscription(
                user_id=user_id,
                subscription_type=subscription_type,
                price=price,
                payment_id=payment_id,
                start_date=start_date,
                end_date=end_date
            )
            
            # Kullanıcıyı güncelle
            user.is_premium = True
            user.subscription_end = end_date
            user.total_spent += price
            
            session.add(subscription)
            session.commit()
            
            return subscription
        finally:
            session.close()
    
    def log_prediction(self, user_id: int, fixture_id: int, match_info: str,
                      prediction: str, confidence: float, match_date: datetime = None):
        """Tahmin kaydı oluştur"""
        session = self.get_session()
        try:
            log = PredictionLog(
                user_id=user_id,
                fixture_id=fixture_id,
                match_info=match_info,
                prediction=prediction,
                confidence=confidence,
                match_date=match_date
            )
            session.add(log)
            session.commit()
            return log
        finally:
            session.close()
    
    def get_cached_prediction(self, fixture_id: int, user_id: int = None):
        """Daha önce yapılmış tahmin varsa getir"""
        session = self.get_session()
        try:
            query = session.query(PredictionLog).filter_by(fixture_id=fixture_id)
            if user_id:
                query = query.filter_by(user_id=user_id)
            
            # En son yapılan tahmini getir
            log = query.order_by(PredictionLog.created_at.desc()).first()
            
            if log:
                # Session'dan ayır
                session.expunge(log)
            return log
        finally:
            session.close()
    
    def update_prediction_result(self, fixture_id: int, match_result: str, is_correct: bool):
        """Maç bittiğinde tahmin sonucunu güncelle"""
        session = self.get_session()
        try:
            predictions = session.query(PredictionLog).filter_by(fixture_id=fixture_id).all()
            for pred in predictions:
                pred.match_result = match_result
                pred.is_correct = is_correct
                pred.result = 'won' if is_correct else 'lost'
            session.commit()
        finally:
            session.close()
    
    def get_predictions_by_date(self, date: datetime):
        """Belirli bir tarihteki tüm tahminleri getir"""
        session = self.get_session()
        try:
            # O günün başı ve sonu
            start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = date.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            predictions = session.query(PredictionLog).filter(
                PredictionLog.match_date >= start_of_day,
                PredictionLog.match_date <= end_of_day
            ).order_by(PredictionLog.match_date).all()
            
            # Session'dan ayır
            for pred in predictions:
                session.expunge(pred)
            
            return predictions
        finally:
            session.close()
    
    def get_prediction_stats(self):
        """Genel tahmin istatistiklerini getir"""
        session = self.get_session()
        try:
            total_predictions = session.query(PredictionLog).filter(
                PredictionLog.is_correct.isnot(None)
            ).count()
            
            correct_predictions = session.query(PredictionLog).filter(
                PredictionLog.is_correct == True
            ).count()
            
            wrong_predictions = session.query(PredictionLog).filter(
                PredictionLog.is_correct == False
            ).count()
            
            success_rate = (correct_predictions / total_predictions * 100) if total_predictions > 0 else 0
            
            return {
                'total': total_predictions,
                'correct': correct_predictions,
                'wrong': wrong_predictions,
                'success_rate': round(success_rate, 1)
            }
        finally:
            session.close()
    
    def get_user_stats(self, telegram_id: int):
        """Kullanıcı istatistiklerini getir"""
        session = self.get_session()
        try:
            user = session.query(User).filter_by(telegram_id=telegram_id).first()
            if not user:
                return None
            
            total_predictions = session.query(PredictionLog).filter_by(user_id=user.id).count()
            
            return {
                'user': user,
                'total_predictions': total_predictions,
                'is_premium': user.is_subscription_active(),
                'subscription_end': user.subscription_end
            }
        finally:
            session.close()
