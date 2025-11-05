"""
Utility Fonksiyonları
Yardımcı araçlar ve formatlaştırma fonksiyonları
"""

from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Optional
import json


def format_datetime(dt: datetime, timezone: str = 'Europe/Istanbul') -> str:
    """Datetime'ı Türkiye saatine göre formatla"""
    try:
        tz = pytz.timezone(timezone)
        if dt.tzinfo is None:
            dt = pytz.utc.localize(dt)
        local_dt = dt.astimezone(tz)
        return local_dt.strftime('%d.%m.%Y %H:%M')
    except:
        return dt.strftime('%d.%m.%Y %H:%M')


def format_currency(amount: float) -> str:
    """Para birimi formatla"""
    return f"{amount:.2f} TL"


def format_percentage(value: float) -> str:
    """Yüzde formatla"""
    return f"{value:.1f}%"


def get_form_emoji(result: str) -> str:
    """Form sonucu için emoji döndür"""
    emoji_map = {
        'W': '✅',  # Win
        'D': '🟨',  # Draw
        'L': '❌'   # Loss
    }
    return emoji_map.get(result, '⚪')


def get_confidence_emoji(confidence: float) -> str:
    """Güven oranına göre emoji döndür"""
    if confidence >= 75:
        return '🟢'
    elif confidence >= 60:
        return '🟡'
    elif confidence >= 50:
        return '🟠'
    else:
        return '🔴'


def truncate_text(text: str, max_length: int = 100) -> str:
    """Metni belirtilen uzunlukta kes"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + '...'


def create_progress_bar(value: float, max_value: float = 100, length: int = 10) -> str:
    """İlerleme çubuğu oluştur"""
    filled = int((value / max_value) * length)
    empty = length - filled
    return '█' * filled + '░' * empty


def format_match_time(dt: datetime) -> str:
    """Maç zamanını formatla"""
    now = datetime.utcnow()
    
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    
    diff = dt - now.replace(tzinfo=pytz.utc)
    
    if diff.days < 0:
        return "Bitti"
    elif diff.days == 0:
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        
        if hours == 0:
            return f"{minutes} dakika sonra"
        return f"{hours} saat {minutes} dakika sonra"
    elif diff.days == 1:
        return "Yarın"
    else:
        return f"{diff.days} gün sonra"


def calculate_roi(predictions: List[Dict]) -> Dict:
    """ROI (Return on Investment) hesapla"""
    total = len(predictions)
    
    if total == 0:
        return {
            'total': 0,
            'won': 0,
            'lost': 0,
            'pending': 0,
            'win_rate': 0.0,
            'roi': 0.0
        }
    
    won = sum(1 for p in predictions if p.get('result') == 'won')
    lost = sum(1 for p in predictions if p.get('result') == 'lost')
    pending = sum(1 for p in predictions if p.get('result') is None)
    
    win_rate = (won / (won + lost) * 100) if (won + lost) > 0 else 0.0
    
    # Basit ROI hesaplaması (her doğru tahmin için +1, yanlış için -1)
    roi = ((won - lost) / total * 100) if total > 0 else 0.0
    
    return {
        'total': total,
        'won': won,
        'lost': lost,
        'pending': pending,
        'win_rate': win_rate,
        'roi': roi
    }


def get_league_flag(league_id: int) -> str:
    """Lig için bayrak emojisi döndür"""
    flags = {
        39: '🏴󠁧󠁢󠁥󠁮󠁧󠁿',   # Premier League
        140: '🇪🇸',  # La Liga
        78: '🇩🇪',   # Bundesliga
        135: '🇮🇹',  # Serie A
        61: '🇫🇷',   # Ligue 1
        203: '🇹🇷',  # Süper Lig
        2: '🇪🇺',    # Champions League
        3: '🇪🇺',    # Europa League
        88: '🇳🇱',   # Eredivisie
        94: '🇵🇹',   # Primeira Liga
    }
    return flags.get(league_id, '⚽')


def format_team_form(form: List[str]) -> str:
    """Takım formunu emoji ile formatla"""
    return ' '.join([get_form_emoji(result) for result in form])


def validate_odds(odds: float) -> bool:
    """Bahis oranının geçerli olup olmadığını kontrol et"""
    return 1.0 <= odds <= 100.0


def calculate_expected_value(probability: float, odds: float) -> float:
    """Beklenen değer hesapla (EV)"""
    # EV = (probability * odds) - 1
    return (probability / 100 * odds) - 1


def get_time_until_match(dt: datetime) -> str:
    """Maça kalan süreyi hesapla"""
    now = datetime.utcnow()
    
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    
    diff = dt - now.replace(tzinfo=pytz.utc)
    
    if diff.days < 0:
        return "Başladı"
    
    hours = diff.seconds // 3600
    minutes = (diff.seconds % 3600) // 60
    
    return f"{diff.days}g {hours}s {minutes}d"


def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Güvenli bölme işlemi"""
    try:
        return a / b if b != 0 else default
    except (TypeError, ZeroDivisionError):
        return default


def parse_json_safe(json_string: str, default: Dict = None) -> Dict:
    """Güvenli JSON parsing"""
    if default is None:
        default = {}
    
    try:
        return json.loads(json_string)
    except (json.JSONDecodeError, TypeError):
        return default


def format_large_number(number: int) -> str:
    """Büyük sayıları formatla (1000 -> 1K)"""
    if number < 1000:
        return str(number)
    elif number < 1000000:
        return f"{number/1000:.1f}K"
    else:
        return f"{number/1000000:.1f}M"


class MatchStatus:
    """Maç durumu sabitleri"""
    NOT_STARTED = 'NS'
    FIRST_HALF = '1H'
    HALF_TIME = 'HT'
    SECOND_HALF = '2H'
    EXTRA_TIME = 'ET'
    PENALTY = 'P'
    FINISHED = 'FT'
    POSTPONED = 'PST'
    CANCELLED = 'CANC'
    ABANDONED = 'ABD'
    
    @staticmethod
    def is_live(status: str) -> bool:
        """Maç canlı mı?"""
        live_statuses = ['1H', '2H', 'HT', 'ET', 'P']
        return status in live_statuses
    
    @staticmethod
    def is_finished(status: str) -> bool:
        """Maç bitti mi?"""
        finished_statuses = ['FT', 'AET', 'PEN']
        return status in finished_statuses
    
    @staticmethod
    def get_status_emoji(status: str) -> str:
        """Durum için emoji döndür"""
        emoji_map = {
            'NS': '🕐',
            '1H': '🔴',
            'HT': '⏸️',
            '2H': '🔴',
            'FT': '✅',
            'PST': '⏰',
            'CANC': '❌',
        }
        return emoji_map.get(status, '⚽')
