import requests
import datetime
import json


class NaverLineupCrawler:
    """네이버 스포츠 API에서 라인업 정보를 가져오는 크롤러"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'Referer': 'https://m.sports.naver.com',
            'Origin': 'https://m.sports.naver.com'
        }
    
    def get_naver_lineup(self, game_id):
        """네이버 스포츠 API에서 라인업 정보 가져오기"""
        api_url = f"https://api-gw.sports.naver.com/schedule/games/{game_id}/preview"
        
        # Referer 헤더 업데이트
        self.headers['Referer'] = f'https://m.sports.naver.com/game/{game_id}/lineup'
        
        print(f"API URL 호출: {api_url}")
        response = requests.get(api_url, headers=self.headers)
        
        if response.status_code != 200:
            print(f"API 요청 실패: 상태 코드 {response.status_code}")
            return None
        
        # JSON 응답 파싱
        data = response.json()
        
        # 응답 코드 확인
        if data.get('code') != 200 or not data.get('success', False):
            print(f"API 오류: {data.get('message', '알 수 없는 오류')}")
            return None
        
        return self.extract_lineup_from_preview(data, game_id)
    
    def extract_lineup_from_preview(self, data, game_id):
        """Preview API 응답에서 라인업 정보 추출"""
        if 'result' not in data or 'previewData' not in data['result']:
            print("API 응답에 필요한 데이터가 없습니다.")
            return None
        
        preview_data = data['result']['previewData']
        
        # 게임 정보
        game_info = preview_data.get('gameInfo', {})
        away_team_name = game_info.get('aName', '원정팀')
        away_team_full = game_info.get('aFullName', f"{away_team_name}")
        home_team_name = game_info.get('hName', '홈팀')
        home_team_full = game_info.get('hFullName', f"{home_team_name}")
        stadium = game_info.get('stadium', '')
        game_time = game_info.get('gtime', '')
        
        # 경기 날짜 (yyyymmdd 형식)
        game_date = game_info.get('gdate', '')
        formatted_date = ''
        if game_date:
            game_date_str = str(game_date)
            if len(game_date_str) == 8:
                formatted_date = f"{game_date_str[:4]}-{game_date_str[4:6]}-{game_date_str[6:8]}"
        
        # 기본 결과 구조 설정
        result = {
            "경기ID": game_id,
            "경기": f"{away_team_name} vs {home_team_name}",
            "원정팀": {
                "팀명": away_team_name,
                "팀풀네임": away_team_full,
                "선발투수": "정보 없음",
                "라인업": []
            },
            "홈팀": {
                "팀명": home_team_name,
                "팀풀네임": home_team_full,
                "선발투수": "정보 없음",
                "라인업": []
            },
            "경기장": stadium,
            "경기시간": game_time,
            "날짜": formatted_date or datetime.datetime.now().strftime("%Y-%m-%d")
        }
        
        # 선발 투수 정보
        if 'awayStarter' in preview_data and 'playerInfo' in preview_data['awayStarter']:
            result["원정팀"]["선발투수"] = preview_data['awayStarter']['playerInfo'].get('name', '정보 없음')
        
        if 'homeStarter' in preview_data and 'playerInfo' in preview_data['homeStarter']:
            result["홈팀"]["선발투수"] = preview_data['homeStarter']['playerInfo'].get('name', '정보 없음')
        
        # 원정팀 라인업
        if 'awayTeamLineUp' in preview_data and 'fullLineUp' in preview_data['awayTeamLineUp']:
            away_lineup = preview_data['awayTeamLineUp']['fullLineUp']
            
            # 선발투수는 batorder가 없으므로 제외
            for player in away_lineup:
                if 'batorder' in player:
                    result["원정팀"]["라인업"].append({
                        "순서": str(player.get('batorder', '')),
                        "포지션": player.get('positionName', ''),
                        "이름": player.get('playerName', ''),
                        "타격": player.get('batsThrows', ''),
                        "등번호": player.get('backnum', '')
                    })
        
        # 홈팀 라인업
        if 'homeTeamLineUp' in preview_data and 'fullLineUp' in preview_data['homeTeamLineUp']:
            home_lineup = preview_data['homeTeamLineUp']['fullLineUp']
            
            # 선발투수는 batorder가 없으므로 제외
            for player in home_lineup:
                if 'batorder' in player:
                    result["홈팀"]["라인업"].append({
                        "순서": str(player.get('batorder', '')),
                        "포지션": player.get('positionName', ''),
                        "이름": player.get('playerName', ''),
                        "타격": player.get('batsThrows', ''),
                        "등번호": player.get('backnum', '')
                    })
        
        return result 