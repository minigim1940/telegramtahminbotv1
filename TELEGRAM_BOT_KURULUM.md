# 🤖 TELEGRAM BOT KURULUM REHBERİ

## 📱 ADIM ADIM GÖRSEL KURULUM

---

## 1️⃣ TELEGRAM'I AÇIN

### Windows için:
- Başlat Menüsü → "Telegram" yazın ve açın
- VEYA: Web tarayıcınızdan https://web.telegram.org adresine gidin

### Telefon için:
- Telegram uygulamasını açın

---

## 2️⃣ BOTFATHER'I BULUN

### Arama Yapın:
1. Telegram'ın üst kısmındaki **arama kutusuna** tıklayın
2. **`@BotFather`** yazın (@ işaretini unutmayın!)
3. **Mavi onay tiki olan** resmi BotFather'ı seçin

```
┌─────────────────────────────────┐
│  🔍 Ara...                      │
│                                 │
│  @BotFather                     │
└─────────────────────────────────┘
```

### Doğru BotFather:
- ✅ İsmi: **BotFather**
- ✅ Kullanıcı adı: **@BotFather**
- ✅ Mavi onay işareti var ✓
- ✅ Açıklama: "The one and only official Telegram Bot Father"

### ⚠️ DİKKAT! Sahte botlara kanmayın:
- ❌ @BotFatherBot
- ❌ @BotFather_bot
- ❌ Mavi tik olmayanlar

---

## 3️⃣ BOTFATHER İLE SOHBETE BAŞLAYIN

### İlk Mesaj:
1. BotFather sohbetini açın
2. Alt kısımda **"START"** veya **"BAŞLAT"** butonuna tıklayın
3. VEYA: `/start` yazıp Enter'a basın

### BotFather'ın Karşılama Mesajı:
```
I can help you create and manage Telegram bots. 
If you're new to the Bot API, please see the 
manual (https://core.telegram.org/bots).

You can control me by sending these commands:

/newbot - create a new bot
/mybots - edit your bots
...
```

---

## 4️⃣ YENİ BOT OLUŞTURUN

### Komut Gönderin:
1. Mesaj kutusuna **`/newbot`** yazın
2. **Enter** veya **Gönder** butonuna basın

```
┌─────────────────────────────────┐
│  Siz:                           │
│  /newbot                        │
└─────────────────────────────────┘
```

### BotFather'ın Cevabı:
```
Alright, a new bot. How are we going to call it? 
Please choose a name for your bot.
```

**Türkçe çevirisi:**
"Tamam, yeni bir bot. Ona ne ad vereceğiz? 
Botunuz için bir isim seçin."

---

## 5️⃣ BOT İSMİNİ BELİRLEYİN

### İsim Önerileri:
- ⚽ **Futbol Tahmin Botu**
- 🎯 **Tahmin Asistanı**
- 📊 **Maç Analiz Botu**
- 🏆 **Futbol Tahmin Uzmanı**

### Örnek:
```
┌─────────────────────────────────┐
│  Siz:                           │
│  Futbol Tahmin Botu             │
└─────────────────────────────────┘
```

### BotFather'ın Cevabı:
```
Good. Now let's choose a username for your bot. 
It must end in `bot`. Like this, for example: 
TetrisBot or tetris_bot.
```

**Türkçe çevirisi:**
"Güzel. Şimdi botunuz için bir kullanıcı adı 
seçelim. 'bot' ile bitmelidir. Örneğin: 
TetrisBot veya tetris_bot."

---

## 6️⃣ KULLANICI ADI BELİRLEYİN

### ⚠️ ÖNEMLİ KURALLAR:
- ✅ **'bot'** ile BİTMELİ
- ✅ Küçük harf kullanın
- ✅ Sayı ve alt tire (_) kullanılabilir
- ❌ Boşluk KULLANILAMAZ
- ❌ Türkçe karakter KULLANILAMAZ
- ❌ Başka biri tarafından kullanılmamış olmalı

### ✅ DOĞRU Örnekler:
- `futbol_tahmin_bot`
- `futboltahminbot`
- `tahmin2024_bot`
- `futbol_predict_bot`
- `matchpredict_bot`

### ❌ YANLIŞ Örnekler:
- `futbol tahmin` (boşluk var, bot ile bitmiyor)
- `futboltahmin` ('bot' ile bitmiyor)
- `futbol_bot.` (nokta kullanılamaz)
- `futbol-bot` (tire yerine alt tire kullanın)

### Örnek Giriş:
```
┌─────────────────────────────────┐
│  Siz:                           │
│  futbol_tahmin_2024_bot         │
└─────────────────────────────────┘
```

---

## 7️⃣ TOKEN'I ALIN! (ÇOK ÖNEMLİ!)

### ✅ BAŞARILI OLURSA:

BotFather size şöyle bir mesaj gönderecek:

```
Done! Congratulations on your new bot. 
You will find it at t.me/futbol_tahmin_2024_bot. 
You can now add a description, about section and 
profile picture for your bot, see /help for a 
list of commands.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567

For a description of the Bot API, see this page: 
https://core.telegram.org/bots/api

Keep your token secure and store it safely, it 
can be used by anyone to control your bot.
```

### 🔑 TOKEN BURASI:
```
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567
          ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
        BU KISMI KOPYALAYIN!
```

### Token Nasıl Kopyalanır:

#### Bilgisayarda:
1. Token metninin üzerine **3 kez** tıklayın (tümünü seçer)
2. VEYA: Fareyle sürükleyerek seçin
3. **Ctrl + C** (kopyala)
4. Bir yere yapıştırın: **Ctrl + V**

#### Telefonda:
1. Token metnine **uzun basın**
2. "Kopyala" seçeneğine tıklayın
3. Not defterine yapıştırın

### ⚠️ ÇOK ÖNEMLİ!
- 🔒 Bu token'ı **KİMSEYLE PAYLAŞMAYIN!**
- 🔒 Token ile **botunuzu kontrol edebilirler!**
- 🔒 Güvenli bir yerde **saklayın!**
- 🔒 GitHub'a **yüklemeyİn!**

---

## 8️⃣ TELEGRAM ID'NİZİ ÖĞRENİN (Admin için)

### @userinfobot Kullanın:

1. Telegram arama kutusuna **`@userinfobot`** yazın
2. Botu bulun ve sohbeti açın
3. **"START"** butonuna tıklayın VEYA `/start` yazın

### Bot Size Şunu Gönderecek:
```
Id: 987654321
First: Mustafa
Username: @mustafa_kullanici
Language: tr
```

### 🔑 ID'NİZİ KOPYALAYIN:
```
Id: 987654321
    ↑↑↑↑↑↑↑↑↑
  BU SAYI TELEGRAM ID'NİZ
```

- Bu numara sizin benzersiz Telegram ID'niz
- Admin olarak kendinizi eklemek için lazım

---

## 9️⃣ .ENV DOSYASINI DÜZENLEYİN

### Dosyayı Açın:
1. **Masaüstü** → **TelegramTahminBot** klasörü
2. **`.env`** dosyasını bulun
3. **Sağ tık** → **Birlikte aç** → **Not Defteri**

### Düzenleyin:

#### ÖNCE (Örnek değerler):
```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Admin User IDs (comma-separated Telegram user IDs)
ADMIN_IDS=123456789,987654321
```

#### SONRA (Gerçek değerler):
```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz-1234567

# Admin User IDs (comma-separated Telegram user IDs)
ADMIN_IDS=987654321
```

**Değiştirdiğiniz satırlar:**
1. `TELEGRAM_BOT_TOKEN=` → Token'ınızı yapıştırın
2. `ADMIN_IDS=` → Telegram ID'nizi yazın

### Kaydedin:
- **Ctrl + S** (kaydet)
- Dosyayı kapatın

---

## 🔟 BOTUNUZU TEST EDİN (Henüz Çalıştırmadan)

### Botunuzu Telegram'da Bulun:
1. Telegram arama kutusuna botunuzun kullanıcı adını yazın
   - Örnek: `@futbol_tahmin_2024_bot`
2. Botu bulun ve tıklayın
3. **"START"** butonuna tıklayın

### Ne Göreceksiniz:
- Henüz bot çalışmıyor, cevap vermeyecek
- Bu normal! 
- Bot kodunu çalıştırdıktan sonra çalışacak

---

## 1️⃣1️⃣ BOTU ÇALIŞTIRIN

### CMD Açın:
1. **Windows tuşuna** basın
2. **`cmd`** yazın
3. **Enter**

### Komutları Çalıştırın:
```bash
# Klasöre gidin
cd C:\Users\Mustafa\Desktop\TelegramTahminBot

# Kontrolü çalıştırın (opsiyonel)
python kontrol.py

# Botu başlatın
python main.py
```

### Başarılı Görünüm:
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

## 1️⃣2️⃣ TELEGRAM'DA TEST EDİN

### Botunuza Mesaj Gönderin:
1. Telegram'da botunuzu açın
2. **`/start`** yazın
3. Bot size karşılama mesajı göndermeli! 🎉

### Göreceğiniz Mesaj:
```
🎯 Futbol Tahmin Botuna Hoş Geldiniz! ⚽

Merhaba Mustafa! 

Bu bot, gelişmiş AI algoritmaları ve gerçek 
zamanlı istatistiklerle futbol maçları için 
profesyonel tahminler sunar.

📊 Özellikler:
✅ Canlı maç tahminleri
✅ Detaylı istatistiksel analiz
...
```

### Tahmin Almayı Deneyin:
1. **"⚽ Tahmin Al"** butonuna tıklayın
2. VEYA: `/tahmin` yazın
3. Bugünün maçlarını görün
4. Bir maçı seçin ve tahmin alın! 🎯

---

## ✅ KONTROL LİSTESİ

Kurulumu doğru yaptınız mı?

- [ ] @BotFather ile bot oluşturdunuz
- [ ] Bot ismi ve kullanıcı adı belirlediniz
- [ ] TOKEN'ı kopyaladınız
- [ ] @userinfobot ile ID'nizi öğrendiniz
- [ ] `.env` dosyasını düzenlediniz
- [ ] TOKEN'ı `.env` dosyasına yapıştırdınız
- [ ] Admin ID'nizi `.env` dosyasına yazdınız
- [ ] Dosyayı kaydettiniz (Ctrl+S)
- [ ] `python main.py` ile botu başlattınız
- [ ] Telegram'da `/start` ile test ettiniz
- [ ] Bot cevap verdi ✅

---

## ❌ SORUN GİDERME

### "Username is already taken" Hatası:
**Sorun:** Kullanıcı adı başkası tarafından kullanılıyor
**Çözüm:** Farklı bir kullanıcı adı deneyin
- `futbol_tahmin_2024_bot`
- `tahmin_botu_2024`
- `match_predict_tr_bot`

### Bot Cevap Vermiyor:
**Kontrol edin:**
1. `python main.py` çalışıyor mu? (CMD'de)
2. `.env` dosyasındaki token doğru mu?
3. Token'da boşluk var mı? (olmamalı!)
4. Hata mesajı var mı? (`bot.log` dosyasına bakın)

### "Unauthorized" Hatası:
**Sorun:** Token yanlış veya geçersiz
**Çözüm:** 
1. BotFather'dan yeni token alın: `/token` komutu
2. Yeni token'ı `.env` dosyasına yapıştırın
3. Botu yeniden başlatın

### Token Nerede Görünüyor?
**BotFather'da:**
- Botunuzun sohbetine gidin
- `/mybots` yazın
- Botunuzu seçin
- "API Token" → Token'ınızı görürsünüz

---

## 🎓 İPUÇLARI

### Token Güvenliği:
- 🔒 Token'ı **kimseyle paylaşmayın**
- 🔒 GitHub'a **yüklemeyİn**
- 🔒 Ekran görüntüsü alırken **gizleyin**
- 🔒 Şüphelenirseniz **yeni token alın** (`/revoke` komutu)

### Bot Profili Düzenleme:
```
/setdescription → Açıklama ekleyin
/setabouttext → Hakkında metni
/setuserpic → Profil fotoğrafı
/setcommands → Komut listesi
```

### Örnek Bot Tanımı:
```
⚽ Futbol Tahmin Botu

Gelişmiş AI ile futbol maç tahminleri!
📊 Detaylı analiz | 🎯 Yüksek doğruluk
💎 Premium üyelik mevcut

Komutlar:
/tahmin - Maç tahmini al
/bugun - Bugünün maçları
/premium - Premium paketler
```

---

## 📸 EKRAN GÖRÜNTÜLERİ İLE ÖZET

### 1. BotFather Ara:
```
┌────────────────────────┐
│ 🔍 @BotFather         │
│                        │
│ ✓ BotFather            │
│   The one and only...  │
└────────────────────────┘
```

### 2. /newbot Komutu:
```
┌────────────────────────┐
│ Siz: /newbot          │
│                        │
│ BotFather:            │
│ Alright, a new bot... │
└────────────────────────┘
```

### 3. İsim Girin:
```
┌────────────────────────┐
│ Siz:                   │
│ Futbol Tahmin Botu    │
└────────────────────────┘
```

### 4. Kullanıcı Adı Girin:
```
┌────────────────────────┐
│ Siz:                   │
│ futbol_tahmin_2024_bot│
└────────────────────────┘
```

### 5. Token'ı Kopyalayın:
```
┌────────────────────────┐
│ BotFather:            │
│ Use this token:       │
│ 1234567890:ABCdef...  │
│ ↑ BURAYI KOPYALA!     │
└────────────────────────┘
```

---

## 🎯 ÖZET

### Yapmanız Gerekenler:
1. ✅ @BotFather → /newbot
2. ✅ İsim gir → Kullanıcı adı gir
3. ✅ TOKEN'ı kopyala
4. ✅ @userinfobot → ID'ni öğren
5. ✅ .env dosyasını düzenle
6. ✅ python main.py çalıştır
7. ✅ Telegram'da test et

**Toplam Süre: 3-5 Dakika**

---

## 🎉 TEBRİKLER!

Artık kendi Telegram botunuz var! 🤖

**Sonraki Adımlar:**
- Bot profil fotoğrafı ekleyin
- Açıklama yazın
- Arkadaşlarınızla paylaşın
- Premium özellikleri aktifleştirin

**İyi tahminler! ⚽🎯**
