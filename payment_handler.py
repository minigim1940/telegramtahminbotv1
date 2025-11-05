"""
Ödeme İşleme Modülü
Stripe entegrasyonu ve abonelik yönetimi
"""

import os
import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import stripe

logger = logging.getLogger(__name__)


class PaymentHandler:
    """Ödeme ve abonelik işlemlerini yöneten sınıf"""
    
    def __init__(self, stripe_key: str, db_manager):
        if stripe_key and stripe_key != 'your_stripe_secret_key_here':
            stripe.api_key = stripe_key
            self.stripe_enabled = True
        else:
            self.stripe_enabled = False
            logger.warning("Stripe API key bulunamadı - Ödeme sistemi devre dışı")
        
        self.db = db_manager
        
        # Fiyatlar
        self.prices = {
            'daily': float(os.getenv('DAILY_PRICE', '50')),
            'weekly': float(os.getenv('WEEKLY_PRICE', '200')),
            'monthly': float(os.getenv('MONTHLY_PRICE', '500'))
        }
    
    async def handle_purchase(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                             subscription_type: str):
        """Satın alma işlemini başlat"""
        query = update.callback_query
        user = update.effective_user
        
        # Abonelik tipini al
        sub_type = subscription_type.replace('buy_', '')
        price = self.prices.get(sub_type, 0)
        
        if price == 0:
            await query.message.reply_text("❌ Geçersiz paket!")
            return
        
        # Kullanıcıyı veritabanına kaydet
        db_user = self.db.get_or_create_user(
            telegram_id=user.id,
            username=user.username,
            first_name=user.first_name
        )
        
        if not self.stripe_enabled:
            # Demo mod - Doğrudan aktive et
            await self._activate_demo_subscription(query, db_user, sub_type, price)
        else:
            # Gerçek ödeme süreci
            await self._create_payment_session(query, db_user, sub_type, price)
    
    async def _activate_demo_subscription(self, query, db_user, sub_type, price):
        """Demo abonelik aktivasyonu (test için)"""
        
        # Abonelik oluştur
        subscription = self.db.add_subscription(
            user_id=db_user.id,
            subscription_type=sub_type,
            price=price,
            payment_id=f"DEMO_{db_user.telegram_id}_{sub_type}"
        )
        
        if subscription:
            duration_text = {
                'daily': '24 saat',
                'weekly': '7 gün',
                'monthly': '30 gün'
            }
            
            success_message = f"""
✅ **DEMO MOD - Abonelik Aktifleştirildi!**

**💎 Paket:** {sub_type.title()}
**💰 Fiyat:** {price} TL
**⏰ Süre:** {duration_text[sub_type]}

Artık sınırsız tahmin alabilirsiniz!

⚠️ **NOT:** Bu demo moddur. Gerçek ödeme için 
Stripe API key'inizi .env dosyasına ekleyin.

/tahmin komutuyla tahminlere başlayın!
            """
            
            keyboard = [
                [InlineKeyboardButton("⚽ Tahmin Al", callback_data="get_prediction")],
                [InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                success_message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        else:
            await query.message.reply_text("❌ Abonelik oluşturulamadı!")
    
    async def _create_payment_session(self, query, db_user, sub_type, price):
        """Stripe ödeme oturumu oluştur"""
        try:
            # Stripe checkout session oluştur
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'try',
                        'product_data': {
                            'name': f'Premium {sub_type.title()} Paketi',
                            'description': 'Futbol Tahmin Botu Premium Üyelik'
                        },
                        'unit_amount': int(price * 100),  # Kuruş cinsinden
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'https://t.me/YourBotUsername?start=success_{db_user.telegram_id}',
                cancel_url=f'https://t.me/YourBotUsername?start=cancel',
                client_reference_id=f"{db_user.telegram_id}_{sub_type}",
            )
            
            payment_message = f"""
💳 **ÖDEME SAYFASI**

**Paket:** {sub_type.title()}
**Fiyat:** {price} TL

Aşağıdaki linke tıklayarak ödeme yapabilirsiniz:

{session.url}

⏱️ Ödeme linkinin geçerlilik süresi: 30 dakika
            """
            
            keyboard = [
                [InlineKeyboardButton("💳 Ödeme Yap", url=session.url)],
                [InlineKeyboardButton("❌ İptal", callback_data="main_menu")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_text(
                payment_message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe hatası: {e}")
            await query.message.reply_text(
                "❌ Ödeme işlemi başlatılamadı. Lütfen daha sonra tekrar deneyin."
            )
    
    def verify_payment(self, payment_intent_id: str) -> bool:
        """Ödeme doğrulama"""
        if not self.stripe_enabled:
            return True  # Demo modda her zaman true
        
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return payment_intent.status == 'succeeded'
        except stripe.error.StripeError:
            return False
    
    async def handle_successful_payment(self, user_id: int, subscription_type: str):
        """Başarılı ödeme sonrası işlemler"""
        price = self.prices.get(subscription_type, 0)
        
        subscription = self.db.add_subscription(
            user_id=user_id,
            subscription_type=subscription_type,
            price=price,
            payment_id=f"STRIPE_{user_id}_{subscription_type}"
        )
        
        return subscription is not None


class BankTransferHandler:
    """Havale/EFT işlemleri için yedek sistem"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        self.bank_info = {
            'bank': 'Örnek Banka',
            'iban': 'TR00 0000 0000 0000 0000 0000 00',
            'account_holder': 'ŞİRKET ADI'
        }
    
    async def show_bank_transfer_info(self, update: Update, subscription_type: str):
        """Havale bilgilerini göster"""
        query = update.callback_query
        user = update.effective_user
        
        prices = {
            'daily': float(os.getenv('DAILY_PRICE', '50')),
            'weekly': float(os.getenv('WEEKLY_PRICE', '200')),
            'monthly': float(os.getenv('MONTHLY_PRICE', '500'))
        }
        
        price = prices.get(subscription_type, 0)
        
        transfer_message = f"""
🏦 **HAVALE/EFT BİLGİLERİ**

**Banka:** {self.bank_info['bank']}
**IBAN:** {self.bank_info['iban']}
**Hesap Sahibi:** {self.bank_info['account_holder']}

**Gönderilecek Tutar:** {price} TL

**Açıklama:** {user.id}_{subscription_type}

⚠️ **ÖNEMLİ:**
• Açıklama kısmına mutlaka kullanıcı ID ve paket tipini yazın
• Havale yaptıktan sonra dekontunu @YourSupportUsername'e gönderin
• Onay süreci 1-24 saat içinde tamamlanır

📸 **Dekont Gönderme:**
Havale dekontunuzu çektikten sonra destek hesabımıza 
gönderin ve aktivasyon için bekleyin.
        """
        
        keyboard = [
            [InlineKeyboardButton("💬 Destek", url="https://t.me/YourSupportUsername")],
            [InlineKeyboardButton("🔙 Geri", callback_data="premium_info")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.reply_text(
            transfer_message,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
