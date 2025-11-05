# 🤖 TELEGRAM BOT AYARLARI (BotFather)

## 📋 HIZLI KURULUM

Telegram'da **@BotFather** ile konuşarak aşağıdaki ayarları yapın:

---

## 1️⃣ BOT AÇIKLAMASI (Description)

BotFather'da şu komutu kullanın:
```
/setdescription
```

Sonra botunuzu seçin ve aşağıdaki metni yapıştırın:

```
⚽ Profesyonel Futbol Tahmin Botu

🎯 Yapay Zeka Destekli Maç Analizleri
📊 Detaylı İstatistikler ve Olasılıklar
💰 Bahis Oranları ve Gerçek Olasılıklar
🏆 Tüm Dünya Liglerinden Maçlar

Güvenilir tahminler için başlat!
```

---

## 2️⃣ KISA AÇIKLAMA (About)

BotFather'da şu komutu kullanın:
```
/setabouttext
```

Sonra botunuzu seçin ve aşağıdaki metni yapıştırın:

```
⚽ Yapay zeka ile futbol maçı tahminleri
📊 Detaylı analizler, istatistikler ve bahis oranları
```

---

## 3️⃣ BOT KOMUTLARI (Commands)

BotFather'da şu komutu kullanın:
```
/setcommands
```

Sonra botunuzu seçin ve aşağıdaki komutları **TAM OLARAK** yapıştırın:

```
start - 🏠 Botu başlat ve ana menüyü aç
bugun - 📅 Bugünün maçlarını göster
yarin - 🔜 Yarının maçlarını göster
dun - 📊 Dünkü tahminlerin sonuçları
ligler - 🏆 Popüler ligleri listele
premium - 💎 Premium üyelik bilgileri
yardim - ℹ️ Yardım ve kullanım kılavuzu
iletisim - 📞 Destek ve iletişim
```

**NOT:** Her satır `komut - açıklama` formatında olmalı (tire ve boşluk önemli!)

---

## 4️⃣ BOT PROFİL FOTOĞRAFI

BotFather'da şu komutu kullanın:
```
/setuserpic
```

Sonra:
1. Botunuzu seçin
2. Futbol temalı profesyonel bir logo yükleyin
   - Önerilen boyut: 512x512 px
   - Format: PNG veya JPG
   - Tema: Futbol topu, istatistik grafikleri, AI sembolü

---

## 5️⃣ INLINE MODE (Opsiyonel)

BotFather'da şu komutu kullanın:
```
/setinline
```

Botunuzu seçin ve bu metni yazın:
```
Maç ara ve tahmin al...
```

---

## 6️⃣ GRUP YETKİLERİ

### Grup Yönetim İzinleri
BotFather'da:
```
/setjoingroups
```
Seçin: **Enable** (Botu gruplara eklenebilir yap)

### Grup Gizliliği
```
/setprivacy
```
Seçin: **Disable** (Botun tüm mesajları görmesi için gerekli)

---

## 7️⃣ MENU BUTTON (Menü Butonu)

BotFather'da şu komutu kullanın:
```
/setmenubutton
```

Sonra:
1. Botunuzu seçin
2. Buton metni: `📊 Maçlar`
3. URL: Bot username'iniz (örn: `https://t.me/futbol_tahmin_bot`)

---

## 8️⃣ BUSINESS MODE

BotFather'da:
```
/setbusiness
```
Seçin: **Enable** (İş hesapları için destek)

---

## 9️⃣ DOMAIN (Opsiyonel)

Eğer web siteniz varsa:
```
/setdomain
```
Domain adınızı girin (örn: `tahminbot.com`)

---

## 🎨 GÖRSEL ÖNERİLER

### Profil Fotoğrafı İçin Fikirler:
- ⚽ Futbol topu + AI chip sembolü
- 📊 Grafik çizgileri ile futbol sahası
- 🎯 Hedef tahtası + futbol elementi
- 🤖 Robot yüzü futbol teması ile

### Renk Paleti:
- Ana renk: Yeşil (futbol sahası) #2ECC71
- İkincil: Mavi (güven) #3498DB
- Vurgu: Altın (premium) #F39C12

---

## ✅ KONTROL LİSTESİ

Tüm ayarları yaptıktan sonra kontrol edin:

- [ ] Description (Uzun açıklama) ayarlandı
- [ ] About (Kısa açıklama) ayarlandı
- [ ] Commands (Komutlar) eklendi
- [ ] Profile picture (Profil fotoğrafı) yüklendi
- [ ] Inline mode etkinleştirildi
- [ ] Join groups izni verildi
- [ ] Privacy mode ayarlandı
- [ ] Menu button eklendi

---

## 📱 TEST

Ayarları test etmek için:

1. Telegram'da botunuzu arayın
2. Bot profilini açın - açıklama görünmeli
3. `/start` yazın - komutlar listesi görünmeli
4. Menu butonuna tıklayın - çalışıyor mu?

---

## 🔧 EK AYARLAR

### Bot Token'ı Yenile (Güvenlik)
```
/revoke
```
**UYARI:** Mevcut token geçersiz olur, .env dosyasını güncelleyin!

### Bot İstatistikleri
```
/stats
```
Botunuzun kullanım istatistiklerini gösterir

### Bot Bilgileri
```
/mybots
```
Tüm botlarınızı ve ayarlarını listeler

---

## 📞 YARDIM

Sorun yaşarsanız:
- BotFather'da `/help` yazın
- Telegram Bot API Docs: https://core.telegram.org/bots

---

**SON GÜNCELLEME:** 6 Kasım 2025
**BOT VERSİYON:** 1.0
