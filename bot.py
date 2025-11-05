"""
Telegram Bot - Ana Bot Dosyası
Kullanıcı arayüzü ve komut işleme
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
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
            [InlineKeyboardButton("💎 Premium Ol", callback_data="premium_info")],
            [InlineKeyboardButton("📊 İstatistiklerim", callback_data="my_stats")]
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
                            
                            # Tahmin doğru mu?
                            predicted_result = analysis_data['prediction']['result']
                            if home_score > away_score:
                                actual_winner = 'home_win'
                            elif away_score > home_score:
                                actual_winner = 'away_win'
                            else:
                                actual_winner = 'draw'
                            
                            is_correct = (predicted_result == actual_winner)
                            
                            # Veritabanını güncelle
                            db_manager.update_prediction_result(fixture_id, actual_result, is_correct)
                            
                            analysis_data['is_correct'] = is_correct
                            analysis_data['match_result'] = actual_result
                    except Exception as e:
                        logger.warning(f"Maç sonucu kontrol hatası: {e}")
                    
                    # Raporu formatla (cache'den)
                    report = self._format_cached_prediction_report(analysis_data)
                    
                except Exception as e:
                    logger.error(f"Cache parse hatası: {e}", exc_info=True)
                    # Cache bozuksa yeni analiz yap
                    cached_prediction = None
            
            if not cached_prediction:
                # Cache'de yok - yeni analiz yap
                logger.info(f"🔄 Yeni tahmin yapılıyor: fixture_id={fixture_id}")
                
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
                            'league': analysis['league']
                        }),
                        prediction=json.dumps(analysis['prediction']),
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

━━━━━━━━━━━━━━━━━━━━

💡 **Not:** Bu tahmin, gelişmiş AI algoritmaları ve 
gerçek zamanlı istatistiklerle oluşturulmuştur.

🎯 İyi şanslar!
        """
        
        return report
    
    def _format_cached_prediction_report(self, analysis_data: Dict) -> str:
        """Cache'den gelen tahmin raporunu formatla (orijinal tahmin gösterilir)"""
        match_info = analysis_data['match_info']
        pred = analysis_data['prediction']
        
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
🎯 **TAHMİN ANALİZİ** (Kayıtlı Tahmin)

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

━━━━━━━━━━━━━━━━━━━━

💡 **Not:** Bu tahmin daha önce yapılmıştır ve
değiştirilmemiştir. Maç başlamadan önceki
orijinal analizdir.

📌 **Önemli:** Tahminler maç bittikten sonra
yeniden hesaplanmaz, orijinal tahmin gösterilir.
        """
        
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
                [InlineKeyboardButton("💎 Premium Ol", callback_data="premium_info")],
                [InlineKeyboardButton("📊 İstatistiklerim", callback_data="my_stats")]
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
        elif query.data.startswith("matches_page_"):
            # Sayfa değişikliği
            page = int(query.data.replace("matches_page_", ""))
            await self.today_matches(update, context, page=page)
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
        
        # Botu başlat
        logger.info("Bot başlatılıyor...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    bot = FootballPredictionBot()
    bot.run()
