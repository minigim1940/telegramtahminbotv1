# 📦 PROJE DOSYALARI VE AÇIKLAMALAR

## 🎯 ANA DOSYALAR

### 📱 Bot Dosyaları
| Dosya | Ne İşe Yarar? | Değiştirilmeli mi? |
|-------|---------------|-------------------|
| `bot.py` | Telegram bot arayüzü, komutlar | ❌ Hayır |
| `api_football.py` | API-Football veri çekme | ❌ Hayır |
| `prediction_engine.py` | Tahmin algoritması | ⚙️ Ağırlıklar değiştirilebilir |
| `database.py` | Veritabanı işlemleri | ❌ Hayır |
| `payment_handler.py` | Ödeme sistemi | ⚙️ Stripe key eklenebilir |
| `admin_panel.py` | Admin komutları | ❌ Hayır |
| `utils.py` | Yardımcı fonksiyonlar | ❌ Hayır |

### ⚙️ Yapılandırma Dosyaları
| Dosya | Ne İşe Yarar? | Değiştirilmeli mi? |
|-------|---------------|-------------------|
| `.env` | Gizli ayarlar (TOKEN, API KEY) | ✅ EVET! |
| `.env.example` | Örnek ayarlar | ❌ Hayır |
| `requirements.txt` | Python kütüphaneleri | ❌ Hayır |
| `.gitignore` | Git hariç tutma | ❌ Hayır |

### 🚀 Çalıştırma Dosyaları
| Dosya | Ne İşe Yarar? | Ne Zaman Kullanılır? |
|-------|---------------|---------------------|
| `main.py` | Bot başlatma | Her zaman bu ile başlat |
| `setup.py` | İlk kurulum | Sadece ilk kurulumda |
| `test_api.py` | API testi | Sorun olduğunda test et |

### 📚 Dokümantasyon
| Dosya | İçerik |
|-------|--------|
| `BASLAT.md` | ⚡ Hızlı başlangıç (5 dakika) |
| `YAPILACAKLAR.md` | 📋 Sizin yapacaklarınız |
| `QUICKSTART.md` | 🚀 Detaylı kurulum |
| `README.md` | 📖 Tam dokümantasyon |

### 🗄️ Veritabanı
| Dosya | Ne İşe Yarar? |
|-------|---------------|
| `football_bot.db` | SQLite veritabanı (otomatik oluşturuldu) |

---

## 🔧 AYARLANMASI GEREKENLER

### ✅ .ENV DOSYASI (MUTLAKA!)

Şu 2 satırı değiştirmelisiniz:

```env
# 1. BotFather'dan alacağınız token
TELEGRAM_BOT_TOKEN=buraya_token_gelecek

# 2. Kendi Telegram ID'niz
ADMIN_IDS=buraya_id_gelecek
```

**Diğer satırlar:**
- ✅ `API_FOOTBALL_KEY` → Zaten ayarlı (6336fb21e17dea87880d3b133132a13f)
- ⚙️ `STRIPE_SECRET_KEY` → Opsiyonel (demo modda çalışır)
- ⚙️ Fiyatlar → İsterseniz değiştirin (DAILY_PRICE, WEEKLY_PRICE, MONTHLY_PRICE)

---

## 📂 KLASÖR YAPISI

```
TelegramTahminBot/
│
├── 📱 BOT KOD DOSYALARI
│   ├── bot.py                 (Ana bot)
│   ├── api_football.py        (API entegrasyonu)
│   ├── prediction_engine.py   (Tahmin motoru)
│   ├── database.py            (Veritabanı)
│   ├── payment_handler.py     (Ödeme)
│   ├── admin_panel.py         (Admin paneli)
│   └── utils.py               (Yardımcılar)
│
├── ⚙️ YAPILANDIRMA
│   ├── .env                   (GİZLİ AYARLAR - DEĞİŞTİR!)
│   ├── .env.example           (Örnek)
│   ├── requirements.txt       (Kütüphaneler)
│   └── .gitignore            (Git)
│
├── 🚀 ÇALIŞTIRMA
│   ├── main.py               (Bot başlat)
│   ├── setup.py              (Kurulum)
│   └── test_api.py           (Test)
│
├── 📚 DOKÜMANTASYON
│   ├── BASLAT.md             (5 dakikalık kılavuz)
│   ├── YAPILACAKLAR.md       (Yapılacaklar listesi)
│   ├── QUICKSTART.md         (Hızlı başlangıç)
│   └── README.md             (Tam dokümantasyon)
│
└── 🗄️ VERİTABANI
    └── football_bot.db       (SQLite)
```

---

## 🎯 HANGİ DOSYAYI NE ZAMAN OKUMALI?

### İlk Kurulum:
1. 📖 `BASLAT.md` → En hızlı başlangıç (5 dakika)
2. 📋 `YAPILACAKLAR.md` → Detaylı adımlar

### Sorun Yaşıyorsanız:
1. 📖 `README.md` → Sorun giderme bölümü
2. 🔍 `bot.log` → Hata logları

### Özelleştirme:
1. 📖 `README.md` → Özelleştirme bölümü
2. ⚙️ `.env` → Ayarlar
3. 🔧 `prediction_engine.py` → Tahmin ağırlıkları

---

## 🔄 GÜNCELLEME VE YEDEKLEMe

### Yedeklenmesi Gerekenler:
✅ `.env` → Gizli ayarlarınız
✅ `football_bot.db` → Kullanıcı verileri

### Yedeklenmesine Gerek Yok:
❌ Python dosyaları (tekrar oluşturulabilir)
❌ `__pycache__/` (otomatik oluşur)

---

## 📊 VERİTABANI TABLOLARI

`football_bot.db` dosyasında:

1. **users** → Kullanıcı bilgileri
2. **subscriptions** → Premium abonelikler
3. **prediction_logs** → Tahmin geçmişi
4. **match_cache** → API önbelleği
5. **admin_logs** → Admin işlemleri

---

## 🎨 ÖZELLEŞTİRME

### Tahmin Ağırlıklarını Değiştirme:
`prediction_engine.py` → `__init__` metodunda:

```python
self.weights = {
    'form': 0.25,           # %25 Form
    'h2h': 0.20,            # %20 H2H
    'home_advantage': 0.15, # %15 Ev sahibi
    'league_position': 0.15,# %15 Lig pozisyonu
    'goals_stats': 0.15,    # %15 Gol istatistikleri
    'api_prediction': 0.10  # %10 API tahmini
}
```

### Fiyatları Değiştirme:
`.env` dosyasında:

```env
DAILY_PRICE=50      # Günlük
WEEKLY_PRICE=200    # Haftalık
MONTHLY_PRICE=500   # Aylık
```

### Ücretsiz Tahmin Limitini Değiştirme:
`.env` dosyasında:

```env
FREE_PREDICTIONS_PER_DAY=2  # Günlük ücretsiz tahmin
```

---

## 🚨 YAPMAMANIZ GEREKENLER

❌ `.env` dosyasını GitHub'a yüklemeyin
❌ API key'inizi kimseyle paylaşmayın
❌ Bot token'ını açıklamayın
❌ `football_bot.db` dosyasını silmeyin (kullanıcı verileri kaybolur)

---

## ✅ KONTROL LİSTESİ

Kurulum tamamlandı mı?

- [ ] Tüm Python kütüphaneleri yüklü
- [ ] `.env` dosyası düzenlendi
- [ ] Telegram bot oluşturuldu
- [ ] Bot token `.env`'ye eklendi
- [ ] Admin ID `.env`'ye eklendi
- [ ] `python test_api.py` çalıştırıldı ✅
- [ ] `python main.py` ile bot başlatıldı
- [ ] Telegram'da bot test edildi

**Hepsi tamamsa: HAZIRSINIZ! 🎉**
