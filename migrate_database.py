"""
Veritabanı Migration Script
Mevcut veritabanına yeni kolonları ekler (veri kaybı olmadan)
"""

import sqlite3
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_database():
    """Veritabanına yeni kolonları ekle"""
    db_path = 'football_bot.db'
    
    if not os.path.exists(db_path):
        logger.error(f"❌ Veritabanı bulunamadı: {db_path}")
        logger.info("💡 Önce botu başlatıp veritabanını oluşturun!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Mevcut kolonları kontrol et
        cursor.execute("PRAGMA table_info(prediction_logs)")
        columns = [col[1] for col in cursor.fetchall()]
        logger.info(f"Mevcut kolonlar: {columns}")
        
        # Yeni kolonları ekle
        new_columns = {
            'match_date': 'TEXT',
            'prediction_made_at': 'DATETIME',
            'match_result': 'TEXT',
            'is_correct': 'BOOLEAN'
        }
        
        for col_name, col_type in new_columns.items():
            if col_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE prediction_logs ADD COLUMN {col_name} {col_type}")
                    logger.info(f"✅ Kolon eklendi: {col_name}")
                except sqlite3.OperationalError as e:
                    logger.warning(f"⚠️ Kolon zaten var olabilir: {col_name} - {e}")
            else:
                logger.info(f"✓ Kolon zaten mevcut: {col_name}")
        
        conn.commit()
        conn.close()
        
        logger.info("🎉 Migration tamamlandı!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration hatası: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("VERİTABANI MIGRATION")
    print("=" * 50)
    migrate_database()
