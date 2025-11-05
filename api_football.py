"""
API Football Data Service
API-Football'dan gerçek zamanlı maç verileri çekme modülü
"""

import requests
import os
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIFootballService:
    """API-Football ile veri alışverişi için servis sınıfı"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """API'ye istek gönder ve sonucu döndür"""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('errors'):
                logger.error(f"API Error: {data['errors']}")
                return None
            
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def get_live_matches(self) -> List[Dict]:
        """Canlı maçları getir"""
        data = self._make_request('fixtures', {'live': 'all'})
        return data.get('response', []) if data else []
    
    def get_today_matches(self) -> List[Dict]:
        """Bugünkü maçları getir - Türkiye saati ile"""
        # Türkiye saati ile bugünün tarihini al
        turkey_tz = pytz.timezone('Europe/Istanbul')
        today = datetime.now(turkey_tz).strftime('%Y-%m-%d')
        
        logger.info(f"Bugünün maçları çekiliyor: {today}")
        
        data = self._make_request('fixtures', {'date': today})
        matches = data.get('response', []) if data else []
        
        logger.info(f"{len(matches)} maç bulundu")
        
        return matches
    
    def get_upcoming_matches(self, days: int = 3) -> List[Dict]:
        """Yaklaşan maçları getir"""
        matches = []
        for i in range(days):
            date = (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d')
            data = self._make_request('fixtures', {'date': date})
            if data:
                matches.extend(data.get('response', []))
        return matches
    
    def get_match_statistics(self, fixture_id: int) -> Optional[Dict]:
        """Belirli bir maçın istatistiklerini getir"""
        data = self._make_request('fixtures/statistics', {'fixture': fixture_id})
        return data.get('response', []) if data else None
    
    def get_head_to_head(self, team1_id: int, team2_id: int) -> List[Dict]:
        """İki takım arasındaki geçmiş maçları getir"""
        h2h = f"{team1_id}-{team2_id}"
        data = self._make_request('fixtures/headtohead', {'h2h': h2h, 'last': 10})
        return data.get('response', []) if data else []
    
    def get_team_statistics(self, team_id: int, league_id: int, season: int) -> Optional[Dict]:
        """Takım istatistiklerini getir"""
        data = self._make_request('teams/statistics', {
            'team': team_id,
            'league': league_id,
            'season': season
        })
        return data.get('response') if data else None
    
    def get_team_form(self, team_id: int, last: int = 5) -> List[Dict]:
        """Takımın son maçlarını getir (form analizi için)"""
        data = self._make_request('fixtures', {
            'team': team_id,
            'last': last
        })
        return data.get('response', []) if data else []
    
    def get_predictions(self, fixture_id: int) -> Optional[Dict]:
        """API-Football tahminlerini getir"""
        data = self._make_request('predictions', {'fixture': fixture_id})
        return data.get('response', [{}])[0] if data else None
    
    def get_odds(self, fixture_id: int) -> List[Dict]:
        """Maç oranlarını getir"""
        data = self._make_request('odds', {
            'fixture': fixture_id
        })
        return data.get('response', []) if data else []
    
    def get_league_standings(self, league_id: int, season: int) -> List[Dict]:
        """Lig sıralamasını getir"""
        data = self._make_request('standings', {
            'league': league_id,
            'season': season
        })
        if data and data.get('response'):
            return data['response'][0].get('league', {}).get('standings', [[]])[0]
        return []
    
    def get_top_leagues(self) -> List[int]:
        """En popüler liglerin ID'lerini döndür"""
        return [
            39,   # Premier League
            140,  # La Liga
            78,   # Bundesliga
            135,  # Serie A
            61,   # Ligue 1
            203,  # Süper Lig (Türkiye)
            2,    # UEFA Champions League
            3,    # UEFA Europa League
            88,   # Eredivisie
            94,   # Primeira Liga
        ]
    
    def get_fixture_details(self, fixture_id: int) -> Optional[Dict]:
        """Maç detaylarını getir"""
        data = self._make_request('fixtures', {'id': fixture_id})
        if data and data.get('response'):
            return data['response'][0]
        return None
    
    def search_team(self, team_name: str) -> List[Dict]:
        """Takım ara"""
        data = self._make_request('teams', {'search': team_name})
        return data.get('response', []) if data else []
    
    def get_injuries(self, fixture_id: int) -> List[Dict]:
        """Maç için sakatlık listesini getir"""
        data = self._make_request('injuries', {'fixture': fixture_id})
        return data.get('response', []) if data else []
    
    def get_lineups(self, fixture_id: int) -> List[Dict]:
        """Maç kadrosunu getir"""
        data = self._make_request('fixtures/lineups', {'fixture': fixture_id})
        return data.get('response', []) if data else []
