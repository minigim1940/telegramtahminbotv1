# ⚽ Telegram Futbol Tahmin Botu

Gelişmiş AI algoritmaları ve gerçek zamanlı API-Football verileri kullanarak profesyonel futbol maç tahminleri sunan Telegram botu.

## 🌟 Özellikler

### 📊 Tahmin Sistemi
- ✅ **Gelişmiş AI Tahmin Motoru** - Çok katmanlı analiz sistemi
- ✅ **Gerçek Zamanlı Veriler** - API-Football entegrasyonu
- ✅ **Form Analizi** - Takımların son 5 maç performansı
- ✅ **H2H (Head to Head)** - Geçmiş karşılaşma analizleri
- ✅ **İstatistiksel Analiz** - Gol ortalamaları, kazanma oranları
- ✅ **Ev Sahibi Avantajı** - Saha faktörü hesaplaması
- ✅ **Over/Under 2.5** - Gol sayısı tahminleri
- ✅ **BTTS (Both Teams To Score)** - İki takım da gol atar mı?

### 💎 Üyelik Sistemi
- 🎁 **Ücretsiz Kullanım** - Günde 2 tahmin hakkı
- 💰 **Günlük Paket** - 24 saat sınırsız tahmin (50 TL)
- 📅 **Haftalık Paket** - 7 gün sınırsız tahmin (200 TL)
- ⭐ **Aylık Paket** - 30 gün sınırsız tahmin (500 TL)

### 🔐 Admin Paneli
- 📊 Detaylı istatistikler
- 👥 Kullanıcı yönetimi
- 💰 Gelir raporları
- 📢 Toplu duyuru gönderme
- 🎁 Manuel premium verme

## 🚀 Kurulum

### 1. Gereksinimler
```bash
Python 3.8 veya üzeri
```

### 2. Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Telegram Bot Oluşturun
1. [@BotFather](https://t.me/BotFather) ile konuşun
2. `/newbot` komutunu kullanarak yeni bot oluşturun
3. Bot token'ınızı alın

### 4. Ortam Değişkenlerini Ayarlayın
`.env.example` dosyasını `.env` olarak kopyalayın ve düzenleyin:

```bash
# .env dosyası
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
API_FOOTBALL_KEY=6336fb21e17dea87880d3b133132a13f
STRIPE_SECRET_KEY=your_stripe_secret_key_here  # Opsiyonel
ADMIN_IDS=123456789,987654321  # Telegram user ID'leriniz
```

### 5. Botu Başlatın
```bash
python bot.py
```

## 📖 Kullanım

### Kullanıcı Komutları
- `/start` - Botu başlat ve ana menüyü görüntüle
- `/tahmin` - Maç tahmini al
- `/bugun` - Bugünün maçlarını listele
- `/premium` - Premium paketleri görüntüle
- `/istatistik` - Kişisel istatistiklerinizi görün
- `/yardim` - Yardım menüsü

### Admin Komutları
- `/adminstats` - Genel bot istatistikleri
- `/givepremium <user_id> <daily|weekly|monthly>` - Manuel premium ver
- `/broadcast <mesaj>` - Tüm kullanıcılara duyuru gönder
- `/premiumlist` - Premium kullanıcıları listele
- `/revenue` - Gelir raporu

## 🎯 Tahmin Algoritması

Bot, aşağıdaki faktörleri analiz ederek tahmin oluşturur:

1. **Form Analizi (25%)**
   - Son 5 maçın sonuçları
   - Kazanma/beraberlik/mağlubiyet dağılımı
   - Form skoru hesaplaması

2. **H2H Analizi (20%)**
   - Son 10 karşılaşma
   - Kazanan takım avantajı
   - Gol ortalamaları

3. **Ev Sahibi Avantajı (15%)**
   - İstatistiksel ev sahibi faktörü

4. **Lig Pozisyonu (15%)**
   - Takımların ligteki sıralaması
   - Puan durumu analizi

5. **Gol İstatistikleri (15%)**
   - Gol atma ortalaması
   - Gol yeme ortalaması
   - Clean sheet sayısı

6. **API Tahminleri (10%)**
   - API-Football'un kendi tahminleri

## 💳 Ödeme Sistemi

### Stripe Entegrasyonu
Bot, Stripe üzerinden kredi kartı ödemelerini destekler. Stripe kullanmak için:

1. [Stripe Dashboard](https://dashboard.stripe.com/) hesabı oluşturun
2. API anahtarlarınızı alın
3. `.env` dosyasına ekleyin

### Demo Mod
Stripe anahtarları yoksa, bot demo modda çalışır ve ödemeleri otomatik onaylar.

### Alternatif Ödeme
Havale/EFT desteği için `payment_handler.py` içindeki banka bilgilerini güncelleyin.

## 📊 Veritabanı

Bot SQLite kullanır (SQLAlchemy ile). Aşağıdaki tablolar oluşturulur:

- `users` - Kullanıcı bilgileri
- `subscriptions` - Abonelik kayıtları
- `prediction_logs` - Tahmin geçmişi
- `match_cache` - API sonuçlarını önbellekleme
- `admin_logs` - Admin işlem logları

## 🔧 Yapılandırma

### Ücretsiz Tahmin Limiti
```python
FREE_PREDICTIONS_PER_DAY=2  # .env dosyasında
```

### Fiyatlandırma
```python
DAILY_PRICE=50    # Günlük paket (TL)
WEEKLY_PRICE=200  # Haftalık paket (TL)
MONTHLY_PRICE=500 # Aylık paket (TL)
```

### API Rate Limiting
API-Football çağrıları otomatik olarak cache'lenir (1 saat).

## 🎨 Özelleştirme

### Tahmin Ağırlıklarını Değiştirme
`prediction_engine.py` içinde:

```python
self.weights = {
    'form': 0.25,           # Form ağırlığı
    'h2h': 0.20,            # H2H ağırlığı
    'home_advantage': 0.15, # Ev sahibi ağırlığı
    'league_position': 0.15,# Lig pozisyonu
    'goals_stats': 0.15,    # Gol istatistikleri
    'api_prediction': 0.10  # API tahmini
}
```

### Desteklenen Ligler
`api_football.py` içinde `get_top_leagues()` fonksiyonunu düzenleyin.

## 🐛 Hata Ayıklama

Logları kontrol edin:
```python
logging.basicConfig(level=logging.DEBUG)  # bot.py içinde
```

## 📝 Lisans

Bu proje eğitim amaçlıdır. Ticari kullanım için API-Football ve Telegram Bot API kullanım şartlarını kontrol edin.

## ⚠️ Önemli Notlar

1. **API Limitleri**: API-Football planınızın limitlerini kontrol edin
2. **Ücretli Sistem**: Gerçek para işlemleri için ödeme sağlayıcısı şartlarına uyun
3. **Tahmin Sorumluluğu**: Tahminler bilgilendirme amaçlıdır, bahis tavsiyesi değildir
4. **KVKK**: Kullanıcı verilerini güvenli tutun ve yasal düzenlemelere uyun

## 🤝 Destek

Sorularınız için:
- GitHub Issues
- Email: your-email@example.com
- Telegram: @YourSupportUsername

## 🚀 Gelecek Özellikler

- [ ] Canlı maç skorları
- [ ] Push bildirimleri
- [ ] Tahmin başarı oranı takibi
- [ ] Çoklu dil desteği
- [ ] Web panel
- [ ] Referans sistemi
- [ ] VIP analiz paketleri

## 📈 Güncellemeler

### v1.0.0 (İlk Sürüm)
- ✅ Temel tahmin sistemi
- ✅ Ödeme entegrasyonu
- ✅ Admin paneli
- ✅ Ücretsiz kullanım limitleri
- ✅ API-Football entegrasyonu

---

**Made with ❤️ for Football Fans**

⚽ İyi tahminler! 🎯
