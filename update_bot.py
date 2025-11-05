import re

# bot.py dosyasını oku
with open('bot.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 212-278 satırlar arası kod bloğunu bul ve değiştir
old_pattern = r'''        response = f"\*\*📅 BUGÜNÜN MAÇLARI\*\*\\n".*?        keyboard = \[
            \[InlineKeyboardButton\("🎯 En İyi Tahminler", callback_data="top_predictions"\)\],
            \[InlineKeyboardButton\("🔙 Ana Menü", callback_data="main_menu"\)\]
        \]'''

new_code = '''        response = f"📅 **BUGÜNÜN MAÇLARI**\\n"
        response += f"📆 {datetime.now().strftime('%d.%m.%Y')} | Toplam: {len(matches)} maç\\n"
        response += f"━━━━━━━━━━━━━━━━━━━━\\n\\n"
        
        # Inline keyboard için butonlar
        keyboard = []
        match_count = 0
        league_count = 0
        
        for league_key, league_matches in sorted_leagues:
            if match_count >= 20:  # Sayfa başına 20 maç
                break
            
            if league_count >= 10:  # Maksimum 10 lig
                break
                
            response += f"🏆 **{league_key}**\\n"
            league_count += 1
            
            for match in league_matches:
                if match_count >= 20:
                    break
                    
                home = match['teams']['home']['name']
                away = match['teams']['away']['name']
                
                try:
                    match_time = datetime.fromisoformat(match['fixture']['date'].replace('Z', '+00:00'))
                    match_time = match_time + timedelta(hours=3)
                    time_str = match_time.strftime('%H:%M')
                except:
                    time_str = "??:??"
                
                status = match['fixture']['status']['short']
                fixture_id = match['fixture']['id']
                
                if status == 'NS':
                    status_emoji = "⏰"
                elif status in ['1H', '2H', 'HT']:
                    status_emoji = "🔴"
                    home_score = match['goals']['home'] or 0
                    away_score = match['goals']['away'] or 0
                    time_str = f"{home_score}-{away_score}"
                elif status == 'FT':
                    status_emoji = "✅"
                    home_score = match['goals']['home'] or 0
                    away_score = match['goals']['away'] or 0
                    time_str = f"{home_score}-{away_score}"
                elif status == 'PST':
                    status_emoji = "⏸️"
                    time_str = "Ertelendi"
                else:
                    status_emoji = "⚽"
                
                response += f"\\n{status_emoji} **{time_str}**\\n"
                response += f"{home} 🆚 {away}\\n"
                keyboard.append([InlineKeyboardButton("📊 Tahmin Al", callback_data=f"pred_{fixture_id}")])
                match_count += 1
            
            response += "\\n"
        
        response += f"\\n💡 İlk {match_count} maç gösteriliyor.\\n"
        
        keyboard.append([InlineKeyboardButton("🎯 En İyi Tahminler", callback_data="top_predictions")])
        keyboard.append([InlineKeyboardButton("🔙 Ana Menü", callback_data="main_menu")])'''

# Değiştir (regex ile)
new_content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

# Kaydet
with open('bot.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ bot.py güncellendi!")
print(f"📝 Değişiklik: Maç listesine her maç için 'Tahmin Al' butonu eklendi")
