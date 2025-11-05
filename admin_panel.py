"""
Admin Paneli
Bot yöneticileri için komutlar ve istatistikler
"""

import os
import logging
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import DatabaseManager, User, Subscription, PredictionLog
from sqlalchemy import func

logger = logging.getLogger(__name__)

ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip()]


class AdminPanel:
    """Admin komutları ve işlemleri"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def is_admin(self, user_id: int) -> bool:
        """Kullanıcının admin olup olmadığını kontrol et"""
        return user_id in ADMIN_IDS
    
    async def admin_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Genel bot istatistikleri"""
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text("❌ Bu komutu kullanma yetkiniz yok!")
            return
        
        session = self.db.get_session()
        
        try:
            # Toplam kullanıcılar
            total_users = session.query(User).count()
            
            # Premium kullanıcılar
            now = datetime.utcnow()
            premium_users = session.query(User).filter(
                User.subscription_end > now
            ).count()
            
            # Bugünkü yeni kullanıcılar
            today = datetime.utcnow().date()
            new_users_today = session.query(User).filter(
                func.date(User.created_at) == today
            ).count()
            
            # Toplam tahminler
            total_predictions = session.query(PredictionLog).count()
            
            # Bugünkü tahminler
            predictions_today = session.query(PredictionLog).filter(
                func.date(PredictionLog.created_at) == today
            ).count()
            
            # Toplam gelir
            total_revenue = session.query(
                func.sum(Subscription.price)
            ).scalar() or 0
            
            # Bu ayki gelir
            this_month = datetime.utcnow().replace(day=1)
            monthly_revenue = session.query(
                func.sum(Subscription.price)
            ).filter(
                Subscription.created_at >= this_month
            ).scalar() or 0
            
            stats_message = f"""
📊 **ADMIN PANELİ - İSTATİSTİKLER**

**👥 Kullanıcılar:**
• Toplam: {total_users}
• Premium: {premium_users}
• Bugün Yeni: {new_users_today}
• Ücretsiz: {total_users - premium_users}

**🎯 Tahminler:**
• Toplam: {total_predictions}
• Bugün: {predictions_today}
• Ortalama/Kullanıcı: {total_predictions / total_users if total_users > 0 else 0:.2f}

**💰 Gelir:**
• Toplam: {total_revenue:.2f} TL
• Bu Ay: {monthly_revenue:.2f} TL
• Ortalama/Kullanıcı: {total_revenue / total_users if total_users > 0 else 0:.2f} TL

**📈 Dönüşüm Oranı:**
• {(premium_users / total_users * 100) if total_users > 0 else 0:.2f}% kullanıcı premium

📅 **Tarih:** {datetime.now().strftime('%d.%m.%Y %H:%M')}
            """
            
            keyboard = [
                [InlineKeyboardButton("👥 Kullanıcı Listesi", callback_data="admin_users")],
                [InlineKeyboardButton("💰 Gelir Raporu", callback_data="admin_revenue")],
                [InlineKeyboardButton("📢 Duyuru Gönder", callback_data="admin_broadcast")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                stats_message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
        finally:
            session.close()
    
    async def give_premium(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Kullanıcıya manuel premium ver"""
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text("❌ Bu komutu kullanma yetkiniz yok!")
            return
        
        # Komut formatı: /givepremium <user_id> <daily|weekly|monthly>
        if len(context.args) != 2:
            await update.message.reply_text(
                "❌ Kullanım: /givepremium <user_id> <daily|weekly|monthly>"
            )
            return
        
        try:
            target_user_id = int(context.args[0])
            subscription_type = context.args[1].lower()
            
            if subscription_type not in ['daily', 'weekly', 'monthly']:
                await update.message.reply_text("❌ Geçersiz abonelik tipi!")
                return
            
            session = self.db.get_session()
            
            try:
                target_user = session.query(User).filter_by(
                    telegram_id=target_user_id
                ).first()
                
                if not target_user:
                    await update.message.reply_text("❌ Kullanıcı bulunamadı!")
                    return
                
                # Abonelik ekle
                subscription = self.db.add_subscription(
                    user_id=target_user.id,
                    subscription_type=subscription_type,
                    price=0.0,  # Admin verdiği için ücretsiz
                    payment_id=f"ADMIN_GIFT_{user.id}"
                )
                
                if subscription:
                    await update.message.reply_text(
                        f"✅ Kullanıcı {target_user_id} için {subscription_type} "
                        f"premium başarıyla aktifleştirildi!"
                    )
                else:
                    await update.message.reply_text("❌ Premium eklenemedi!")
                    
            finally:
                session.close()
                
        except ValueError:
            await update.message.reply_text("❌ Geçersiz kullanıcı ID!")
    
    async def broadcast_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Tüm kullanıcılara mesaj gönder"""
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text("❌ Bu komutu kullanma yetkiniz yok!")
            return
        
        # Komut formatı: /broadcast <mesaj>
        if not context.args:
            await update.message.reply_text(
                "❌ Kullanım: /broadcast <mesajınız>"
            )
            return
        
        message = ' '.join(context.args)
        
        session = self.db.get_session()
        
        try:
            users = session.query(User).all()
            
            sent_count = 0
            failed_count = 0
            
            await update.message.reply_text(
                f"📢 {len(users)} kullanıcıya mesaj gönderiliyor..."
            )
            
            for db_user in users:
                try:
                    await context.bot.send_message(
                        chat_id=db_user.telegram_id,
                        text=f"📢 **DUYURU**\n\n{message}",
                        parse_mode='Markdown'
                    )
                    sent_count += 1
                except Exception as e:
                    logger.error(f"Mesaj gönderilemedi {db_user.telegram_id}: {e}")
                    failed_count += 1
            
            await update.message.reply_text(
                f"✅ Gönderim tamamlandı!\n"
                f"Başarılı: {sent_count}\n"
                f"Başarısız: {failed_count}"
            )
            
        finally:
            session.close()
    
    async def list_premium_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Premium kullanıcıları listele"""
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text("❌ Bu komutu kullanma yetkiniz yok!")
            return
        
        session = self.db.get_session()
        
        try:
            now = datetime.utcnow()
            premium_users = session.query(User).filter(
                User.subscription_end > now
            ).order_by(User.subscription_end.desc()).limit(20).all()
            
            if not premium_users:
                await update.message.reply_text("❌ Premium kullanıcı bulunamadı!")
                return
            
            message = "💎 **PREMIUM KULLANICILAR** (İlk 20)\n\n"
            
            for idx, db_user in enumerate(premium_users, 1):
                days_left = (db_user.subscription_end - now).days
                message += f"{idx}. @{db_user.username or 'N/A'} (ID: {db_user.telegram_id})\n"
                message += f"   Kalan: {days_left} gün | Harcama: {db_user.total_spent} TL\n\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        finally:
            session.close()
    
    async def revenue_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gelir raporu"""
        user = update.effective_user
        
        if not self.is_admin(user.id):
            await update.message.reply_text("❌ Bu komutu kullanma yetkiniz yok!")
            return
        
        session = self.db.get_session()
        
        try:
            # Son 7 günün geliri
            days_data = []
            
            for i in range(7):
                day = datetime.utcnow().date() - timedelta(days=i)
                next_day = day + timedelta(days=1)
                
                revenue = session.query(
                    func.sum(Subscription.price)
                ).filter(
                    func.date(Subscription.created_at) == day
                ).scalar() or 0
                
                count = session.query(Subscription).filter(
                    func.date(Subscription.created_at) == day
                ).count()
                
                days_data.append({
                    'date': day.strftime('%d.%m'),
                    'revenue': revenue,
                    'count': count
                })
            
            message = "💰 **GELİR RAPORU** (Son 7 Gün)\n\n"
            
            for data in reversed(days_data):
                message += f"📅 {data['date']}: {data['revenue']:.2f} TL ({data['count']} satış)\n"
            
            total_week = sum(d['revenue'] for d in days_data)
            message += f"\n**Haftalık Toplam:** {total_week:.2f} TL"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        finally:
            session.close()


def setup_admin_handlers(app, db_manager):
    """Admin handler'larını kaydet"""
    from telegram.ext import CommandHandler
    
    admin_panel = AdminPanel(db_manager)
    
    app.add_handler(CommandHandler("adminstats", admin_panel.admin_stats))
    app.add_handler(CommandHandler("givepremium", admin_panel.give_premium))
    app.add_handler(CommandHandler("broadcast", admin_panel.broadcast_message))
    app.add_handler(CommandHandler("premiumlist", admin_panel.list_premium_users))
    app.add_handler(CommandHandler("revenue", admin_panel.revenue_report))
    
    return admin_panel
