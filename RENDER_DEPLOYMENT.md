# 🚀 Render.com'a Deployment Rehberi

Bu rehber, Telegram Tahmin Botunu Render.com'a deploy etmek için adım adım talimatlar içerir.

## 📋 Ön Gereksinimler

1. ✅ Render.com hesabı (Zaten var)
2. ✅ GitHub hesabı
3. ✅ Telegram Bot Token
4. ✅ API-Football Key

## 🔧 Adım 1: GitHub'a Yükleme

### 1.1 GitHub Repository Oluştur

1. GitHub'da yeni bir repository oluştur: `telegram-tahmin-bot`
2. Repository'yi **Private** yapabilirsiniz (güvenlik için önerilir)

### 1.2 Projeyi GitHub'a Push Et

Terminal'de şu komutları çalıştır:

```bash
cd "c:\Users\Mustafa\Desktop\TELEGRAM BOT VERSİYONLAR\TelegramTahminBot.v1"

# Git başlat (eğer yoksa)
git init

# Tüm dosyaları ekle
git add .

# Commit yap
git commit -m "Initial commit - Telegram Tahmin Bot"

# GitHub remote ekle (KENDI_KULLANICI_ADIN ile değiştir)
git remote add origin https://github.com/KENDI_KULLANICI_ADIN/telegram-tahmin-bot.git

# Push et
git branch -M main
git push -u origin main
```

## 🌐 Adım 2: Render.com'da Deployment

### 2.1 New Web Service Oluştur

1. Render Dashboard'a git: https://dashboard.render.com
2. **"New +"** butonuna tıkla
3. **"Background Worker"** seç (Bot için daha uygun)

### 2.2 Repository Bağla

1. **"Connect GitHub"** ile GitHub hesabını bağla
2. `telegram-tahmin-bot` repository'sini seç
3. **Connect** butonuna tıkla

### 2.3 Ayarları Yapılandır

**Temel Ayarlar:**
- **Name:** `telegram-tahmin-bot`
- **Region:** `Frankfurt (EU Central)` (En yakın bölge)
- **Branch:** `main`
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python main.py`

**Plan:**
- **Instance Type:** `Free`

### 2.4 Environment Variables Ekle

**"Environment"** sekmesinden şu değişkenleri ekle:

**ZORUNLU:**
```
TELEGRAM_BOT_TOKEN = <TELEGRAM_BOT_TOKEN_BURAYA>
```

**Opsiyonel (varsayılan değerler render.yaml'de var):**
```
API_FOOTBALL_KEY = 6336fb21e17dea87880d3b133132a13f
API_FOOTBALL_URL = https://v3.football.api-sports.io
DATABASE_URL = sqlite:///football_bot.db
FREE_PREDICTIONS_PER_DAY = 2
TIMEZONE = Europe/Istanbul
DAILY_PRICE = 50
WEEKLY_PRICE = 200
MONTHLY_PRICE = 500
```

**Stripe (ödeme sistemi için - opsiyonel):**
```
STRIPE_SECRET_KEY = <STRIPE_KEY_BURAYA>
STRIPE_PUBLISHABLE_KEY = <STRIPE_KEY_BURAYA>
```

**Admin Ayarları:**
```
ADMIN_IDS = <TELEGRAM_USER_ID_BURAYA>
```

> 💡 **Telegram User ID Nasıl Bulunur?**
> - [@userinfobot](https://t.me/userinfobot) botuna `/start` gönderin
> - Size ID'nizi gönderecektir

### 2.5 Deploy Et

1. **"Create Web Service"** (veya Background Worker) butonuna tıkla
2. Render otomatik olarak deploy işlemini başlatacak
3. Logları izle - yaklaşık 2-3 dakika sürer

## ✅ Adım 3: Doğrulama

### 3.1 Logları Kontrol Et

Render Dashboard'da **"Logs"** sekmesinden botun başladığını doğrula:

```
⚽ Telegram Futbol Tahmin Botu Başlatılıyor...
✅ Bot hazır!
Bot çalışıyor...
```

### 3.2 Telegram'da Test Et

1. Telegram'da botunuza gidin
2. `/start` komutunu gönderin
3. Bot yanıt veriyorsa başarılı! 🎉

## 🔄 Güncelleme Yapmak

Kod değişikliği yaptığınızda:

```bash
git add .
git commit -m "Açıklama"
git push
```

Render otomatik olarak yeni değişiklikleri deploy edecek.

## 🛠️ Sorun Giderme

### Bot çalışmıyor?

1. **Logs** sekmesini kontrol et
2. Environment variables doğru mu?
3. `TELEGRAM_BOT_TOKEN` eklenmiş mi?

### Database hatası?

SQLite dosya sistemi kullanır, Render'da her restart'ta sıfırlanır.
Kalıcı database için PostgreSQL kullanmanız önerilir:

1. Render'da **"New PostgreSQL"** oluştur
2. `DATABASE_URL`'i PostgreSQL connection string ile değiştir
3. `database.py`'de PostgreSQL adaptörü ekle

### Free tier sınırlamaları?

- ⚠️ Free plan 90 gün sonra otomatik kapanabilir
- ⚠️ İnaktif kalırsa spin down olabilir (ilk istek 30sn sürer)
- 💡 Cron job ile keep-alive yapabilirsiniz

## 📚 Faydalı Linkler

- [Render Documentation](https://render.com/docs)
- [Python on Render](https://render.com/docs/deploy-python)
- [Environment Variables](https://render.com/docs/environment-variables)

## 🎯 Sonraki Adımlar

1. ✅ PostgreSQL database ekle (kalıcılık için)
2. ✅ Custom domain ekle (opsiyonel)
3. ✅ Monitoring ve alerts kurulum
4. ✅ Backup stratejisi oluştur

---

**Destek için:** [Render Community](https://community.render.com/)
