# Test Scripti
# API-Football bağlantısını ve tahmin motorunu test eder

from dotenv import load_dotenv
import os

load_dotenv()

print("🧪 API-Football Test Scripti")
print("=" * 60)

# API servisini test et
try:
    from api_football import APIFootballService
    
    api_key = os.getenv('API_FOOTBALL_KEY')
    print(f"\n✅ API Key bulundu: {api_key[:10]}...")
    
    api = APIFootballService(api_key)
    
    print("\n📊 Bugünün maçları getiriliyor...")
    matches = api.get_today_matches()
    
    if matches:
        print(f"✅ {len(matches)} maç bulundu!")
        
        # İlk 3 maçı göster
        print("\nİlk 3 maç:")
        for i, match in enumerate(matches[:3], 1):
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            league = match['league']['name']
            print(f"{i}. {home} vs {away} ({league})")
    else:
        print("⚠️  Bugün maç bulunamadı")
    
    print("\n✅ API servisi çalışıyor!")
    
except Exception as e:
    print(f"❌ API test hatası: {e}")

# Tahmin motorunu test et
print("\n" + "=" * 60)
print("🎯 Tahmin Motoru Testi")
print("=" * 60)

try:
    from prediction_engine import PredictionEngine
    
    engine = PredictionEngine(api)
    print("✅ Tahmin motoru oluşturuldu!")
    
    if matches and len(matches) > 0:
        print(f"\n📊 İlk maç analiz ediliyor...")
        fixture_id = matches[0]['fixture']['id']
        
        analysis = engine.analyze_match(fixture_id)
        
        if analysis:
            print(f"\n✅ Analiz başarılı!")
            print(f"Maç: {analysis['match']}")
            print(f"Tahmin: {analysis['prediction']['result']}")
            print(f"Güven: {analysis['prediction']['confidence']}%")
        else:
            print("⚠️  Analiz yapılamadı (bazı veriler eksik olabilir)")
    
except Exception as e:
    print(f"❌ Tahmin motoru test hatası: {e}")

# Veritabanını test et
print("\n" + "=" * 60)
print("📊 Veritabanı Testi")
print("=" * 60)

try:
    from database import DatabaseManager
    
    db = DatabaseManager()
    print("✅ Veritabanı bağlantısı başarılı!")
    
    # Test kullanıcısı oluştur
    test_user = db.get_or_create_user(
        telegram_id=123456789,
        username="test_user",
        first_name="Test"
    )
    
    print(f"✅ Test kullanıcısı oluşturuldu: {test_user.username}")
    
except Exception as e:
    print(f"❌ Veritabanı test hatası: {e}")

print("\n" + "=" * 60)
print("✅ TÜM TESTLER TAMAMLANDI!")
print("=" * 60)
print("\n💡 Şimdi botu çalıştırabilirsiniz: python main.py\n")
