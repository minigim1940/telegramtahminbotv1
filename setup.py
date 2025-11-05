"""
Kurulum Scripti - Bot Kurulumu için Yardımcı
"""

import os
import sys


def create_env_file():
    """Eğer .env dosyası yoksa oluştur"""
    if os.path.exists('.env'):
        print("✅ .env dosyası zaten mevcut")
        return
    
    if os.path.exists('.env.example'):
        # .env.example'dan kopyala
        with open('.env.example', 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ .env dosyası oluşturuldu (.env.example'dan)")
        print("⚠️  Lütfen .env dosyasını düzenleyip gerekli bilgileri girin!")
    else:
        print("❌ .env.example dosyası bulunamadı")


def check_python_version():
    """Python versiyonunu kontrol et"""
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 veya üzeri gerekli!")
        print(f"Mevcut versiyon: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python versiyonu uygun: {version.major}.{version.minor}.{version.micro}")
    return True


def install_requirements():
    """Gereksinimleri yükle"""
    import subprocess
    
    print("\n📦 Gerekli kütüphaneler yükleniyor...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Tüm kütüphaneler başarıyla yüklendi!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Kütüphaneler yüklenirken hata oluştu!")
        return False


def setup_database():
    """Veritabanını oluştur"""
    print("\n📊 Veritabanı oluşturuluyor...")
    
    try:
        from database import DatabaseManager
        db = DatabaseManager()
        print("✅ Veritabanı başarıyla oluşturuldu!")
        return True
    except Exception as e:
        print(f"❌ Veritabanı oluşturulurken hata: {e}")
        return False


def print_instructions():
    """Kurulum talimatlarını yazdır"""
    print("\n" + "=" * 60)
    print("🎯 KURULUM TAMAMLANDI!")
    print("=" * 60)
    print("\n📝 SONRAKI ADIMLAR:\n")
    print("1. Telegram Bot Oluşturun:")
    print("   - @BotFather ile konuşun")
    print("   - /newbot komutuyla bot oluşturun")
    print("   - Bot token'ınızı alın\n")
    print("2. .env Dosyasını Düzenleyin:")
    print("   - .env dosyasını açın")
    print("   - TELEGRAM_BOT_TOKEN değerini girin")
    print("   - API_FOOTBALL_KEY zaten ayarlanmış (test için)")
    print("   - ADMIN_IDS değerine Telegram ID'nizi ekleyin\n")
    print("3. Telegram ID'nizi Öğrenin:")
    print("   - @userinfobot ile konuşun")
    print("   - Size verilen ID'yi ADMIN_IDS'e ekleyin\n")
    print("4. Botu Çalıştırın:")
    print("   python main.py\n")
    print("=" * 60)
    print("\n💡 İPUCU: Stripe ödeme sistemi opsiyoneldir.")
    print("   Demo modda test edebilirsiniz.\n")


def main():
    """Ana kurulum fonksiyonu"""
    print("=" * 60)
    print("⚽ TELEGRAM FUTBOL TAHMİN BOTU KURULUMU")
    print("=" * 60)
    print()
    
    # Python versiyonu kontrolü
    if not check_python_version():
        sys.exit(1)
    
    # .env dosyası oluştur
    create_env_file()
    
    # Kullanıcıya sor
    response = input("\n📦 Gereksinimleri şimdi yüklemek ister misiniz? (E/H): ")
    
    if response.lower() in ['e', 'evet', 'y', 'yes']:
        if not install_requirements():
            print("\n⚠️  Kütüphaneleri manuel olarak yükleyin:")
            print("   pip install -r requirements.txt")
            sys.exit(1)
        
        # Veritabanı oluştur
        if not setup_database():
            print("\n⚠️  Veritabanı daha sonra otomatik oluşturulacak")
    else:
        print("\n⚠️  Gereksinimleri kendiniz yükleyin:")
        print("   pip install -r requirements.txt")
    
    # Talimatları yazdır
    print_instructions()


if __name__ == '__main__':
    main()
