#!/bin/bash
# PythonAnywhere Kurulum Script

echo "=========================================="
echo "  Telegram Bot - PythonAnywhere Kurulum"
echo "=========================================="
echo ""

# Sanal ortam oluştur
echo "[1/6] Python sanal ortam oluşturuluyor..."
mkvirtualenv --python=/usr/bin/python3.10 telegram-bot

# Sanal ortamı aktifleştir
workon telegram-bot

# Bağımlılıkları yükle
echo "[2/6] Bağımlılıklar yükleniyor..."
pip install -r requirements.txt

# .env dosyası oluştur
echo "[3/6] .env dosyası oluşturuluyor..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "LÜTFEN .env dosyasını düzenleyin ve TELEGRAM_BOT_TOKEN ekleyin!"
else
    echo ".env dosyası zaten mevcut."
fi

# Database klasörü oluştur
echo "[4/6] Database klasörü hazırlanıyor..."
mkdir -p data

# Log klasörü oluştur
echo "[5/6] Log klasörü oluşturuluyor..."
mkdir -p logs

echo ""
echo "=========================================="
echo "  ✅ Kurulum Tamamlandı!"
echo "=========================================="
echo ""
echo "Sonraki adımlar:"
echo "1. .env dosyasını düzenleyin"
echo "2. 'python main.py' ile botu başlatın"
echo ""
echo "PythonAnywhere'de Always On task olarak çalıştırmak için:"
echo "1. Web > Tasks sekmesine gidin"
echo "2. 'Add a new scheduled task' tıklayın"
echo "3. Komut: workon telegram-bot && python /home/sivrii1940/telegram-bot/main.py"
echo ""
