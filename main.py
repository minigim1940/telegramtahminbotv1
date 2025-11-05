#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Telegram Futbol Tahmin Botu - Ana Çalıştırma Dosyası
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

# Logging yapılandırması
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def check_requirements():
    """Gerekli ortam değişkenlerini kontrol et"""
    required_vars = ['TELEGRAM_BOT_TOKEN', 'API_FOOTBALL_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Eksik ortam değişkenleri: {', '.join(missing_vars)}")
        logger.error("Lütfen .env dosyasını oluşturun ve gerekli değişkenleri ekleyin.")
        logger.error(".env.example dosyasını .env olarak kopyalayıp düzenleyebilirsiniz.")
        return False
    
    return True


def main():
    """Ana fonksiyon"""
    logger.info("=" * 60)
    logger.info("⚽ Telegram Futbol Tahmin Botu Başlatılıyor...")
    logger.info("=" * 60)
    
    # Gereksinimleri kontrol et
    if not check_requirements():
        sys.exit(1)
    
    # Bot modülünü import et
    try:
        from bot import FootballPredictionBot
        from database import DatabaseManager
        from admin_panel import setup_admin_handlers
        
        # Veritabanını başlat
        logger.info("📊 Veritabanı başlatılıyor...")
        db_manager = DatabaseManager()
        
        # Botu oluştur
        logger.info("🤖 Bot oluşturuluyor...")
        bot = FootballPredictionBot()
        
        # Admin handler'larını ekle
        logger.info("🔐 Admin paneli yapılandırılıyor...")
        # Not: Admin paneli bot.run() öncesi eklenmeli
        # Bu yüzden bot sınıfında yapıyoruz
        
        logger.info("✅ Bot hazır!")
        logger.info("=" * 60)
        logger.info("Bot çalışıyor... Durdurmak için Ctrl+C basın")
        logger.info("=" * 60)
        
        # Botu çalıştır
        bot.run()
        
    except ImportError as e:
        logger.error(f"❌ Modül import hatası: {e}")
        logger.error("Lütfen gerekli kütüphaneleri yükleyin: pip install -r requirements.txt")
        sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("\n" + "=" * 60)
        logger.info("🛑 Bot kapatılıyor...")
        logger.info("=" * 60)
        sys.exit(0)
    
    except Exception as e:
        logger.error(f"❌ Beklenmeyen hata: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
