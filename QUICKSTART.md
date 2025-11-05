# 🚀 HIZLI BAŞLANGIÇ REHBERİ

## ⚡ 5 Dakikada Kurulum

### 1️⃣ Telegram Bot Oluşturun
1. Telegram'da [@BotFather](https://t.me/BotFather) ile konuşun
2. `/newbot` yazın
3. Bot için bir isim verin (örn: "Futbol Tahmin Bot")
4. Bot için bir kullanıcı adı verin (örn: "futbol_tahmin_bot")
5. Size verilen **token**'ı kopyalayın

### 2️⃣ Telegram ID'nizi Öğrenin
1. [@userinfobot](https://t.me/userinfobot) ile konuşun
2. Size gönderilen **ID**'yi not alın

### 3️⃣ Kurulumu Yapın

```bash
# 1. Kurulum scriptini çalıştırın
python setup.py

# 2. .env dosyasını düzenleyin
# Not: .env.example dosyası otomatik olarak .env'ye kopyalanacak
```

### 4️⃣ .env Dosyasını Doldurun

`.env` dosyasını açıp şu bilgileri girin:

```env
# Telegram Bot Token (BotFather'dan aldınız)
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# API Football Key (ÖNCELİKLE HAZIR)
API_FOOTBALL_KEY=6336fb21e17dea87880d3b133132a13f

# Admin ID'niz (userinfobot'tan aldınız)
ADMIN_IDS=123456789

# Stripe (opsiyonel - demo modda çalışır)
STRIPE_SECRET_KEY=your_stripe_secret_key_here
```

### 5️⃣ Botu Başlatın

```bash
# Test edin
python test_api.py

# Botu çalıştırın
python main.py
```

## 🎯 Botu Test Etme

1. Telegram'da botunuzu bulun
2. `/start` yazın
3. "⚽ Tahmin Al" butonuna tıklayın
4. Bir maç seçin ve tahmin alın!

## 💎 Premium Test (Demo Mod)

Stripe ayarlanmadığı için bot **demo modda** çalışır:
- Premium satın almalar otomatik aktive olur
- Gerçek ödeme gerekmez
- Test için mükemmeldir

## 🔧 Sorun Giderme

### Bot başlamıyor?
```bash
# Gereksinimleri tekrar yükleyin
pip install -r requirements.txt

# .env dosyasını kontrol edin
# TELEGRAM_BOT_TOKEN ve API_FOOTBALL_KEY dolu olmalı
```

### API çalışmıyor?
```bash
# API testini çalıştırın
python test_api.py

# Hata varsa, internet bağlantınızı kontrol edin
```

### Tahmin almıyor?
- API-Football key'in geçerli olduğundan emin olun
- Bugün maç olup olmadığını kontrol edin (`/bugun`)
- Log dosyasını kontrol edin: `bot.log`

## 📱 Admin Komutları

Telegram ID'nizi `.env` dosyasındaki `ADMIN_IDS`'e eklediyseniz:

- `/adminstats` - Bot istatistikleri
- `/givepremium <user_id> monthly` - Ücretsiz premium ver
- `/broadcast Merhaba` - Tüm kullanıcılara mesaj gönder

## 🎁 Demo Özellikleri

✅ Tüm tahmin özellikleri aktif
✅ Gerçek API-Football verileri
✅ Demo ödeme sistemi (gerçek para gerekmez)
✅ Tam fonksiyonel admin paneli

## 📞 Yardım

Sorun mu var? 
1. `bot.log` dosyasını kontrol edin
2. `test_api.py` çalıştırarak test edin
3. README.md dosyasını okuyun

---

**🎉 Artık hazırsınız! İyi tahminler!** ⚽🎯
