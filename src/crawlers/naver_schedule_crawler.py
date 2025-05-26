import requests
import datetime
from typing import List, Dict, Optional


class NaverScheduleCrawler:
    """네이버 스포츠 API에서 KBO 경기 일정을 가져오는 크롤러"""
    
    BASE_URL = "https://api-gw.sports.naver.com/schedule/calendar"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'Referer': 'https://m.sports.naver.com',
            'Origin': 'https://m.sports.naver.com'
        }
    
    def get_monthly_schedule(self, date: Optional[datetime.date] = None) -> Dict:
        """특정 날짜가 속한 월의 경기 일정을 가져옵니다."""
        if date is None:
            date = datetime.date.today()
            
        date_str = date.strftime("%Y-%m-%d")
        
        params = {
            'upperCategoryId': 'kbaseball',
            'categoryIds': ',kbo,kbaseballetc,premier12,apbc',
            'date': date_str
        }
        
        print(f"월간 경기 일정 API 호출: {date_str[:7]} (기준일: {date_str})")
        response = requests.get(self.BASE_URL, params=params, headers=self.headers)
        
        if response.status_code != 200:
            print(f"API 요청 실패: 상태 코드 {response.status_code}")
            return {}
        
        data = response.json()
        
        if data.get('code') != 200 or not data.get('success', False):
            print(f"API 오류: {data.get('message', '알 수 없는 오류')}")
            return {}
        
        return data
    
    def get_daily_games(self, date: Optional[datetime.date] = None) -> List[Dict]:
        """특정 날짜의 KBO 경기 목록을 가져옵니다."""
        if date is None:
            date = datetime.date.today()
            
        date_str = date.strftime("%Y-%m-%d")
        monthly_data = self.get_monthly_schedule(date)
        
        if not monthly_data or 'result' not in monthly_data or 'dates' not in monthly_data['result']:
            return []
        
        # 해당 날짜의 경기 정보 찾기
        daily_games = []
        for day_data in monthly_data['result']['dates']:
            if day_data['ymd'] == date_str:
                # KBO 경기만 필터링 (gameId가 특정 패턴을 가진 경기)
                kbo_games = []
                for game_info in day_data['gameInfos']:
                    game_id = game_info['gameId']
                    # KBO1, SPORTSN1 등은 실제 경기가 아닌 정보성 컨텐츠인 경우가 많음
                    if (len(game_id) > 8 and 
                        game_id.endswith('02025') and 
                        game_info['homeTeamCode'] and 
                        game_info['awayTeamCode']):
                        kbo_games.append({
                            'game_id': game_id,
                            'home_team': game_info['homeTeamCode'],
                            'away_team': game_info['awayTeamCode'],
                            'status': game_info['statusCode'],
                            'date': date_str
                        })
                
                daily_games = kbo_games
                break
                
        return daily_games 