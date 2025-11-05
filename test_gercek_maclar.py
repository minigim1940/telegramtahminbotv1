"""
API Test - Gerçek Maçları Kontrol Et
"""
import os
from dotenv import load_dotenv
from api_football import APIFootballService
from datetime import datetime

load_dotenv()

api = APIFootballService(os.getenv('API_FOOTBALL_KEY'))

print("=" * 70)
print(f"📅 BUGÜNÜN TARİHİ: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 70)

# Bugünün maçlarını çek
print("\n🔍 API'den bugünün maçları çekiliyor...")
matches = api.get_today_matches()

if not matches:
    print("❌ Bugün için maç bulunamadı!")
    print("\n🔄 Canlı maçları kontrol ediliyor...")
    live_matches = api.get_live_matches()
    print(f"📊 Canlı maç sayısı: {len(live_matches)}")
    
    if live_matches:
        print("\n🔴 CANLI MAÇLAR:")
        for i, match in enumerate(live_matches[:5], 1):
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            league = match['league']['name']
            status = match['fixture']['status']['short']
            score_home = match['goals']['home']
            score_away = match['goals']['away']
            
            print(f"{i}. [{status}] {home} {score_home}-{score_away} {away}")
            print(f"   🏆 {league}")
            print(f"   🆔 ID: {match['fixture']['id']}\n")
else:
    print(f"✅ {len(matches)} maç bulundu!\n")
    
    # Liglere göre grupla
    leagues = {}
    for match in matches:
        league_name = match['league']['name']
        if league_name not in leagues:
            leagues[league_name] = []
        leagues[league_name].append(match)
    
    print(f"📊 {len(leagues)} farklı lig\n")
    print("=" * 70)
    
    for league_name, league_matches in list(leagues.items())[:10]:
        print(f"\n🏆 {league_name} ({len(league_matches)} maç)")
        print("-" * 70)
        
        for match in league_matches[:5]:
            home = match['teams']['home']['name']
            away = match['teams']['away']['name']
            time = datetime.fromisoformat(match['fixture']['date'].replace('Z', '+00:00'))
            time_str = time.strftime('%H:%M')
            status = match['fixture']['status']['short']
            fixture_id = match['fixture']['id']
            
            print(f"  ⚽ {time_str} | {home} vs {away}")
            print(f"     Durum: {status} | ID: {fixture_id}")

print("\n" + "=" * 70)
print("✅ Test tamamlandı!")
