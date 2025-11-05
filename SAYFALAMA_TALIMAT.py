"""
SAYFALAMA ÖZELLİĞİ EKLE - Talimatlar

1. bot.py'de today_matches metodunu bul (satır 141)
2. Metod imzasını değiştir:
   ÖNCESİ: async def today_matches(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
   SONRASI: async def today_matches(self, update: Update, context: ContextTypes.DEFAULT_TYPE, page: int = 0):

3. "if match_count >= 40:" satırlarını kaldır
4. Sayfalama kodu ekle (satır 195'ten sonra):
"""

# Sayfalama kodu (satır 195'ten sonra eklenecek):
PAGINATION_CODE = """
        # Maçları saate göre sırala
        sorted_matches = []
        for match in matches:
            try:
                match_time = datetime.fromisoformat(match['fixture']['date'].replace('Z', '+00:00'))
                match_time = match_time + timedelta(hours=3)
                match['_sort_time'] = match_time
                sorted_matches.append(match)
            except:
                sorted_matches.append(match)
        
        sorted_matches.sort(key=lambda x: x.get('_sort_time', datetime.now()))
        
        # Sayfalama
        MATCHES_PER_PAGE = 50
        total_matches = len(sorted_matches)
        total_pages = (total_matches + MATCHES_PER_PAGE - 1) // MATCHES_PER_PAGE
        
        if page < 0:
            page = 0
        if page >= total_pages:
            page = max(0, total_pages - 1)
        
        start_idx = page * MATCHES_PER_PAGE
        end_idx = min(start_idx + MATCHES_PER_PAGE, total_matches)
        page_matches = sorted_matches[start_idx:end_idx]
        
        # Liglere göre grupla (sayfalandırılmış maçlar)
        leagues = {}
        for match in page_matches:
            league_name = match['league']['name']
            country = match['league']['country']
            league_key = f"{country} - {league_name}"
            
            if league_key not in leagues:
                leagues[league_key] = []
            leagues[league_key].append(match)
        
        response = f"**📅 BUGÜNÜN TÜM MAÇLARI**\\n"
        response += f"**🗓️ Tarih:** {datetime.now().strftime('%d.%m.%Y')}\\n"
        response += f"**📊 Toplam:** {total_matches} maç\\n"
        response += f"**📄 Sayfa:** {page + 1}/{total_pages} (Maç {start_idx + 1}-{end_idx})\\n\\n"
"""

# 5. Buton kısmını değiştir (satır 270 civarı):
BUTTON_CODE = """
        # Sayfalama butonları
        keyboard = []
        nav_row = []
        if page > 0:
            nav_row.append(InlineKeyboardButton("⬅️ Önceki", callback_data=f"matches_page_{page - 1}"))
        if page < total_pages - 1:
            nav_row.append(InlineKeyboardButton("Sonraki ➡️", callback_data=f"matches_page_{page + 1}"))
        if nav_row:
            keyboard.append(nav_row)
        
        keyboard.append([InlineKeyboardButton("🎯 En İyi Tahminler", callback_data="top_predictions")])
        keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")])
"""

# 6. button_callback metoduna ekle (satır 730 civarı):
CALLBACK_CODE = """
        elif query.data.startswith("matches_page_"):
            page_num = int(query.data.split("_")[-1])
            await self.today_matches(update, context, page=page_num)
"""

print("Talimatlar hazır!")
print("\nMANUEL DÜZENLEME GEREKLİ:")
print("1. bot.py'yi bir editörde aç")
print("2. today_matches metodunu sayfalama destekli hale getir")
print("3. button_callback'e matches_page_ kontrolü ekle")
