# 🚀 Hızlı Başlangıç - Render.com Deploy

## ⚡ En Hızlı Yol (3 Adım)

### 1️⃣ GitHub'a Yükle

```bash
# Terminalde çalıştır:
cd "c:\Users\Mustafa\Desktop\TELEGRAM BOT VERSİYONLAR\TelegramTahminBot.v1"

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADIN/telegram-tahmin-bot.git
git push -u origin main
```

**VEYA** Windows için:
```bash
# deploy_to_github.bat dosyasını çift tıkla
# Talimatları takip et
```

### 2️⃣ Render'da Background Worker Oluştur

1. **Render Dashboard:** https://dashboard.render.com
2. **New +** → **Background Worker**
3. Repository'yi bağla: `telegram-tahmin-bot`
4. Ayarlar:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`

### 3️⃣ Environment Variables Ekle

**ZORUNLU:**
```
TELEGRAM_BOT_TOKEN = <bot_token_buraya>
```

**Opsiyonel:**
```
ADMIN_IDS = <telegram_user_id>
STRIPE_SECRET_KEY = <stripe_key>
```

### ✅ Deploy Et!

**Create Background Worker** butonuna tıkla.

2-3 dakika sonra botunuz 7/24 çalışacak! 🎉

---

## 📱 Telegram User ID Nasıl Bulunur?

1. Telegram'da [@userinfobot](https://t.me/userinfobot) ara
2. `/start` gönder
3. ID'ni kopyala

## 🔧 Sorun mu yaşıyorsun?

Detaylı talimatlar: **RENDER_DEPLOYMENT.md**

## 💾 Veritabanı Önemli!

⚠️ **SQLite her restart'ta sıfırlanır!**

Kalıcı database için Render'da **PostgreSQL** ekle (ücretsiz).

---

**Sorular?** RENDER_DEPLOYMENT.md dosyasına bakın.
