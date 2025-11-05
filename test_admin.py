"""
Admin Kontrolü Test Scripti
Botun admin algılama mekanizmasını test eder
"""

import os
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

def test_admin_config():
    """Admin yapılandırmasını test et"""
    print("=" * 60)
    print("🔐 ADMIN YAPIŞLANDIRMA TESTİ")
    print("=" * 60)
    
    # Admin ID'leri al
    admin_ids_str = os.getenv('ADMIN_IDS', '')
    print(f"\n📋 .env dosyasından ADMIN_IDS: {admin_ids_str}")
    
    # Admin ID'leri parse et (bot.py ve admin_panel.py'deki gibi)
    ADMIN_IDS = [int(x) for x in admin_ids_str.split(',') if x.strip()]
    
    print(f"✅ Parse edilen Admin ID'ler: {ADMIN_IDS}")
    print(f"📊 Toplam Admin Sayısı: {len(ADMIN_IDS)}")
    
    # Her admin ID'yi göster
    print("\n👥 Tanımlı Adminler:")
    for idx, admin_id in enumerate(ADMIN_IDS, 1):
        print(f"   {idx}. Admin Telegram ID: {admin_id}")
    
    # Test fonksiyonu
    def is_admin(user_id: int) -> bool:
        """Kullanıcının admin olup olmadığını kontrol et"""
        return user_id in ADMIN_IDS
    
    print("\n" + "=" * 60)
    print("🧪 ADMIN DOĞRULAMA TESTİ")
    print("=" * 60)
    
    # Örnekler
    if ADMIN_IDS:
        test_id = ADMIN_IDS[0]
        print(f"\n✅ Admin ID Test ({test_id}):")
        print(f"   is_admin({test_id}) = {is_admin(test_id)}")
        
        fake_id = 999999999
        print(f"\n❌ Admin Olmayan ID Test ({fake_id}):")
        print(f"   is_admin({fake_id}) = {is_admin(fake_id)}")
    
    # Telegram'dan ID alma talimatı
    print("\n" + "=" * 60)
    print("📱 TELEGRAM ID'NİZİ NASIL ÖĞRENİRSİNİZ?")
    print("=" * 60)
    print("""
1. Telegram'da @userinfobot botunu açın
2. /start komutunu gönderin
3. Bot size Telegram ID'nizi verecektir
4. Bu ID'yi .env dosyasındaki ADMIN_IDS'e ekleyin

ÖRNEĞİN:
ADMIN_IDS=6078613226,123456789,987654321
(Birden fazla admin için virgülle ayırın)
""")
    
    # Bot loglarından kontrol
    print("=" * 60)
    print("🤖 BOTTA ADMIN KONTROLÜ NASIL YAPILIR?")
    print("=" * 60)
    print("""
1. Botu başlatın: python main.py
2. Telegram'dan botunuza /admin komutunu gönderin
3. Eğer admin iseniz, istatistikler göreceksiniz
4. Değilseniz, "Bu komutu kullanma yetkiniz yok!" mesajı alacaksınız

MEVCUT ADMIN KOMUTLARI:
• /admin - Admin paneli ana menü
• /stats - Bot istatistikleri
• /broadcast - Tüm kullanıcılara mesaj gönder
• /users - Kullanıcı listesi
• /premium - Premium kullanıcı listesi
""")
    
    print("\n" + "=" * 60)
    print("✅ Test Tamamlandı!")
    print("=" * 60)
    
    return ADMIN_IDS


if __name__ == "__main__":
    admins = test_admin_config()
    
    if admins:
        print(f"\n🎉 {len(admins)} admin tanımlı ve hazır!")
    else:
        print("\n⚠️  Uyarı: Hiç admin tanımlı değil!")
        print("   .env dosyasını düzenleyip ADMIN_IDS ekleyin.")
