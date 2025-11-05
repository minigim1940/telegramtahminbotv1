# 📋 SİZİN YAPMANIZ GEREKENLER

## ✅ TAMAMLANAN İŞLER (Otomatik Yapıldı)

✓ Tüm kod dosyaları oluşturuldu
✓ Python kütüphaneleri yüklendi
✓ Veritabanı oluşturuldu
✓ API-Football entegrasyonu test edildi ✅ ÇALIŞIYOR!
✓ .env dosyası oluşturuldu
✓ API key ayarlandı (6336fb21e17dea87880d3b133132a13f)

---

## 🎯 ŞİMDİ YAPMANIZ GEREKENLER

### 1️⃣ TELEGRAM BOT OLUŞTURUN (5 dakika)

**Adım 1:** Telegram'ı açın

**Adım 2:** @BotFather ile konuşun
- Telegram arama kutusuna `@BotFather` yazın
- Bota tıklayın ve sohbeti başlatın

**Adım 3:** Yeni bot oluşturun
```
Siz yazın: /newbot
BotFather: Alright, a new bot. How are we going to call it?

Siz yazın: Futbol Tahmin Bot
(veya istediğiniz bir isim)

BotFather: Good. Now let's choose a username for your bot.

Siz yazın: futbol_tahmin_2024_bot
(veya başka bir username - sonunda 'bot' olmalı)
```

**Adım 4:** Token'ı kopyalayın
BotFather size böyle bir mesaj gönderecek:
```
Done! Congratulations on your new bot. You will find it at 
t.me/futbol_tahmin_2024_bot. You can now add a description...

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567

For a description of the Bot API, see this page: 
https://core.telegram.org/bots/api
```

**ÖNEMLİ:** `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567` 
gibi görünen TOKEN'ı kopyalayın!

---

### 2️⃣ TELEGRAM ID'NİZİ ÖĞRENİN (1 dakika)

**Adım 1:** @userinfobot ile konuşun
- Telegram'da `@userinfobot` arayın
- Bota `/start` yazın

**Adım 2:** ID'nizi kopyalayın
Bot size böyle bir mesaj gönderecek:
```
Id: 123456789
First: Mustafa
Username: @mustafa
Language: tr
```

**ÖNEMLİ:** `Id: 123456789` kısmındaki SAYIYI kopyalayın!

---

### 3️⃣ .ENV DOSYASINI DÜZENLEYİN (2 dakika)

**Adım 1:** `.env` dosyasını açın
- Masaüstünde TelegramTahminBot klasörüne gidin
- `.env` dosyasına sağ tıklayın
- "Birlikte aç" → "Not Defteri" seçin

**Adım 2:** Şu satırı bulun:
```
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

**Adım 3:** `your_telegram_bot_token_here` yerine BotFather'dan 
aldığınız TOKEN'ı yapıştırın:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567
```

**Adım 4:** Şu satırı bulun:
```
ADMIN_IDS=123456789,987654321
```

**Adım 5:** `123456789` yerine kendi Telegram ID'nizi yazın:
```
ADMIN_IDS=987654321
```
(Birden fazla admin varsa virgülle ayırın: `987654321,123456789`)

**Adım 6:** Dosyayı kaydedin (Ctrl+S) ve kapatın

---

### 4️⃣ BOTU ÇALIŞTIRIN (1 dakika)

**Adım 1:** Komut İstemi'ni açın (CMD)
- Windows tuşuna basın
- `cmd` yazın
- Enter'a basın

**Adım 2:** Klasöre gidin:
```
cd C:\Users\Mustafa\Desktop\TelegramTahminBot
```

**Adım 3:** Botu başlatın:
```
python main.py
```

**Başarılı olursa göreceğiniz ekran:**
```
============================================================
⚽ Telegram Futbol Tahmin Botu Başlatılıyor...
============================================================
📊 Veritabanı başlatılıyor...
🤖 Bot oluşturuluyor...
🔐 Admin paneli yapılandırılıyor...
✅ Bot hazır!
============================================================
Bot çalışıyor... Durdurmak için Ctrl+C basın
============================================================
```

---

### 5️⃣ BOTU TEST EDİN (2 dakika)

**Adım 1:** Telegram'da botunuzu bulun
- Arama kutusuna bot username'inizi yazın
  (örn: `@futbol_tahmin_2024_bot`)

**Adım 2:** Bota `/start` yazın

**Adım 3:** Karşılama mesajını görmelisiniz! 🎉

**Adım 4:** "⚽ Tahmin Al" butonuna tıklayın

**Adım 5:** Bugünün maçlarını görün ve bir tanesini seçin!

---

## 🎯 KULLANIM

### Kullanıcı Komutları:
- `/start` - Botu başlat
- `/tahmin` - Maç tahmini al
- `/bugun` - Bugünün maçları
- `/premium` - Premium paketler (DEMO MODDA ÜCRETSİZ!)
- `/istatistik` - İstatistikleriniz

### Admin Komutları (Sizin için):
- `/adminstats` - Bot istatistikleri
- `/givepremium 123456789 monthly` - Birine premium ver
- `/broadcast Merhaba herkese!` - Toplu duyuru
- `/revenue` - Gelir raporu
- `/premiumlist` - Premium kullanıcılar

---

## 💎 DEMO MOD NEDİR?

Stripe ödeme sistemi kurulmadığı için bot **DEMO MODDA** çalışır:

✅ Kullanıcılar "Premium Al" dediğinde otomatik aktive olur
✅ Gerçek ödeme gerekmez
✅ Tüm premium özellikler çalışır
✅ Test için mükemmeldir!

**Gerçek ödeme almak isterseniz:**
- Stripe hesabı açın (https://stripe.com)
- API key'lerinizi `.env` dosyasına ekleyin

---

## ❌ SORUN GİDERME

### "ModuleNotFoundError" hatası alıyorsanız:
```
pip install -r requirements.txt
```

### Bot başlamıyorsa:
1. `.env` dosyasında TELEGRAM_BOT_TOKEN'ın doğru olduğundan emin olun
2. Token'da boşluk olmamalı
3. Token BotFather'dan yeni alınmış olmalı

### "Unauthorized" hatası alıyorsanız:
- Bot token'ınız yanlış
- BotFather'dan yeni token alın
- `.env` dosyasına doğru yapıştırın

### Tahmin alamıyorsanız:
- İnternete bağlı olduğunuzdan emin olun
- `/bugun` yazarak bugün maç olup olmadığını kontrol edin
- `python test_api.py` ile API'yi test edin

---

## 📞 YARDIM

Sorun yaşarsanız:
1. `bot.log` dosyasını kontrol edin (hata mesajları orada)
2. Komutu tekrar çalıştırın
3. Botu durdurup yeniden başlatın (Ctrl+C sonra `python main.py`)

---

## 🎉 HAZIRSINIZ!

Artık her şey hazır! Sadece:
1. Telegram bot oluşturun
2. .env dosyasını düzenleyin  
3. `python main.py` ile başlatın

**İyi tahminler! ⚽🎯**
