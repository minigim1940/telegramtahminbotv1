# 🚀 HIZLI BAŞLANGIÇ - PythonAnywhere

## ⚡ 5 Dakikada Bot Çalıştır

### 1️⃣ Console Aç
https://www.pythonanywhere.com/user/sivrii1940/ → **Consoles** → **Bash**

### 2️⃣ Bu Komutları Kopyala-Yapıştır

```bash
# Projeyi indir
cd ~
rm -rf telegramtahminbotv1
git clone https://github.com/minigim1940/telegramtahminbotv1.git
cd telegramtahminbotv1

# Python ortamı oluştur
mkvirtualenv --python=/usr/bin/python3.10 telegram-bot

# Bağımlılıkları yükle
pip install -r requirements.txt

# .env dosyası oluştur
cp .env.example .env
nano .env
```

### 3️⃣ .env Dosyasını Düzenle

Nano editörde (açılacak):

1. `TELEGRAM_BOT_TOKEN=` satırını bul
2. Token'ınızı yapıştır: `7968223220:AAGwfeTH6qa6OuCQChrqkUtDk0e29tW9x0M`
3. `Ctrl+O` → `Enter` → `Ctrl+X` (kaydet ve çık)

### 4️⃣ Botu Başlat

```bash
python main.py
```

✅ `Bot çalışıyor...` mesajını görünce başarılı!

### 5️⃣ Telegram'da Test Et

Botunuza `/start` gönderin 🎉

---

## 🔄 7/24 Çalıştırma (Arka Planda)

Bot'u durdurun (`Ctrl+C`) sonra:

```bash
nohup python main.py > bot.log 2>&1 &
```

**Console kapansa bile bot çalışmaya devam eder!**

### Bot Kontrol

```bash
# Çalışıyor mu?
ps aux | grep main.py

# Log izle
tail -f bot.log

# Durdur
pkill -f "python main.py"
```

---

## ⚙️ Alternatif: Scheduled Task (Her gün otomatik başlat)

PythonAnywhere Dashboard → **Tasks** sekmesi

**Komut:**
```bash
cd /home/sivrii1940/telegramtahminbotv1 && /home/sivrii1940/.virtualenvs/telegram-bot/bin/python main.py
```

**Saat:** 00:00 (Her gün gece yarısı restart)

---

## 🔄 Güncelleme

```bash
cd ~/telegramtahminbotv1
pkill -f "python main.py"  # Bot'u durdur
git pull  # Güncellemeleri çek
workon telegram-bot
pip install -r requirements.txt
nohup python main.py > bot.log 2>&1 &  # Yeniden başlat
```

---

## 🆘 Sorun mu var?

Detaylı rehber: **PYTHONANYWHERE_DEPLOYMENT.md**

---

**Hazır! Bot'unuz çalışıyor! 🚀**
