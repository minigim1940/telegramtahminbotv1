"""
Telegram Bot - Ana Bot Dosyası
Kullanıcı arayüzü ve komut işleme
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pytz
from dateutil import parser as date_parser
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from dotenv import load_dotenv
import json

from api_football import APIFootballService
from prediction_engine import PredictionEngine
from database import DatabaseManager
from payment_handler import PaymentHandler

# Logging ayarları
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Ortam değişkenlerini yükle
load_dotenv()

# Servisler
api_service = APIFootballService(os.getenv('API_FOOTBALL_KEY'))
prediction_engine = PredictionEngine(api_service)
db_manager = DatabaseManager()
payment_handler = PaymentHandler(
    os.getenv('STRIPE_SECRET_KEY'),
    db_manager
)

# Admin kullanıcılar
ADMIN_IDS = [int(x) for x in os.getenv('ADMIN_IDS', '').split(',') if x.strip()]


class FootballPredictionBot:
    """Telegram Futbol Tahmin Botu"""
    
    def __init__(self):
        self.app = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Bot başlangıç komutu"""
        user = update.effective_user
        
        # Kullanıcıyı veritabanına kaydet
        db_user = db_manager.get_or_create_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        welcome_message = f"""
🎯 **Futbol Tahmin Botuna Hoş Geldiniz!** ⚽

Merhaba {user.first_name}! 

🎁 **DEMO MOD AKTİF - Sınırsız Tahmin!** 🎁

Bu bot, gelişmiş AI algoritmaları ve gerçek zamanlı istatistiklerle 
futbol maçları için profesyonel tahminler sunar.

**📊 Özellikler:**
✅ Canlı maç tahminleri
✅ Detaylı istatistiksel analiz
✅ H2H (Kafa Kafaya) karşılaştırma
✅ Form analizi
✅ Over/Under tahminleri
✅ BTTS (İki takım da gol atar mı?) tahmini

**🎁 Test Sürümü:**
💎 Sınırsız tahmin - Ücretsiz!
💎 Tüm premium özellikler aktif!
� Ödeme sistemi kapalı (test için)

**📱 Komutlar:**
/tahmin - Maç tahmini al
/bugun - Bugünün maçları
/premium - Premium paketler
/istatistik - İstatistikleriniz
/yardim - Yardım menüsü

Haydi başlayalım! ⚽🎯
        """
        
        keyboard = [
            [InlineKeyboardButton("⚽ Tahmin Al", callback_data="get_prediction")],
            [InlineKeyboardButton("📅 Bugünün Maçları", callback_data="today_matches")],
            [InlineKeyboardButton("� Dünün Sonuçları", callback_data="yesterday_matches")],
            [InlineKeyboardButton("�💎 Premium Ol", callback_data="premium_info")],
            [InlineKeyboardButton("� İstatistiklerim", callback_data="my_stats")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Yardım komutu"""
        help_text = """
📖 **Yardım Menüsü**

**Temel Komutlar:**
/start - Botu başlat
/tahmin - Maç tahmini al
/bugun - Bugünün maçları
/premium - Premium paketleri görüntüle
/istatistik - Kişisel istatistikleriniz
/yardim - Bu yardım menüsü

**Tahmin Nasıl Alınır?**
1. /tahmin komutunu kullanın
2. Listeden bir maç seçin
3. Detaylı analiz ve tahmin gelsin!

**Premium Nasıl Olunur?**
1. /premium komutunu kullanın
2. Size uygun paketi seçin
3. Ödeme yapın
4. Sınırsız tahmin keyfini çıkarın!

**Sorularınız için:** @YourSupportUsername
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def today_matches(self, update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 0):
        """Bugünün maçlarını göster (sayfalama ile)"""
        query = update.callback_query
        if query:
            await query.answer()
            message = query.message
            is_callback = True
        else:
            message = update.message
            is_callback = False
        
        # Yükleniyor mesajı
        if is_callback:
            await query.edit_message_text("📊 Bugünün maçları yükleniyor...\n⏳ API'den gerçek veriler çekiliyor...")
        else:
            loading_msg = await message.reply_text("📊 Bugünün maçları yükleniyor...\n⏳ API'den gerçek veriler çekiliyor...")
        
        matches = api_service.get_today_matches()
        
        if not matches:
            error_text = (
                "❌ Bugün için maç bulunamadı.\n\n"
                "� Muhtemel sebepler:\n"
                "• Bugün maç yok olabilir\n"
                "• API hatası olabilir\n"
                "• Farklı saat dilimi olabilir\n\n"
                "�🔙 Ana menüye dönmek için butona tıklayın."
            )
            keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if is_callback:
                await query.edit_message_text(error_text, reply_markup=reply_markup)
            else:
                await loading_msg.edit_text(error_text, reply_markup=reply_markup)
            return
        
        # Liglere göre grupla
        leagues = {}
        for match in matches:
            league_name = match['league']['name']
            country = match['league']['country']
            league_key = f"{country} - {league_name}"
            
            if league_key not in leagues:
                leagues[league_key] = []
            leagues[league_key].append(match)
        
        # En popüler ligleri öne çıkar
        priority_leagues = [
            'England - Premier League',
            'Spain - La Liga',
            'Germany - Bundesliga', 
            'Italy - Serie A',
            'France - Ligue 1',
            'Turkey - Super Lig',
            'World - UEFA Champions League',
            'Europe - UEFA Europa League'
        ]
        
        # Ligleri sırala: önce popüler ligler, sonra diğerleri
        sorted_leagues = []
        for priority in priority_leagues:
            if priority in leagues:
                sorted_leagues.append((priority, leagues[priority]))
        
        # Diğer ligleri ekle
        for league_key, league_matches in leagues.items():
            if league_key not in priority_leagues:
                sorted_leagues.append((league_key, league_matches))
        
        # Tüm maçları tek listede topla ve saate göre sırala
        all_matches = []
        for league_key, league_matches in sorted_leagues:
            for match in league_matches:
                match['_league_key'] = league_key
                try:
                    match_time = datetime.fromisoformat(match['fixture']['date'].replace('Z', '+00:00'))
                    match['_sort_time'] = match_time + timedelta(hours=3)  # Türkiye saati
                except:
                    match['_sort_time'] = datetime.now()
                all_matches.append(match)
        
        all_matches.sort(key=lambda x: x['_sort_time'])
        
        # Sayfalama
        MATCHES_PER_PAGE = 15
        total_matches = len(all_matches)
        total_pages = (total_matches + MATCHES_PER_PAGE - 1) // MATCHES_PER_PAGE
        
        if page < 0:
            page = 0
        if page >= total_pages:
            page = max(0, total_pages - 1)
        
        start_idx = page * MATCHES_PER_PAGE
        end_idx = min(start_idx + MATCHES_PER_PAGE, total_matches)
        page_matches = all_matches[start_idx:end_idx]
        
        response = f"📅 **BUGÜNÜN MAÇLARI**\n"
        response += f"📆 {datetime.now().strftime('%d.%m.%Y')} | Toplam: {total_matches} maç\n"
        response += f"📄 Sayfa: {page + 1}/{total_pages} (Maç {start_idx + 1}-{end_idx})\n"
        response += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Butonlar için keyboard
        keyboard = []
        current_league = None
        
        for match in page_matches:
            league_key = match['_league_key']
            
            # Yeni lig başlığı
            if league_key != current_league:
                response += f"\n🏆 **{league_key}**\n"
                current_league = league_key
            
            # Maç bilgileri
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            
            # Saat formatını düzenle (UTC'den Türkiye saatine)
            try:
                match_time = match['_sort_time']
                time_str = match_time.strftime('%H:%M')
            except:
                time_str = "??:??"
            
            status = match['fixture']['status']['short']
            fixture_id = match['fixture']['id']
            
            # Durum emojisi
            if status == 'NS':  # Not Started
                status_emoji = "⏰"
            elif status in ['1H', '2H', 'HT']:  # Live
                status_emoji = "🔴"
                home_score = match['goals']['home'] or 0
                away_score = match['goals']['away'] or 0
                time_str = f"{home_score}-{away_score}"
            elif status == 'FT':  # Finished
                status_emoji = "✅"
                home_score = match['goals']['home'] or 0
                away_score = match['goals']['away'] or 0
                time_str = f"{home_score}-{away_score}"
            elif status == 'PST':  # Postponed
                status_emoji = "⏸️"
                time_str = "Ertelendi"
            else:
                status_emoji = "⚽"
            
            # Maç bilgisi ve tahmin kodu
            response += f"{status_emoji} **{time_str}** - {home} vs {away}\n"
            response += f"/tahmin{fixture_id}\n\n"
        
        # Sayfalama butonları
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Önceki", callback_data=f"matches_page_{page-1}"))
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("Sonraki ➡️", callback_data=f"matches_page_{page+1}"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        # Alt kısım butonları
        keyboard.append([InlineKeyboardButton("🎯 En İyi Tahminler", callback_data="top_predictions")])
        keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if is_callback:
            await query.edit_message_text(
                response,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await loading_msg.edit_text(
                response,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    async def yesterday_matches(self, update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 0):
        """Dünün maçlarını tahmin sonuçları ile göster"""
        query = update.callback_query
        if query:
            await query.answer()
            message = query.message
            is_callback = True
        else:
            message = update.message
            is_callback = False
        
        # Yükleniyor mesajı
        if is_callback:
            await query.edit_message_text("📊 Dünün maçları yükleniyor...\n⏳ Tahmin sonuçları kontrol ediliyor...")
        else:
            loading_msg = await message.reply_text("📊 Dünün maçları yükleniyor...\n⏳ Tahmin sonuçları kontrol ediliyor...")
        
        # Dünün maçlarını al
        try:
            matches = api_service.get_yesterday_matches()
            logger.info(f"API'den {len(matches) if matches else 0} maç alındı")
        except Exception as e:
            logger.error(f"API hatası: {e}")
            matches = []
        
        if not matches:
            error_text = (
                "❌ Dün için maç bulunamadı.\n\n"
                "🔙 Ana menüye dönmek için butona tıklayın."
            )
            keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if is_callback:
                await query.edit_message_text(error_text, reply_markup=reply_markup)
            else:
                await loading_msg.edit_text(error_text, reply_markup=reply_markup)
            return
        
        # Sadece bitmiş maçları göster
        finished_matches = [m for m in matches if m['fixture']['status']['short'] == 'FT']
        logger.info(f"Bitmiş maç sayısı: {len(finished_matches)}")
        
        if not finished_matches:
            error_text = (
                "ℹ️ Dün için henüz tamamlanmış maç yok.\n\n"
                "🔙 Ana menüye dönmek için butona tıklayın."
            )
            keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if is_callback:
                await query.edit_message_text(error_text, reply_markup=reply_markup)
            else:
                await loading_msg.edit_text(error_text, reply_markup=reply_markup)
            return
        
        # Her maç için tahmin kontrolü yap
        match_predictions = []
        logger.info(f"Tahmin kontrolü başlıyor, {len(finished_matches)} maç için...")
        
        for match in finished_matches:
            fixture_id = match['fixture']['id']
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            
            logger.info(f"Kontrol ediliyor: {home} vs {away} (ID: {fixture_id})")
            
            # Bu maç için tahmin var mı?
            cached_pred = db_manager.get_cached_prediction(fixture_id=fixture_id)
            
            if cached_pred:
                logger.info(f"✅ Tahmin bulundu! Confidence: {cached_pred.confidence}")
                # Tahmin varsa sonucu kontrol et
                home_score = match['goals']['home']
                away_score = match['goals']['away']
                actual_result = f"{home_score}-{away_score}"
                
                # Tahmin parse et
                try:
                    prediction_data = json.loads(cached_pred.prediction)
                    
                    # Tahmin result'ı doğru yerden al
                    if 'prediction' in prediction_data and 'result' in prediction_data['prediction']:
                        # Yeni format: prediction.result
                        predicted_text = prediction_data['prediction']['result']
                    elif 'result' in prediction_data:
                        # Eski format: direkt result
                        predicted_text = prediction_data['result']
                    else:
                        logger.error(f"Tahmin formatı tanınmıyor: {prediction_data.keys()}")
                        continue
                    
                    # Tahmin metnini result tipine çevir
                    # "1 (Ev Sahibi Kazanır)" -> 'home_win'
                    if '1' in predicted_text or 'Ev Sahibi' in predicted_text or 'home' in predicted_text.lower():
                        predicted_result = 'home_win'
                    elif '2' in predicted_text or 'Deplasman' in predicted_text or 'away' in predicted_text.lower():
                        predicted_result = 'away_win'
                    elif 'X' in predicted_text or 'Beraberlik' in predicted_text or 'draw' in predicted_text.lower():
                        predicted_result = 'draw'
                    else:
                        logger.error(f"Tahmin metni parse edilemedi: {predicted_text}")
                        continue
                    
                    # Gerçek sonucu belirle
                    if home_score > away_score:
                        actual_winner = 'home_win'
                    elif away_score > home_score:
                        actual_winner = 'away_win'
                    else:
                        actual_winner = 'draw'
                    
                    is_correct = (predicted_result == actual_winner)
                    
                    logger.info(f"📊 {home} vs {away}: Tahmin={predicted_result}, Gerçek={actual_winner}, Doğru={is_correct}")
                    
                    # Veritabanını güncelle
                    if cached_pred.is_correct is None:
                        db_manager.update_prediction_result(fixture_id, actual_result, is_correct)
                    
                    match_predictions.append({
                        'match': match,
                        'prediction': prediction_data,
                        'is_correct': is_correct,
                        'actual_result': actual_result,
                        'confidence': cached_pred.confidence
                    })
                except Exception as e:
                    logger.error(f"Tahmin parse hatası ({home} vs {away}): {e}")
            else:
                logger.info(f"❌ Tahmin bulunamadı: {home} vs {away}")
        
        logger.info(f"Toplam {len(match_predictions)} tahminli maç bulundu")
        
        # Eğer tahminli maç yoksa bilgi ver
        if not match_predictions:
            error_text = (
                "ℹ️ Dün için tahmin yapılmış maç bulunamadı.\n\n"
                f"📊 **TOPLAM BİTEN MAÇ:** {len(finished_matches)}\n"
                "💡 Bu maçlar için tahmin yapılmamış.\n\n"
                "🔹 Tahminli maçları görmek için bugünün maçlarından tahmin alın!\n\n"
                "🔙 Ana menüye dönmek için butona tıklayın."
            )
            keyboard = [[InlineKeyboardButton("📅 Bugünün Maçları", callback_data="today_matches")],
                       [InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if is_callback:
                await query.edit_message_text(error_text, reply_markup=reply_markup)
            else:
                await loading_msg.edit_text(error_text, reply_markup=reply_markup)
            return
        
        # İstatistikler
        total_with_prediction = len(match_predictions)
        correct_count = sum(1 for mp in match_predictions if mp['is_correct'])
        wrong_count = total_with_prediction - correct_count
        success_rate = (correct_count / total_with_prediction * 100) if total_with_prediction > 0 else 0
        
        # Sayfalama
        MATCHES_PER_PAGE = 10
        total_matches = len(match_predictions)
        total_pages = max(1, (total_matches + MATCHES_PER_PAGE - 1) // MATCHES_PER_PAGE)
        
        if page < 0:
            page = 0
        if page >= total_pages:
            page = max(0, total_pages - 1)
        
        start_idx = page * MATCHES_PER_PAGE
        end_idx = min(start_idx + MATCHES_PER_PAGE, total_matches)
        page_matches = match_predictions[start_idx:end_idx]
        
        # Başlık
        turkey_tz = pytz.timezone('Europe/Istanbul')
        yesterday = (datetime.now(turkey_tz) - timedelta(days=1)).strftime('%d.%m.%Y')
        
        response = f"📅 **DÜN YAPILAN TAHMİNLER**\n"
        response += f"📆 {yesterday} | Tahminli Maç: {total_with_prediction}\n\n"
        
        if total_with_prediction > 0:
            response += f"**📊 BAŞARI İSTATİSTİKLERİ:**\n"
            response += f"✅ Doğru: {correct_count}\n"
            response += f"❌ Yanlış: {wrong_count}\n"
            response += f"📈 Başarı Oranı: **{success_rate:.1f}%**\n"
            response += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        
        if total_matches > 0:
            response += f"📄 Sayfa: {page + 1}/{total_pages}\n\n"
        
        # Maçları listele
        for mp in page_matches:
            match = mp['match']
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            score = mp['actual_result']
            
            # Tahmin emoji
            if mp['is_correct']:
                status_emoji = "✅ DOĞRU"
            else:
                status_emoji = "🔴 YANLIŞ"
            
            # Tahmin metnini al - prediction içinde result var
            pred_data = mp['prediction']
            if 'prediction' in pred_data and 'result' in pred_data['prediction']:
                # Yeni format
                predicted_text = pred_data['prediction']['result']
            elif 'result' in pred_data:
                # Eski format
                predicted_text = pred_data['result']
            else:
                predicted_text = 'Bilinmiyor'
            
            # Tahmin için emoji ekle
            if '1' in predicted_text or 'Ev Sahibi' in predicted_text:
                pred_text = f"🏠 {home} Kazanır"
            elif '2' in predicted_text or 'Deplasman' in predicted_text:
                pred_text = f"✈️ {away} Kazanır"
            elif 'X' in predicted_text or 'Beraberlik' in predicted_text:
                pred_text = "⚖️ Beraberlik"
            else:
                pred_text = predicted_text
            
            response += f"{status_emoji}\n"
            response += f"**{home} {score} {away}**\n"
            response += f"📊 Tahmin: {pred_text}\n"
            response += f"💯 Güven: {mp['confidence']:.0f}%\n"
            response += f"🏆 Lig: {match['league']['name']}\n"
            response += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        
        # Sayfalama butonları
        keyboard = []
        nav_buttons = []
        
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("◀️ Önceki", callback_data=f"yesterday_page_{page-1}"))
        
        if page < total_pages - 1:
            nav_buttons.append(InlineKeyboardButton("▶️ Sonraki", callback_data=f"yesterday_page_{page+1}"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        # Alt butonlar
        keyboard.append([InlineKeyboardButton("📅 Bugünün Maçları", callback_data="today_matches")])
        keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if is_callback:
            await query.edit_message_text(
                response,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await loading_msg.edit_text(
                response,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    async def get_prediction(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Tahmin al"""
        user = update.effective_user
        
        # Kullanıcı kontrolü
        db_user = db_manager.get_or_create_user(
            telegram_id=user.id,
            username=user.username
        )
        
        # Premium kontrolü
        is_premium = db_user.is_subscription_active()
        can_use_free = db_user.can_get_free_prediction()
        
        if not is_premium and not can_use_free:
            await self._show_premium_required(update)
            return
        
        # Maç listesini göster
        await self.today_matches(update, context)
    
    async def specific_prediction(self, update: Update, context: ContextTypes.DEFAULT_TYPE, is_from_button: bool = False):
        """Belirli bir maç için tahmin"""
        loading_msg = None
        try:
            # Fixture ID'yi al
            if is_from_button:
                # Butondan geliyorsa context.args'dan al
                fixture_id = int(context.args[0])
                query = update.callback_query
                await query.answer()
                user = update.effective_user
                loading_msg = await query.edit_message_text("🔄 Analiz yapılıyor, lütfen bekleyin...")
            else:
                # Komuttan geliyorsa mesajdan al
                command = update.message.text
                # /tahmin1479575 veya /tahmin_1479575 formatını destekle
                if '_' in command:
                    fixture_id = int(command.split('_')[1])
                else:
                    fixture_id = int(command.replace('/tahmin', ''))
                user = update.effective_user
                loading_msg = await update.message.reply_text("🔄 Analiz yapılıyor, lütfen bekleyin...")
            
            logger.info(f"Tahmin isteği: fixture_id={fixture_id}, user={user.id}")
            
            db_user = db_manager.get_or_create_user(telegram_id=user.id)
            
            # ÖNCE CACHE'E BAK - Daha önce yapılmış tahmin var mı?
            try:
                cached_prediction = db_manager.get_cached_prediction(fixture_id=fixture_id)
            except Exception as e:
                logger.error(f"Cache okuma hatası: {e}")
                cached_prediction = None
            
            if cached_prediction:
                # Cache'den tahmin var - yeniden analiz yapma!
                logger.info(f"✅ Cache'den tahmin alındı: fixture_id={fixture_id}")
                
                try:
                    # JSON'dan parse et
                    analysis_data = {
                        'fixture_id': fixture_id,  # Bahis oranları için gerekli
                        'match_info': json.loads(cached_prediction.match_info),
                        'prediction': json.loads(cached_prediction.prediction),
                        'confidence': cached_prediction.confidence,
                        'match_date': cached_prediction.match_date,
                        'is_correct': cached_prediction.is_correct,
                        'match_result': cached_prediction.match_result
                    }
                    
                    # Maç sonucunu kontrol et (eğer maç bittiyse)
                    try:
                        fixture_details = api_service.get_fixture_details(fixture_id)
                        if fixture_details and fixture_details['fixture']['status']['short'] == 'FT':
                            # Maç bitti - sonucu kontrol et
                            home_score = fixture_details['goals']['home']
                            away_score = fixture_details['goals']['away']
                            actual_result = f"{home_score}-{away_score}"
                            
                            # Tahmin parse et - DOĞRU YER
                            pred_data = analysis_data['prediction']
                            if 'prediction' in pred_data and 'result' in pred_data['prediction']:
                                predicted_text = pred_data['prediction']['result']
                            elif 'result' in pred_data:
                                predicted_text = pred_data['result']
                            else:
                                logger.error(f"Tahmin formatı tanınmıyor")
                                predicted_text = ""
                            
                            # Tahmin metnini result tipine çevir
                            if '1' in predicted_text or 'Ev Sahibi' in predicted_text or 'home' in predicted_text.lower():
                                predicted_result = 'home_win'
                            elif '2' in predicted_text or 'Deplasman' in predicted_text or 'away' in predicted_text.lower():
                                predicted_result = 'away_win'
                            elif 'X' in predicted_text or 'Beraberlik' in predicted_text or 'draw' in predicted_text.lower():
                                predicted_result = 'draw'
                            else:
                                predicted_result = 'unknown'
                            
                            # Gerçek sonucu belirle
                            if home_score > away_score:
                                actual_winner = 'home_win'
                            elif away_score > home_score:
                                actual_winner = 'away_win'
                            else:
                                actual_winner = 'draw'
                            
                            is_correct = (predicted_result == actual_winner)
                            
                            logger.info(f"📊 Maç bitti - Tahmin:{predicted_result}, Gerçek:{actual_winner}, Doğru:{is_correct}")
                            
                            # Veritabanını güncelle
                            if cached_prediction.is_correct is None:
                                db_manager.update_prediction_result(fixture_id, actual_result, is_correct)
                            
                            analysis_data['is_correct'] = is_correct
                            analysis_data['match_result'] = actual_result
                    except Exception as e:
                        logger.warning(f"Maç sonucu kontrol hatası: {e}")
                    
                    # Raporu formatla (cache'den) - TAM FORMAT KULLAN
                    # Cache verilerini yeni format için dönüştür
                    match_info = analysis_data['match_info']
                    pred_data = analysis_data['prediction']
                    
                    # Yeni format için analysis objesi oluştur
                    full_analysis = {
                        'match': match_info.get('match', 'N/A'),
                        'league': match_info.get('league', 'N/A'),
                        'venue': match_info.get('venue', 'N/A'),
                        'date': match_info.get('date', ''),
                        'recommendation': match_info.get('recommendation', ''),
                        'prediction': {
                            'result': pred_data.get('result', 'N/A'),
                            'confidence': analysis_data.get('confidence', 0),
                            'probabilities': pred_data.get('probabilities', {}),
                            'over_under': pred_data.get('over_under', 'N/A'),
                            'btts': pred_data.get('btts', 'N/A'),
                            'btts_probability': pred_data.get('btts_probability', 'N/A'),
                            'expected_goals': pred_data.get('expected_goals', 'N/A')
                        },
                        'analysis': pred_data.get('analysis', {}),
                        'betting_odds': pred_data.get('betting_odds', {})
                    }
                    
                    # Bahis oranları yoksa API'den çek
                    if not full_analysis['betting_odds'].get('available') and fixture_id:
                        try:
                            odds_data = api_service.get_odds(fixture_id)
                            if odds_data:
                                # Oranları formata uygun hale getir
                                full_analysis['betting_odds'] = {
                                    'available': True,
                                    'bookmaker': odds_data.get('bookmaker', 'Bet365'),
                                    'match_winner': odds_data.get('match_winner', {}),
                                    'over_under_25': odds_data.get('over_under_25', {}),
                                    'btts': odds_data.get('btts', {}),
                                    'implied_probabilities': {}
                                }
                                
                                # İmplied probabilities hesapla
                                if odds_data.get('match_winner'):
                                    mw = odds_data['match_winner']
                                    full_analysis['betting_odds']['implied_probabilities']['match_winner'] = {}
                                    if 'home' in mw:
                                        full_analysis['betting_odds']['implied_probabilities']['match_winner']['home'] = (1/mw['home'])*100
                                    if 'draw' in mw:
                                        full_analysis['betting_odds']['implied_probabilities']['match_winner']['draw'] = (1/mw['draw'])*100
                                    if 'away' in mw:
                                        full_analysis['betting_odds']['implied_probabilities']['match_winner']['away'] = (1/mw['away'])*100
                                
                                if odds_data.get('over_under_25'):
                                    ou = odds_data['over_under_25']
                                    full_analysis['betting_odds']['implied_probabilities']['over_under'] = {}
                                    if 'over' in ou:
                                        full_analysis['betting_odds']['implied_probabilities']['over_under']['over'] = (1/ou['over'])*100
                                    if 'under' in ou:
                                        full_analysis['betting_odds']['implied_probabilities']['over_under']['under'] = (1/ou['under'])*100
                                
                                if odds_data.get('btts'):
                                    btts = odds_data['btts']
                                    full_analysis['betting_odds']['implied_probabilities']['btts'] = {}
                                    if 'yes' in btts:
                                        full_analysis['betting_odds']['implied_probabilities']['btts']['yes'] = (1/btts['yes'])*100
                                    if 'no' in btts:
                                        full_analysis['betting_odds']['implied_probabilities']['btts']['no'] = (1/btts['no'])*100
                                        
                        except Exception as e:
                            logger.warning(f"Bahis oranları API'den alınamadı: {e}")
                    
                    # Sonuç indikatörü ekle (eğer maç bittiyse)
                    result_note = ""
                    if analysis_data.get('is_correct') is not None:
                        if analysis_data['is_correct']:
                            result_note = "\n\n✅ **TAHMİN DOĞRU!**"
                        else:
                            result_note = "\n\n🔴 **TAHMİN YANLIŞ!**"
                        result_note += f"\n**📊 Gerçek Sonuç:** {analysis_data['match_result']}"
                    
                    report = self._format_prediction_report(full_analysis) + result_note
                    
                except Exception as e:
                    logger.error(f"Cache parse hatası: {e}", exc_info=True)
                    # Cache bozuksa yeni analiz yap
                    cached_prediction = None
            
            if not cached_prediction:
                # Cache'de yok - ÖNCE MAÇIN DURUMUNU KONTROL ET
                logger.info(f"🔄 Yeni tahmin yapılıyor: fixture_id={fixture_id}")
                
                # Maç başladı mı / bitti mi kontrol et
                try:
                    fixture_details = api_service.get_fixture_details(fixture_id)
                    if fixture_details:
                        match_status = fixture_details['fixture']['status']['short']
                        
                        # Eğer maç başladıysa veya bittiyse tahmin YAPMA!
                        if match_status not in ['NS', 'TBD', 'PST']:  # NS=Not Started, TBD=To Be Defined, PST=Postponed
                            error_msg = (
                                "⚠️ Bu maç için tahmin yapılamaz!\n\n"
                                f"📊 Maç Durumu: {match_status}\n\n"
                                "💡 Sadece **başlamamış maçlar** için tahmin yapabilirsiniz.\n"
                                "Bu, tahminlerin güvenilirliğini korumak içindir.\n\n"
                                "🔙 Lütfen başka bir maç seçin."
                            )
                            keyboard = [[InlineKeyboardButton("📅 Bugünün Maçları", callback_data="today_matches")],
                                      [InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]]
                            reply_markup = InlineKeyboardMarkup(keyboard)
                            await loading_msg.edit_text(error_msg, reply_markup=reply_markup)
                            return
                except Exception as e:
                    logger.warning(f"Maç durumu kontrol hatası: {e}")
                
                # Tahmin analizi
                try:
                    analysis = prediction_engine.analyze_match(fixture_id)
                except Exception as e:
                    logger.error(f"Tahmin motoru hatası: {e}", exc_info=True)
                    analysis = None
                
                if not analysis:
                    error_msg = (
                        "❌ Maç analizi yapılamadı.\n\n"
                        "💡 Olası sebepler:\n"
                        "• Maç verisi eksik veya erişilemiyor\n"
                        "• API yanıt vermiyor\n"
                        "• Geçersiz maç kodu\n\n"
                        "🔄 Lütfen başka bir maç deneyin veya\n"
                        "birkaç dakika sonra tekrar deneyin."
                    )
                    await loading_msg.edit_text(error_msg)
                    return
                
                # Maç tarihini al
                match_date = None
                try:
                    match_date = datetime.fromisoformat(analysis['date'].replace('Z', '+00:00'))
                except Exception as e:
                    logger.warning(f"Tarih parse hatası: {e}")
                
                # Veritabanına kaydet
                try:
                    db_manager.log_prediction(
                        user_id=db_user.id,
                        fixture_id=fixture_id,
                        match_info=json.dumps({
                            'match': analysis['match'],
                            'league': analysis['league'],
                            'venue': analysis.get('venue', 'N/A'),
                            'date': analysis.get('date', ''),
                            'recommendation': analysis.get('recommendation', '')
                        }),
                        prediction=json.dumps({
                            **analysis['prediction'],
                            'analysis': analysis.get('analysis', {}),
                            'betting_odds': analysis.get('betting_odds', {})
                        }),
                        confidence=analysis['prediction']['confidence'],
                        match_date=match_date
                    )
                    logger.info(f"✅ Tahmin veritabanına kaydedildi")
                except Exception as e:
                    logger.error(f"Veritabanı kayıt hatası: {e}")
                
                # Tahmin raporunu oluştur
                report = self._format_prediction_report(analysis)
            
            # Ana menü butonu ekle
            keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await loading_msg.edit_text(report, parse_mode='Markdown', reply_markup=reply_markup)
            logger.info(f"✅ Tahmin başarıyla gönderildi: fixture_id={fixture_id}")
            
        except (IndexError, ValueError) as e:
            logger.error(f"Geçersiz fixture ID hatası: {e}")
            error_msg = (
                "❌ Geçersiz maç kodu.\n\n"
                "💡 Kullanım: /tahmin[KOD]\n"
                "📝 Örnek: /tahmin1479575"
            )
            if loading_msg:
                await loading_msg.edit_text(error_msg)
            else:
                await update.message.reply_text(error_msg)
        except Exception as e:
            logger.error(f"Beklenmeyen tahmin hatası: {e}", exc_info=True)
            error_msg = (
                "❌ Bir hata oluştu.\n\n"
                "Lütfen daha sonra tekrar deneyin.\n"
                "Sorun devam ederse /yardim komutunu kullanın."
            )
            if loading_msg:
                try:
                    await loading_msg.edit_text(error_msg)
                except:
                    pass
    
    def _format_prediction_report(self, analysis: Dict) -> str:
        """Tahmin raporunu formatla"""
        pred = analysis['prediction']
        home = analysis['analysis']['home_team']
        away = analysis['analysis']['away_team']
        h2h = analysis['analysis']['h2h']
        betting = analysis.get('betting_odds', {})
        
        # Bahis oranları bölümü
        betting_section = ""
        if betting.get('available'):
            betting_section = f"\n━━━━━━━━━━━━━━━━━━━━\n\n"
            betting_section += f"**💰 BAHİS ORANLARI**\n\n"
            
            # 1X2 Oranları
            if betting.get('match_winner'):
                mw = betting['match_winner']
                imp = betting.get('implied_probabilities', {}).get('match_winner', {})
                
                betting_section += f"**Maç Sonucu (1X2):**\n"
                if 'home' in mw:
                    prob_text = f" (Gerçek Olasılık: {imp['home']:.1f}%)" if 'home' in imp else ""
                    betting_section += f"🏠 MS1: {mw['home']}{prob_text}\n"
                if 'draw' in mw:
                    prob_text = f" (Gerçek Olasılık: {imp['draw']:.1f}%)" if 'draw' in imp else ""
                    betting_section += f"⚖️ X: {mw['draw']}{prob_text}\n"
                if 'away' in mw:
                    prob_text = f" (Gerçek Olasılık: {imp['away']:.1f}%)" if 'away' in imp else ""
                    betting_section += f"✈️ MS2: {mw['away']}{prob_text}\n"
            
            # Over/Under 2.5
            if betting.get('over_under_25'):
                ou = betting['over_under_25']
                imp = betting.get('implied_probabilities', {}).get('over_under', {})
                
                betting_section += f"\n**Gol Sayısı (2.5):**\n"
                if 'over' in ou:
                    prob_text = f" (Gerçek Olasılık: {imp['over']:.1f}%)" if 'over' in imp else ""
                    betting_section += f"📈 Üst 2.5: {ou['over']}{prob_text}\n"
                if 'under' in ou:
                    prob_text = f" (Gerçek Olasılık: {imp['under']:.1f}%)" if 'under' in imp else ""
                    betting_section += f"📉 Alt 2.5: {ou['under']}{prob_text}\n"
            
            # BTTS
            if betting.get('btts'):
                btts_odds = betting['btts']
                imp = betting.get('implied_probabilities', {}).get('btts', {})
                
                betting_section += f"\n**Karşılıklı Gol (KG):**\n"
                if 'yes' in btts_odds:
                    prob_text = f" (Gerçek Olasılık: {imp['yes']:.1f}%)" if 'yes' in imp else ""
                    betting_section += f"✅ KG Var: {btts_odds['yes']}{prob_text}\n"
                if 'no' in btts_odds:
                    prob_text = f" (Gerçek Olasılık: {imp['no']:.1f}%)" if 'no' in imp else ""
                    betting_section += f"❌ KG Yok: {btts_odds['no']}{prob_text}\n"
        
        report = f"""
🎯 **TAHMİN ANALİZİ**

**⚽ Maç:** {analysis['match']}
**🏆 Lig:** {analysis['league']}
**🏟️ Saha:** {analysis['venue']}
**📅 Tarih:** {datetime.fromisoformat(analysis['date'].replace('Z', '+00:00')).strftime('%d.%m.%Y %H:%M')}

━━━━━━━━━━━━━━━━━━━━

**🎲 TAHMİN: {pred['result']}**
**📊 Güven Oranı: {pred['confidence']}%**

{analysis['recommendation']}

**📈 Olasılıklar:**
🏠 Ev Sahibi: {pred['probabilities']['home_win']}%
⚖️ Beraberlik: {pred['probabilities']['draw']}%
✈️ Deplasman: {pred['probabilities']['away_win']}%

**⚽ Gol Tahminleri:**
📊 {pred['over_under']}
🎯 BTTS: {pred['btts']} ({pred['btts_probability']}%)
⚽ Beklenen Gol: {pred['expected_goals']}
{betting_section}
━━━━━━━━━━━━━━━━━━━━

**📊 TAKIM ANALİZİ**

**🏠 {home['name']}**
Form: {''.join(home['form'])} (Skor: {home['form_score']}%)
⚽ Gol Ort: {home['goals_avg']} | Yenilen: {home['conceded_avg']}
📈 Kazanma Oranı: {home['win_rate']}%

**✈️ {away['name']}**
Form: {''.join(away['form'])} (Skor: {away['form_score']}%)
⚽ Gol Ort: {away['goals_avg']} | Yenilen: {away['conceded_avg']}
📈 Kazanma Oranı: {away['win_rate']}%

**🤝 Kafa Kafaya (Son {h2h['total_matches']} Maç)**
🏠 Ev Sahibi Galibiyeti: {h2h['home_wins']}
⚖️ Beraberlik: {h2h['draws']}
✈️ Deplasman Galibiyeti: {h2h['away_wins']}
        """
        
        return report
    
    def _format_cached_prediction_report(self, analysis_data: Dict) -> str:
        """Cache'den gelen tahmin raporunu formatla (orijinal tahmin gösterilir)"""
        match_info = analysis_data['match_info']
        pred = analysis_data['prediction']
        fixture_id = analysis_data.get('fixture_id')
        
        # Tahmin sonucu göstergesi
        result_indicator = ""
        if analysis_data.get('is_correct') is not None:
            if analysis_data['is_correct']:
                result_indicator = "✅ **TAHMİN DOĞRU!**"
            else:
                result_indicator = "🔴 **UYARI: TAHMİN YANLIŞ!**"
            
            result_indicator += f"\n**📊 Gerçek Sonuç:** {analysis_data['match_result']}\n"
        
        # Tahmin tipini çevir
        result_map = {
            'home_win': '🏠 Ev Sahibi Kazanır',
            'away_win': '✈️ Deplasman Kazanır',
            'draw': '⚖️ Beraberlik'
        }
        
        prediction_text = result_map.get(pred['result'], pred['result'])
        
        report = f"""
🎯 **TAHMİN ANALİZİ**

**⚽ Maç:** {match_info['match']}
**🏆 Lig:** {match_info['league']}

━━━━━━━━━━━━━━━━━━━━

{result_indicator}

**🎲 TAHMİN: {prediction_text}**
**📊 Güven Oranı: {analysis_data['confidence']}%**

**📈 Olasılıklar:**
🏠 Ev Sahibi: {pred['probabilities']['home_win']}%
⚖️ Beraberlik: {pred['probabilities']['draw']}%
✈️ Deplasman: {pred['probabilities']['away_win']}%

**⚽ Gol Tahminleri:**
📊 {pred.get('over_under', 'N/A')}
🎯 BTTS: {pred.get('btts', 'N/A')} ({pred.get('btts_probability', 'N/A')}%)
⚽ Beklenen Gol: {pred.get('expected_goals', 'N/A')}
        """
        
        # TAKIM ANALİZİ BÖLÜMÜ EKLE
        if 'analysis' in pred:
            analysis = pred['analysis']
            team_analysis = "\n\n━━━━━━━━━━━━━━━━━━━━\n\n"
            team_analysis += "📊 **TAKIM ANALİZİ**\n\n"
            
            # Ev Sahibi Takım
            if 'home_team' in analysis:
                ht = analysis['home_team']
                team_analysis += f"**🏠 {ht.get('name', 'Ev Sahibi')}**\n"
                if 'form' in ht: team_analysis += f"📈 Form: {ht['form']}\n"
                if 'goals_avg' in ht: team_analysis += f"⚽ Gol Ortalaması: {ht['goals_avg']}\n"
                if 'win_rate' in ht: team_analysis += f"🎯 Kazanma Oranı: %{ht['win_rate']}\n"
                team_analysis += "\n"
            
            # Deplasman Takım
            if 'away_team' in analysis:
                at = analysis['away_team']
                team_analysis += f"**✈️ {at.get('name', 'Deplasman')}**\n"
                if 'form' in at: team_analysis += f"📈 Form: {at['form']}\n"
                if 'goals_avg' in at: team_analysis += f"⚽ Gol Ortalaması: {at['goals_avg']}\n"
                if 'win_rate' in at: team_analysis += f"🎯 Kazanma Oranı: %{at['win_rate']}\n"
            
            report += team_analysis
        
        # BAHİS ORANLARI BÖLÜMÜ EKLE (API'den çek)
        if fixture_id:
            try:
                from api_football import APIFootball
                api = APIFootball()
                odds_data = api.get_odds(fixture_id)
                
                if odds_data:
                    betting_section = "\n\n━━━━━━━━━━━━━━━━━━━━\n\n"
                    betting_section += f"💰 **BAHİS ORANLARI** ({odds_data['bookmaker']})\n\n"
                    
                    # Maç Sonucu (1X2)
                    if 'match_winner' in odds_data and odds_data['match_winner']:
                        mw = odds_data['match_winner']
                        betting_section += "**🎲 Maç Sonucu (1X2)**\n"
                        
                        # Oranları ve gerçek olasılıkları göster
                        if 'home' in mw:
                            impl_prob = (1 / mw['home']) * 100
                            betting_section += f"🏠 MS1: {mw['home']:.2f} (%{impl_prob:.1f} olasılık)\n"
                        
                        if 'draw' in mw:
                            impl_prob = (1 / mw['draw']) * 100
                            betting_section += f"🤝 X (Beraberlik): {mw['draw']:.2f} (%{impl_prob:.1f} olasılık)\n"
                        
                        if 'away' in mw:
                            impl_prob = (1 / mw['away']) * 100
                            betting_section += f"✈️ MS2: {mw['away']:.2f} (%{impl_prob:.1f} olasılık)\n"
                        
                        betting_section += "\n"
                    
                    # Alt/Üst 2.5
                    if 'over_under_25' in odds_data and odds_data['over_under_25']:
                        ou = odds_data['over_under_25']
                        betting_section += "**📊 Alt/Üst 2.5 Gol**\n"
                        
                        if 'over' in ou:
                            impl_prob = (1 / ou['over']) * 100
                            betting_section += f"⬆️ Üst 2.5: {ou['over']:.2f} (%{impl_prob:.1f} olasılık)\n"
                        
                        if 'under' in ou:
                            impl_prob = (1 / ou['under']) * 100
                            betting_section += f"⬇️ Alt 2.5: {ou['under']:.2f} (%{impl_prob:.1f} olasılık)\n"
                        
                        betting_section += "\n"
                    
                    # Karşılıklı Gol
                    if 'btts' in odds_data and odds_data['btts']:
                        btts = odds_data['btts']
                        betting_section += "**⚽ Karşılıklı Gol (KG)**\n"
                        
                        if 'yes' in btts:
                            impl_prob = (1 / btts['yes']) * 100
                            betting_section += f"✅ Var: {btts['yes']:.2f} (%{impl_prob:.1f} olasılık)\n"
                        
                        if 'no' in btts:
                            impl_prob = (1 / btts['no']) * 100
                            betting_section += f"❌ Yok: {btts['no']:.2f} (%{impl_prob:.1f} olasılık)\n"
                    
                    report += betting_section
                else:
                    logger.info(f"Bahis oranları bulunamadı: fixture_id={fixture_id}")
                    
            except Exception as e:
                logger.warning(f"Bahis oranları alınamadı: {e}")
        
        return report
    
    async def _show_premium_required(self, update: Update):
        """Premium gerekli mesajı göster"""
        message = """
⚠️ **Günlük Ücretsiz Tahmin Hakkınız Doldu!**

Premium üye olarak sınırsız tahmin alabilirsiniz.

💎 **Premium Avantajları:**
✅ Sınırsız tahmin
✅ Günlük en iyi tahminler
✅ Özel analizler
✅ Öncelikli destek

Premium paketleri görüntülemek için /premium komutunu kullanın.
        """
        
        keyboard = [
            [InlineKeyboardButton("💎 Premium Paketler", callback_data="premium_info")],
            [InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.message.reply_text(
                message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    async def premium_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Premium paket bilgileri"""
        query = update.callback_query
        if query:
            await query.answer()
            message = query.message
        else:
            message = update.message
        
        premium_text = f"""
💎 **PREMIUM PAKETLER**

**📱 Günlük Paket**
💰 Fiyat: {os.getenv('DAILY_PRICE', '50')} TL
⏱️ Süre: 24 Saat
✅ Sınırsız tahmin

**📅 Haftalık Paket**
💰 Fiyat: {os.getenv('WEEKLY_PRICE', '200')} TL
⏱️ Süre: 7 Gün
✅ Sınırsız tahmin
✅ %20 İndirim

**⭐ Aylık Paket** (EN POPÜLER)
💰 Fiyat: {os.getenv('MONTHLY_PRICE', '500')} TL
⏱️ Süre: 30 Gün
✅ Sınırsız tahmin
✅ %50 İndirim
✅ Özel analizler

**💳 Ödeme Yöntemleri:**
• Kredi Kartı
• Banka Kartı
• Havale/EFT

Satın almak için aşağıdan bir paket seçin:
        """
        
        keyboard = [
            [InlineKeyboardButton("📱 Günlük - 50 TL", callback_data="buy_daily")],
            [InlineKeyboardButton("📅 Haftalık - 200 TL", callback_data="buy_weekly")],
            [InlineKeyboardButton("⭐ Aylık - 500 TL", callback_data="buy_monthly")],
            [InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.reply_text(
            premium_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def user_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Kullanıcı istatistikleri"""
        query = update.callback_query
        user = update.effective_user
        
        if query:
            await query.answer()
            message = query.message
        else:
            message = update.message
        
        stats = db_manager.get_user_stats(user.id)
        
        if not stats:
            await message.reply_text("❌ İstatistikler yüklenemedi.")
            return
        
        db_user = stats['user']
        
        stats_text = f"""
📊 **KULLANICI İSTATİSTİKLERİ**

**👤 Kullanıcı:** {user.first_name}
**🆔 ID:** {user.id}

**📈 Genel:**
✅ Toplam Tahmin: {stats['total_predictions']}
💎 Premium: {'Aktif ✅' if stats['is_premium'] else 'Pasif ❌'}

**🎁 Ücretsiz Haklar:**
Bugün kullanılan: {db_user.free_predictions_used}/{os.getenv('FREE_PREDICTIONS_PER_DAY', 2)}
        """
        
        if stats['is_premium']:
            end_date = stats['subscription_end']
            stats_text += f"\n**⏰ Abonelik Bitiş:** {end_date.strftime('%d.%m.%Y %H:%M')}"
        
        stats_text += f"\n\n**💰 Toplam Harcama:** {db_user.total_spent} TL"
        
        keyboard = [
            [InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]
        ]
        
        if not stats['is_premium']:
            keyboard.insert(0, [InlineKeyboardButton("💎 Premium Ol", callback_data="premium_info")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.reply_text(
            stats_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def top_predictions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """En iyi tahminler"""
        query = update.callback_query
        if query:
            await query.answer()
            message = query.message
            is_callback = True
        else:
            message = update.message
            is_callback = False
        
        # DEMO MOD: Premium kontrolü YOK
        # user = update.effective_user
        # db_user = db_manager.get_or_create_user(telegram_id=user.id)
        
        # if not db_user.is_subscription_active():
        #     await self._show_premium_required(update)
        #     return
        
        if is_callback:
            await query.edit_message_text(
                "🔄 En iyi tahminler analiz ediliyor...\n"
                "⏳ Bu işlem 30-60 saniye sürebilir..."
            )
        else:
            loading_msg = await message.reply_text(
                "🔄 En iyi tahminler analiz ediliyor...\n"
                "⏳ Bu işlem 30-60 saniye sürebilir..."
            )
        
        try:
            predictions = prediction_engine.get_top_predictions_today(min_confidence=60.0)
            
            if not predictions:
                error_text = (
                    "❌ Bugün için yüksek güvenli tahmin bulunamadı.\n\n"
                    "💡 Sebep: 60% üzeri güvenli tahmin yok.\n"
                    "🔄 Normal tahminler için maç listesine bakın."
                )
                keyboard = [[InlineKeyboardButton("📅 Bugünün Maçları", callback_data="today_matches")],
                           [InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                if is_callback:
                    await query.edit_message_text(error_text, reply_markup=reply_markup)
                else:
                    await loading_msg.edit_text(error_text, reply_markup=reply_markup)
                return
            
            response = "🎯 **BUGÜNÜN EN İYİ TAHMİNLERİ**\n\n"
            response += f"📊 {len(predictions)} yüksek güvenli tahmin bulundu!\n\n"
            
            for idx, pred in enumerate(predictions[:5], 1):
                response += f"**{idx}. {pred['match']}**\n"
                response += f"🏆 {pred['league']}\n"
                response += f"🎲 Tahmin: {pred['prediction']['result']}\n"
                response += f"📊 Güven: {pred['prediction']['confidence']}%\n"
                response += f"⚽ Skor: {pred['prediction']['expected_goals']}\n"
                response += f"/tahmin{pred['fixture_id']}\n\n"
            
            keyboard = [
                [InlineKeyboardButton("📅 Bugünün Maçları", callback_data="today_matches")],
                [InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if is_callback:
                await query.edit_message_text(response, parse_mode='Markdown', reply_markup=reply_markup)
            else:
                await loading_msg.edit_text(response, parse_mode='Markdown', reply_markup=reply_markup)
                
        except Exception as e:
            logger.error(f"Top predictions hatası: {e}")
            error_text = (
                "❌ En iyi tahminler alınırken hata oluştu.\n\n"
                f"💡 Hata: {str(e)[:100]}\n\n"
                "🔄 Lütfen daha sonra tekrar deneyin."
            )
            keyboard = [[InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if is_callback:
                await query.edit_message_text(error_text, reply_markup=reply_markup)
            else:
                await loading_msg.edit_text(error_text, reply_markup=reply_markup)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Buton tıklama işleyici"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "main_menu":
            # Ana menüye dön
            user = update.effective_user
            
            welcome_message = f"""
🎯 **Futbol Tahmin Botuna Hoş Geldiniz!** ⚽

Merhaba {user.first_name}! 

🎁 **DEMO MOD AKTİF - Sınırsız Tahmin!** 🎁

Bu bot, gelişmiş AI algoritmaları ve gerçek zamanlı istatistiklerle 
futbol maçları için profesyonel tahminler sunar.

**📊 Özellikler:**
✅ Canlı maç tahminleri
✅ Detaylı istatistiksel analiz
✅ H2H (Kafa Kafaya) karşılaştırma
✅ Form analizi
✅ Over/Under tahminleri
✅ BTTS (İki takım da gol atar mı?) tahmini

**🎁 Test Sürümü:**
💎 Sınırsız tahmin - Ücretsiz!
💎 Tüm premium özellikler aktif!
� Ödeme sistemi kapalı (test için)

**📱 Komutlar:**
/tahmin - Maç tahmini al
/bugun - Bugünün maçları
/premium - Premium paketler
/istatistik - İstatistikleriniz
/yardim - Yardım menüsü

Haydi başlayalım! ⚽🎯
            """
            
            keyboard = [
                [InlineKeyboardButton("⚽ Tahmin Al", callback_data="get_prediction")],
                [InlineKeyboardButton("📅 Bugünün Maçları", callback_data="today_matches")],
                [InlineKeyboardButton("� Dünün Sonuçları", callback_data="yesterday_matches")],
                [InlineKeyboardButton("�💎 Premium Ol", callback_data="premium_info")],
                [InlineKeyboardButton("� İstatistiklerim", callback_data="my_stats")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                welcome_message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
        elif query.data == "get_prediction":
            await self.get_prediction(update, context)
        elif query.data == "today_matches":
            await self.today_matches(update, context, page=0)
        elif query.data == "yesterday_matches":
            await self.yesterday_matches(update, context, page=0)
        elif query.data.startswith("matches_page_"):
            # Sayfa değişikliği
            page = int(query.data.replace("matches_page_", ""))
            await self.today_matches(update, context, page=page)
        elif query.data.startswith("yesterday_page_"):
            # Dünün maçları sayfa değişikliği
            page = int(query.data.replace("yesterday_page_", ""))
            await self.yesterday_matches(update, context, page=page)
        elif query.data.startswith("pred_"):
            # Maç tahmin butonu - fixture_id'yi al
            fixture_id = query.data.replace("pred_", "")
            context.args = [fixture_id]
            await self.specific_prediction(update, context, is_from_button=True)
        elif query.data == "premium_info":
            await self.premium_info(update, context)
        elif query.data == "my_stats":
            await self.user_stats(update, context)
        elif query.data == "top_predictions":
            await self.top_predictions(update, context)
        elif query.data.startswith("buy_"):
            await payment_handler.handle_purchase(update, context, query.data)
    
    async def auto_predict_today_matches(self, context: ContextTypes.DEFAULT_TYPE):
        """Bugünün tüm maçlarını otomatik olarak tahmin et ve kaydet"""
        logger.info("🤖 Otomatik tahmin sistemi başlatıldı...")
        
        try:
            # Bugünün maçlarını al
            matches = api_service.get_today_matches()
            
            if not matches:
                logger.info("📭 Bugün için maç bulunamadı")
                return
            
            logger.info(f"📊 {len(matches)} maç bulundu, tahminler hesaplanıyor...")
            
            success_count = 0
            skip_count = 0
            error_count = 0
            
            for match in matches:
                try:
                    fixture_id = match['fixture']['id']
                    home_team = match['teams']['home']['name']
                    away_team = match['teams']['away']['name']
                    match_datetime = match['fixture']['date']
                    
                    # Zaten tahmin var mı kontrol et
                    existing_pred = db_manager.get_cached_prediction(fixture_id=fixture_id)
                    if existing_pred:
                        logger.info(f"⏭️ Atlanıyor (tahmin mevcut): {home_team} vs {away_team}")
                        skip_count += 1
                        continue
                    
                    # Tahmin yap
                    logger.info(f"🔮 Tahmin yapılıyor: {home_team} vs {away_team}")
                    result = prediction_engine.analyze_match(fixture_id)
                    
                    if result and result.get('prediction'):
                        # Match info oluştur
                        match_info = f"{home_team} vs {away_team} - {match['league']['name']}"
                        
                        # Maç tarihini parse et
                        try:
                            match_date = date_parser.parse(match_datetime) if match_datetime else datetime.now()
                        except:
                            match_date = datetime.now()
                        
                        # Tahmin bilgilerini al
                        prediction_data = result.get('prediction', {})
                        confidence = prediction_data.get('confidence', 0)
                        
                        # Eğer confidence None ise varsayılan değer kullan
                        if confidence is None:
                            confidence = 50.0
                        
                        # Veritabanına kaydet
                        db_manager.log_prediction(
                            user_id=0,  # Sistem tahmini (kullanıcı değil)
                            fixture_id=fixture_id,
                            match_info=match_info,
                            prediction=json.dumps(result),
                            confidence=float(confidence),
                            match_date=match_date
                        )
                        
                        pred_result = prediction_data.get('result', 'Unknown')
                        logger.info(f"✅ Kaydedildi: {home_team} vs {away_team} - {pred_result} ({confidence:.1f}%)")
                        success_count += 1
                    else:
                        logger.warning(f"⚠️ Tahmin alınamadı: {home_team} vs {away_team}")
                        error_count += 1
                    
                except Exception as e:
                    logger.error(f"❌ Hata ({home_team} vs {away_team}): {e}")
                    error_count += 1
            
            logger.info(f"🎯 Otomatik tahmin tamamlandı! ✅ {success_count} başarılı, ⏭️ {skip_count} atlandı, ❌ {error_count} hata")
            
        except Exception as e:
            logger.error(f"❌ Otomatik tahmin sistemi hatası: {e}")
    
    def run(self):
        """Botu başlat"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN bulunamadı!")
        
        # Uygulama oluştur
        self.app = Application.builder().token(token).build()
        
        # Komut handler'ları
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("yardim", self.help_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("bugun", self.today_matches))
        self.app.add_handler(CommandHandler("dun", self.yesterday_matches))
        self.app.add_handler(CommandHandler("tahmin", self.get_prediction))
        self.app.add_handler(CommandHandler("premium", self.premium_info))
        self.app.add_handler(CommandHandler("istatistik", self.user_stats))
        
        # Tahmin komutları (dinamik)
        # /tahmin1479575 veya /tahmin_1479575 formatlarını destekle
        self.app.add_handler(MessageHandler(
            filters.Regex(r'^/tahmin[_]?\d+$'),
            self.specific_prediction
        ))
        
        # Callback handler
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Admin komutlarını ekle
        from admin_panel import setup_admin_handlers
        setup_admin_handlers(self.app, db_manager)
        logger.info("Admin komutları yüklendi!")
        
        # Otomatik tahmin zamanlayıcısı (Her gece 00:05'te)
        job_queue = self.app.job_queue
        turkey_tz = pytz.timezone('Europe/Istanbul')
        
        # Her gece 00:05'te çalış (yeni günün maçları için)
        job_queue.run_daily(
            self.auto_predict_today_matches,
            time=datetime.strptime("00:05", "%H:%M").time(),
            days=(0, 1, 2, 3, 4, 5, 6),  # Her gün
            name="auto_predict_daily"
        )
        logger.info("⏰ Otomatik tahmin zamanlayıcısı kuruldu (Her gece 00:05 Türkiye saati)")
        
        # Botu başlat
        logger.info("Bot başlatılıyor...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    bot = FootballPredictionBot()
    bot.run()
