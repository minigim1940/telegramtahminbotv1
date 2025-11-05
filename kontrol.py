"""
Final Kontrol Scripti
Kurulumun tamamlanıp tamamlanmadığını kontrol eder
"""

import os
import sys
from pathlib import Path

print("=" * 70)
print("🔍 TELEGRAM FUTBOL TAHMİN BOTU - KURULUM KONTROLÜ")
print("=" * 70)
print()

errors = []
warnings = []
success = []

# 1. .env dosyası kontrolü
print("📋 1. .env Dosyası Kontrolü...")
if os.path.exists('.env'):
    success.append("✅ .env dosyası mevcut")
    
    with open('.env', 'r', encoding='utf-8') as f:
        env_content = f.read()
    
    # Token kontrolü
    if 'TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here' in env_content:
        errors.append("❌ TELEGRAM_BOT_TOKEN henüz ayarlanmamış!")
        print("   ❌ Bot token'ı ayarlanmamış")
    else:
        success.append("✅ Bot token ayarlanmış")
        print("   ✅ Bot token ayarlanmış")
    
    # API key kontrolü
    if 'API_FOOTBALL_KEY=6336fb21e17dea87880d3b133132a13f' in env_content:
        success.append("✅ API-Football key hazır")
        print("   ✅ API-Football key hazır")
    else:
        warnings.append("⚠️  API key değiştirilmiş")
    
    # Admin ID kontrolü
    if 'ADMIN_IDS=123456789,987654321' in env_content:
        warnings.append("⚠️  Admin ID'ler örnek değerlerde (değiştirmelisiniz)")
        print("   ⚠️  Admin ID'ler henüz değiştirilmemiş")
    else:
        success.append("✅ Admin ID'ler ayarlanmış")
        print("   ✅ Admin ID'ler ayarlanmış")
else:
    errors.append("❌ .env dosyası bulunamadı!")
    print("   ❌ .env dosyası bulunamadı")

print()

# 2. Python kütüphaneleri kontrolü
print("📦 2. Python Kütüphaneleri Kontrolü...")
required_modules = [
    'telegram',
    'requests', 
    'dotenv',
    'sqlalchemy',
    'pandas',
    'numpy',
    'sklearn',
    'stripe',
    'pytz'
]

missing_modules = []
for module in required_modules:
    try:
        if module == 'telegram':
            __import__('telegram')
        elif module == 'dotenv':
            __import__('dotenv')
        elif module == 'sklearn':
            __import__('sklearn')
        else:
            __import__(module)
        print(f"   ✅ {module} yüklü")
    except ImportError:
        missing_modules.append(module)
        print(f"   ❌ {module} eksik")

if missing_modules:
    errors.append(f"❌ Eksik modüller: {', '.join(missing_modules)}")
else:
    success.append("✅ Tüm Python kütüphaneleri yüklü")

print()

# 3. Veritabanı kontrolü
print("🗄️  3. Veritabanı Kontrolü...")
if os.path.exists('football_bot.db'):
    success.append("✅ Veritabanı oluşturulmuş")
    print("   ✅ football_bot.db mevcut")
    
    # Veritabanı tabloları kontrolü
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        print("   ✅ Veritabanı bağlantısı başarılı")
        success.append("✅ Veritabanı çalışıyor")
    except Exception as e:
        errors.append(f"❌ Veritabanı hatası: {e}")
        print(f"   ❌ Veritabanı hatası: {e}")
else:
    warnings.append("⚠️  Veritabanı henüz oluşturulmamış (ilk çalıştırmada oluşacak)")
    print("   ⚠️  Veritabanı henüz oluşturulmamış")

print()

# 4. API bağlantısı kontrolü
print("🌐 4. API-Football Bağlantısı Kontrolü...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    
    from api_football import APIFootballService
    
    api_key = os.getenv('API_FOOTBALL_KEY')
    if api_key and api_key != 'your_api_key_here':
        api = APIFootballService(api_key)
        
        # Basit bir test
        print("   🔄 API testi yapılıyor...")
        matches = api.get_today_matches()
        
        if matches:
            success.append(f"✅ API çalışıyor ({len(matches)} maç bulundu)")
            print(f"   ✅ API çalışıyor! Bugün {len(matches)} maç var")
        else:
            warnings.append("⚠️  API çalışıyor ama bugün maç yok")
            print("   ⚠️  API çalışıyor ama bugün maç bulunamadı")
    else:
        errors.append("❌ API key ayarlanmamış")
        print("   ❌ API key ayarlanmamış")
        
except Exception as e:
    errors.append(f"❌ API testi başarısız: {e}")
    print(f"   ❌ API testi başarısız: {e}")

print()

# 5. Dosya yapısı kontrolü
print("📂 5. Dosya Yapısı Kontrolü...")
required_files = [
    'bot.py',
    'api_football.py',
    'prediction_engine.py',
    'database.py',
    'payment_handler.py',
    'admin_panel.py',
    'main.py',
    'requirements.txt'
]

missing_files = []
for file in required_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        missing_files.append(file)
        print(f"   ❌ {file} eksik!")

if missing_files:
    errors.append(f"❌ Eksik dosyalar: {', '.join(missing_files)}")
else:
    success.append("✅ Tüm gerekli dosyalar mevcut")

print()
print("=" * 70)
print("📊 SONUÇ RAPORU")
print("=" * 70)
print()

print("✅ BAŞARILAR:")
for s in success:
    print(f"   {s}")
print()

if warnings:
    print("⚠️  UYARILAR:")
    for w in warnings:
        print(f"   {w}")
    print()

if errors:
    print("❌ HATALAR:")
    for e in errors:
        print(f"   {e}")
    print()
    print("🔧 YAPMANIZ GEREKENLER:")
    print()
    
    if any('TELEGRAM_BOT_TOKEN' in e for e in errors):
        print("1. Telegram'da @BotFather ile bot oluşturun")
        print("2. Aldığınız token'ı .env dosyasına yazın")
        print()
    
    if any('Admin ID' in w for w in warnings):
        print("1. Telegram'da @userinfobot ile ID'nizi öğrenin")
        print("2. .env dosyasındaki ADMIN_IDS satırını değiştirin")
        print()
    
    if any('modül' in e.lower() for e in errors):
        print("Eksik kütüphaneleri yükleyin:")
        print("   pip install -r requirements.txt")
        print()
else:
    print("🎉 HARIKA! KURULUM TAMAMLANDI!")
    print()
    print("🚀 BOTU BAŞLATMAK İÇİN:")
    print("   python main.py")
    print()
    print("📱 TELEGRAM'DA TEST ETMEK İÇİN:")
    print("   1. Botunuzu bulun")
    print("   2. /start yazın")
    print("   3. Tahmin almaya başlayın!")
    print()

print("=" * 70)
print()

# Çıkış kodu
sys.exit(0 if not errors else 1)
