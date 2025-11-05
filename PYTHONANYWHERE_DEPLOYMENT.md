# 🚀 PythonAnywhere Deployment Rehberi

Bu rehber, Telegram Tahmin Botunu PythonAnywhere'de ücretsiz olarak 7/24 çalıştırmak için adım adım talimatlar içerir.

## 🎯 PythonAnywhere Avantajları

✅ **Tamamen Ücretsiz**
✅ **7/24 Çalışır**
✅ **Kolay Kurulum**
✅ **SSH Erişimi**
✅ **3GB Disk**
✅ **Her gün otomatik restart**

## 📋 Gereksinimler

- ✅ PythonAnywhere hesabı (sivrii1940)
- ✅ GitHub repository (minigim1940/telegramtahminbotv1)
- ✅ Telegram Bot Token

---

## 🔧 ADIM 1: PythonAnywhere Console Aç

1. **PythonAnywhere Dashboard:** https://www.pythonanywhere.com/user/sivrii1940/
2. **"Consoles"** sekmesine git
3. **"Bash"** console başlat

---

## 🔧 ADIM 2: GitHub'dan Projeyi İndir

Bash console'da şu komutları çalıştır:

```bash
# Ana dizine git
cd ~

# Eski klasörü sil (varsa)
rm -rf telegramtahminbotv1

# GitHub'dan klonla
git clone https://github.com/minigim1940/telegramtahminbotv1.git

# Proje klasörüne gir
cd telegramtahminbotv1

# Dosyaları kontrol et
ls -la
```

---

## 🔧 ADIM 3: Python Sanal Ortam Oluştur

```bash
# Python 3.10 ile sanal ortam oluştur
mkvirtualenv --python=/usr/bin/python3.10 telegram-bot

# Sanal ortam otomatik aktifleşir
# Prompt başında (telegram-bot) görünecek
```

---

## 🔧 ADIM 4: Bağımlılıkları Yükle

```bash
# Sanal ortamda olduğunuzdan emin olun
workon telegram-bot

# Bağımlılıkları yükle
pip install -r requirements.txt

# Yükleme tamamlanana kadar bekleyin (2-3 dakika)
```

---

## 🔧 ADIM 5: .env Dosyası Oluştur

```bash
# .env.example'ı .env olarak kopyala
cp .env.example .env

# Nano editör ile .env dosyasını düzenle
nano .env
```

**Nano Editörde:**

1. `TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here` satırını bulun
2. `your_telegram_bot_token_here` yerine gerçek bot token'ınızı yazın:
   ```
   TELEGRAM_BOT_TOKEN=7968223220:AAGwfeTH6qa6OuCQChrqkUtDk0e29tW9x0M
   ```

3. İsterseniz `ADMIN_IDS` ekleyin (Telegram User ID'niz)
   ```
   ADMIN_IDS=YOUR_TELEGRAM_USER_ID
   ```

4. Kaydet ve çık:
   - `Ctrl + O` (kaydet)
   - `Enter` (onayla)
   - `Ctrl + X` (çık)

---

## 🔧 ADIM 6: Botu Test Et

```bash
# Botu manuel başlat
python main.py
```

**Başarılı olursa göreceksiniz:**
```
⚽ Telegram Futbol Tahmin Botu Başlatılıyor...
✅ Bot hazır!
Bot çalışıyor... Durdurmak için Ctrl+C basın
```

**Telegram'da test et:**
1. Botunuza `/start` gönderin
2. Yanıt veriyorsa başarılı! 🎉

**Durdurmak için:** `Ctrl + C`

---

## 🔧 ADIM 7: Always-On Task Oluştur (7/24 Çalıştırma)

PythonAnywhere **ücretsiz hesapta background task yok**, ama bazı alternatifler var:

### ✅ Seçenek 1: Scheduled Task (Önerilen)

1. **Dashboard** → **"Tasks"** sekmesine git
2. **"Scheduled tasks"** bölümüne inin
3. Şu komutu ekleyin:

```bash
cd /home/sivrii1940/telegramtahminbotv1 && /home/sivrii1940/.virtualenvs/telegram-bot/bin/python main.py
```

4. **Saat:** Her gün tekrar edilmesi için bir saat seçin (örn: 00:00)
5. **Create** tıklayın

⚠️ **Not:** Ücretsiz hesap her gün sadece 1 scheduled task çalıştırabilir.

### ✅ Seçenek 2: Console'da Manuel Başlatma

Console'da botu başlatıp açık tutun:

```bash
cd ~/telegramtahminbotv1
workon telegram-bot
python main.py &
```

⚠️ **Dikkat:** Console kapanırsa bot da durur.

### ✅ Seçenek 3: nohup ile Arka Planda Çalıştırma

```bash
cd ~/telegramtahminbotv1
workon telegram-bot
nohup python main.py > bot.log 2>&1 &
```

Bot'u kontrol et:
```bash
# Çalışıyor mu?
ps aux | grep main.py

# Log izle
tail -f ~/telegramtahminbotv1/bot.log
```

Bot'u durdur:
```bash
pkill -f "python main.py"
```

### 🌟 Seçenek 4: Paid Plan ($5/ay)

**"Always-On Tasks"** için PythonAnywhere Hacker plan'a yükseltme:
- ✅ Gerçek 7/24 background task
- ✅ Otomatik restart
- ✅ Daha fazla CPU/RAM

---

## 🔄 Bot'u Güncellemek

Kodu GitHub'da güncellediyseniz:

```bash
cd ~/telegramtahminbotv1

# Bot'u durdur (çalışıyorsa)
pkill -f "python main.py"

# Son değişiklikleri çek
git pull

# Sanal ortamı aktifleştir
workon telegram-bot

# Bağımlılıkları güncelle (gerekirse)
pip install -r requirements.txt

# Botu yeniden başlat
nohup python main.py > bot.log 2>&1 &
```

---

## 🛠️ Sorun Giderme

### Bot başlamıyor?

```bash
# Log dosyasını kontrol et
cat ~/telegramtahminbotv1/bot.log

# Veya canlı izle
tail -f ~/telegramtahminbotv1/bot.log
```

### Environment variable hatası?

```bash
# .env dosyasını kontrol et
cat ~/telegramtahminbotv1/.env

# Düzenle
nano ~/telegramtahminbotv1/.env
```

### Bağımlılık hatası?

```bash
workon telegram-bot
pip install --upgrade -r requirements.txt
```

### Bot'u tamamen sıfırla

```bash
# Bot'u durdur
pkill -f "python main.py"

# Sanal ortamı sil
rmvirtualenv telegram-bot

# Projeyi sil
rm -rf ~/telegramtahminbotv1

# Baştan başla (ADIM 2'den)
```

---

## 📊 Bot Durumunu Kontrol Et

```bash
# Bot çalışıyor mu?
ps aux | grep main.py

# Son 50 satır log
tail -n 50 ~/telegramtahminbotv1/bot.log

# Disk kullanımı
du -sh ~/telegramtahminbotv1

# Sanal ortamlar
workon
```

---

## 💡 İpuçları

1. **Console her 24 saatte kapanır** - Ücretsiz planda normal
2. **Scheduled task kullanın** - Her gün otomatik restart
3. **Log dosyalarını temizleyin** - Disk alanı için
4. **Database yedekleme** - Düzenli olarak SQLite dosyasını indirin

---

## 🎯 Hızlı Komutlar Özeti

```bash
# Bot başlat
cd ~/telegramtahminbotv1 && workon telegram-bot && python main.py

# Arka planda başlat
cd ~/telegramtahminbotv1 && workon telegram-bot && nohup python main.py > bot.log 2>&1 &

# Bot'u durdur
pkill -f "python main.py"

# Log izle
tail -f ~/telegramtahminbotv1/bot.log

# Güncelle
cd ~/telegramtahminbotv1 && git pull && workon telegram-bot && pip install -r requirements.txt
```

---

## 📚 Faydalı Linkler

- **Dashboard:** https://www.pythonanywhere.com/user/sivrii1940/
- **Help:** https://help.pythonanywhere.com/
- **Forums:** https://www.pythonanywhere.com/forums/

---

## 🚨 Önemli Notlar

⚠️ **Ücretsiz hesap sınırlamaları:**
- Console her 3 ayda bir sıfırlanır
- Günlük CPU sınırı var (100 saniye)
- Background task yok (Paid gerekli)

✅ **Çözüm:**
- Scheduled task kullanın (her gün restart)
- Veya $5/ay Hacker plan alın (önerilir bot'lar için)

---

**Bot'unuz başarıyla çalışıyor! 🎉**

Sorularınız için: https://help.pythonanywhere.com/
