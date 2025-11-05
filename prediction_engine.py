"""
Gelişmiş Tahmin Motoru
Makine öğrenimi ve istatistiksel analiz ile futbol maç tahminleri
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class PredictionEngine:
    """Gelişmiş futbol maç tahmin motoru"""
    
    def __init__(self, api_service):
        self.api = api_service
        self.weights = {
            'form': 0.25,
            'h2h': 0.20,
            'home_advantage': 0.15,
            'league_position': 0.15,
            'goals_stats': 0.15,
            'api_prediction': 0.10
        }
    
    def analyze_match(self, fixture_id: int) -> Optional[Dict]:
        """Maçı kapsamlı analiz et ve tahmin üret"""
        try:
            logger.info(f"Maç analizi başlıyor: fixture_id={fixture_id}")
            
            # Maç bilgilerini al
            fixture = self.api.get_fixture_details(fixture_id)
            if not fixture:
                logger.error(f"Fixture bilgisi alınamadı: {fixture_id}")
                return None
            
            home_team = fixture['teams']['home']
            away_team = fixture['teams']['away']
            league_id = fixture['league']['id']
            season = fixture['league']['season']
            
            logger.info(f"Maç: {home_team['name']} vs {away_team['name']}")
            
            # Veri toplama
            try:
                home_stats = self._get_team_analysis(home_team['id'], league_id, season)
                logger.info(f"Ev sahibi istatistikleri alındı")
            except Exception as e:
                logger.warning(f"Ev sahibi istatistikleri alınamadı: {e}")
                home_stats = self._get_default_team_analysis(home_team['id'])
            
            try:
                away_stats = self._get_team_analysis(away_team['id'], league_id, season)
                logger.info(f"Deplasman istatistikleri alındı")
            except Exception as e:
                logger.warning(f"Deplasman istatistikleri alınamadı: {e}")
                away_stats = self._get_default_team_analysis(away_team['id'])
            
            try:
                h2h = self.api.get_head_to_head(home_team['id'], away_team['id'])
                logger.info(f"H2H verileri alındı")
            except Exception as e:
                logger.warning(f"H2H verileri alınamadı: {e}")
                h2h = []
            
            try:
                api_pred = self.api.get_predictions(fixture_id)
                logger.info(f"API tahminleri alındı")
            except Exception as e:
                logger.warning(f"API tahminleri alınamadı: {e}")
                api_pred = None
            
            # Tahmin hesapla
            prediction = self._calculate_prediction(
                home_stats, away_stats, h2h, api_pred, fixture
            )
            
            # Detaylı rapor oluştur
            report = self._generate_report(
                fixture, home_stats, away_stats, h2h, prediction
            )
            
            logger.info(f"Analiz tamamlandı")
            return report
            
        except Exception as e:
            logger.error(f"Tahmin analizi hatası (fixture_id={fixture_id}): {str(e)}", exc_info=True)
            return None
    
    def _get_default_team_analysis(self, team_id: int) -> Dict:
        """Varsayılan takım analizi (veri yoksa)"""
        return {
            'team_id': team_id,
            'form_score': 50.0,
            'goals_avg': 1.0,
            'goals_conceded_avg': 1.0,
            'win_percentage': 33.0,
            'clean_sheets': 0,
            'recent_form': [],
            'league_position': 999
        }
    
    def _get_team_analysis(self, team_id: int, league_id: int, season: int) -> Dict:
        """Takım için detaylı analiz"""
        stats = self.api.get_team_statistics(team_id, league_id, season)
        form_matches = self.api.get_team_form(team_id, last=5)
        
        analysis = {
            'team_id': team_id,
            'form_score': self._calculate_form_score(form_matches),
            'goals_avg': 0,
            'goals_conceded_avg': 0,
            'win_percentage': 0,
            'clean_sheets': 0,
            'recent_form': [],
            'league_position': 999
        }
        
        if stats:
            fixtures = stats.get('fixtures', {})
            goals = stats.get('goals', {}).get('for', {})
            conceded = stats.get('goals', {}).get('against', {})
            
            total = fixtures.get('played', {}).get('total', 0)
            if total > 0:
                wins = fixtures.get('wins', {}).get('total', 0)
                analysis['win_percentage'] = (wins / total) * 100
                
                total_goals = goals.get('total', {}).get('total', 0)
                total_conceded = conceded.get('total', {}).get('total', 0)
                
                analysis['goals_avg'] = total_goals / total
                analysis['goals_conceded_avg'] = total_conceded / total
                analysis['clean_sheets'] = stats.get('clean_sheet', {}).get('total', 0)
        
        # Son 5 maç formu
        for match in form_matches[:5]:
            if match['teams']['home']['id'] == team_id:
                result = self._get_match_result(
                    match['goals']['home'],
                    match['goals']['away'],
                    True
                )
            else:
                result = self._get_match_result(
                    match['goals']['away'],
                    match['goals']['home'],
                    False
                )
            analysis['recent_form'].append(result)
        
        return analysis
    
    def _calculate_form_score(self, matches: List[Dict]) -> float:
        """Son maçlara göre form skoru hesapla (0-100)"""
        if not matches:
            return 50.0
        
        points = 0
        total_matches = 0
        
        for match in matches[:5]:
            if match['fixture']['status']['short'] not in ['FT', 'AET', 'PEN']:
                continue
            
            home_goals = match['goals']['home']
            away_goals = match['goals']['away']
            
            if home_goals is None or away_goals is None:
                continue
            
            total_matches += 1
            
            # Kazanma: 3 puan, Beraberlik: 1 puan, Mağlubiyet: 0 puan
            if home_goals > away_goals:
                points += 3
            elif home_goals == away_goals:
                points += 1
        
        if total_matches == 0:
            return 50.0
        
        # 5 maçtan maksimum 15 puan alınabilir
        max_points = total_matches * 3
        return (points / max_points) * 100
    
    def _get_match_result(self, goals_for: int, goals_against: int, is_home: bool) -> str:
        """Maç sonucunu belirle"""
        if goals_for > goals_against:
            return 'W'
        elif goals_for < goals_against:
            return 'L'
        else:
            return 'D'
    
    def _analyze_h2h(self, h2h_matches: List[Dict], home_team_id: int) -> Dict:
        """H2H istatistiklerini analiz et"""
        if not h2h_matches:
            return {'home_wins': 0, 'away_wins': 0, 'draws': 0, 'total_matches': 0, 'advantage': 'neutral'}
        
        home_wins = 0
        away_wins = 0
        draws = 0
        
        for match in h2h_matches:
            home_id = match.get('teams', {}).get('home', {}).get('id')
            home_goals = match.get('goals', {}).get('home')
            away_goals = match.get('goals', {}).get('away')
            
            if home_goals is None or away_goals is None or home_id is None:
                continue
            
            if home_goals > away_goals:
                if home_id == home_team_id:
                    home_wins += 1
                else:
                    away_wins += 1
            elif away_goals > home_goals:
                if home_id == home_team_id:
                    away_wins += 1
                else:
                    home_wins += 1
            else:
                draws += 1
        
        total = home_wins + away_wins + draws
        advantage = 'neutral'
        
        if total > 0:
            if home_wins > away_wins * 1.5:
                advantage = 'home'
            elif away_wins > home_wins * 1.5:
                advantage = 'away'
        
        return {
            'home_wins': home_wins,
            'away_wins': away_wins,
            'draws': draws,
            'total_matches': total,
            'advantage': advantage
        }
    
    def _calculate_prediction(self, home_stats: Dict, away_stats: Dict,
                             h2h: List[Dict], api_pred: Dict,
                             fixture: Dict) -> Dict:
        """Tüm verileri kullanarak tahmin hesapla"""
        
        scores = {
            'home_win': 0.0,
            'draw': 0.0,
            'away_win': 0.0
        }
        
        # 1. Form analizi
        home_form = home_stats['form_score']
        away_form = away_stats['form_score']
        form_diff = home_form - away_form
        
        if form_diff > 20:
            scores['home_win'] += self.weights['form'] * 100
        elif form_diff < -20:
            scores['away_win'] += self.weights['form'] * 100
        else:
            scores['draw'] += self.weights['form'] * 50
            scores['home_win'] += self.weights['form'] * 25
            scores['away_win'] += self.weights['form'] * 25
        
        # 2. H2H analizi
        h2h_analysis = self._analyze_h2h(h2h, fixture['teams']['home']['id'])
        if h2h_analysis['advantage'] == 'home':
            scores['home_win'] += self.weights['h2h'] * 100
        elif h2h_analysis['advantage'] == 'away':
            scores['away_win'] += self.weights['h2h'] * 100
        else:
            scores['draw'] += self.weights['h2h'] * 50
            scores['home_win'] += self.weights['h2h'] * 25
            scores['away_win'] += self.weights['h2h'] * 25
        
        # 3. Ev sahibi avantajı
        scores['home_win'] += self.weights['home_advantage'] * 100
        
        # 4. Gol istatistikleri (None kontrolü ile)
        home_goals = home_stats.get('goals_avg', 0) or 0
        away_goals = away_stats.get('goals_avg', 0) or 0
        
        if home_goals > away_goals * 1.3:
            scores['home_win'] += self.weights['goals_stats'] * 70
        elif away_goals > home_goals * 1.3:
            scores['away_win'] += self.weights['goals_stats'] * 70
        else:
            scores['draw'] += self.weights['goals_stats'] * 40
        
        # 5. API tahminini ekle
        if api_pred and 'predictions' in api_pred:
            api_winner = api_pred['predictions'].get('winner', {})
            if api_winner:
                winner_id = api_winner.get('id')
                if winner_id == fixture['teams']['home']['id']:
                    scores['home_win'] += self.weights['api_prediction'] * 100
                elif winner_id == fixture['teams']['away']['id']:
                    scores['away_win'] += self.weights['api_prediction'] * 100
                else:
                    scores['draw'] += self.weights['api_prediction'] * 100
        
        # Skorları normalize et
        total = sum(scores.values())
        if total > 0:
            for key in scores:
                scores[key] = (scores[key] / total) * 100
        
        # En yüksek tahmin
        prediction_type = max(scores, key=scores.get)
        confidence = scores[prediction_type]
        
        # Over/Under 2.5 tahmini (None kontrolü ile)
        home_goals_avg = home_stats.get('goals_avg', 1.0) or 1.0
        away_goals_avg = away_stats.get('goals_avg', 1.0) or 1.0
        home_conceded_avg = home_stats.get('goals_conceded_avg', 1.0) or 1.0
        away_conceded_avg = away_stats.get('goals_conceded_avg', 1.0) or 1.0
        
        avg_goals = (home_goals_avg + away_goals_avg + away_conceded_avg + home_conceded_avg) / 2
        
        over_under = 'Over 2.5' if avg_goals > 2.5 else 'Under 2.5'
        
        # BTTS (Both Teams To Score) (None kontrolü ile)
        btts_prob = 50.0
        clean_sheets_home = home_stats.get('clean_sheets', 0) or 0
        clean_sheets_away = away_stats.get('clean_sheets', 0) or 0
        
        if home_goals_avg > 1 and away_goals_avg > 1:
            btts_prob = 70.0
        elif clean_sheets_home > 3 or clean_sheets_away > 3:
            btts_prob = 30.0
        
        return {
            'prediction_type': prediction_type,
            'confidence': confidence,
            'probabilities': scores,
            'over_under': over_under,
            'btts': 'Yes' if btts_prob > 50 else 'No',
            'btts_probability': btts_prob,
            'expected_goals': round(avg_goals, 2)
        }
    
    def _generate_report(self, fixture: Dict, home_stats: Dict,
                        away_stats: Dict, h2h: List[Dict],
                        prediction: Dict) -> Dict:
        """Detaylı tahmin raporu oluştur"""
        
        home_team = fixture['teams']['home']['name']
        away_team = fixture['teams']['away']['name']
        
        h2h_analysis = self._analyze_h2h(h2h, fixture['teams']['home']['id'])
        
        report = {
            'fixture_id': fixture['fixture']['id'],
            'match': f"{home_team} vs {away_team}",
            'league': fixture['league']['name'],
            'date': fixture['fixture']['date'],
            'venue': fixture['fixture']['venue']['name'],
            
            'prediction': {
                'result': self._get_prediction_text(prediction['prediction_type']),
                'confidence': round(prediction['confidence'], 1),
                'probabilities': {
                    'home_win': round(prediction['probabilities']['home_win'], 1),
                    'draw': round(prediction['probabilities']['draw'], 1),
                    'away_win': round(prediction['probabilities']['away_win'], 1)
                },
                'over_under': prediction['over_under'],
                'btts': prediction['btts'],
                'btts_probability': round(prediction.get('btts_probability', 50.0), 1),
                'expected_goals': prediction['expected_goals']
            },
            
            'analysis': {
                'home_team': {
                    'name': home_team,
                    'form': home_stats['recent_form'][:5],
                    'form_score': round(home_stats['form_score'], 1),
                    'goals_avg': round(home_stats['goals_avg'], 2),
                    'conceded_avg': round(home_stats['goals_conceded_avg'], 2),
                    'win_rate': round(home_stats['win_percentage'], 1)
                },
                'away_team': {
                    'name': away_team,
                    'form': away_stats['recent_form'][:5],
                    'form_score': round(away_stats['form_score'], 1),
                    'goals_avg': round(away_stats['goals_avg'], 2),
                    'conceded_avg': round(away_stats['goals_conceded_avg'], 2),
                    'win_rate': round(away_stats['win_percentage'], 1)
                },
                'h2h': h2h_analysis
            },
            
            'recommendation': self._get_recommendation(prediction)
        }
        
        return report
    
    def _get_prediction_text(self, pred_type: str) -> str:
        """Tahmin tipini metin olarak döndür"""
        mapping = {
            'home_win': '1 (Ev Sahibi Kazanır)',
            'draw': 'X (Beraberlik)',
            'away_win': '2 (Deplasman Kazanır)'
        }
        return mapping.get(pred_type, 'Belirsiz')
    
    def _get_recommendation(self, prediction: Dict) -> str:
        """Tahmine göre öneri oluştur"""
        confidence = prediction['confidence']
        
        if confidence >= 75:
            return "🟢 Yüksek Güven - Güçlü Tahmin"
        elif confidence >= 60:
            return "🟡 Orta Güven - İyi Tahmin"
        elif confidence >= 50:
            return "🟠 Düşük Güven - Riskli"
        else:
            return "🔴 Çok Düşük Güven - Tavsiye Edilmez"
    
    def get_top_predictions_today(self, min_confidence: float = 60.0) -> List[Dict]:
        """Bugün için en güvenli tahminleri getir"""
        logger.info("En iyi tahminler analiz ediliyor...")
        
        today_matches = self.api.get_today_matches()
        
        if not today_matches:
            logger.warning("Bugün için maç bulunamadı")
            return []
        
        predictions = []
        
        # Sadece ilk 10 maçı analiz et (hız için)
        for i, match in enumerate(today_matches[:10], 1):
            try:
                fixture_id = match['fixture']['id']
                logger.info(f"Maç {i}/10 analiz ediliyor: {fixture_id}")
                
                analysis = self.analyze_match(fixture_id)
                
                if analysis and analysis['prediction']['confidence'] >= min_confidence:
                    predictions.append(analysis)
                    logger.info(f"✅ Yüksek güvenli tahmin bulundu: {analysis['prediction']['confidence']}%")
                else:
                    logger.info(f"⚠️ Düşük güven: {analysis['prediction']['confidence'] if analysis else 'N/A'}%")
                    
            except Exception as e:
                logger.error(f"Maç {fixture_id} analiz hatası: {e}")
                continue
        
        # Güven skoruna göre sırala
        predictions.sort(key=lambda x: x['prediction']['confidence'], reverse=True)
        
        logger.info(f"Toplam {len(predictions)} yüksek güvenli tahmin bulundu")
        
        return predictions[:10]  # En iyi 10 tahmin
