import os
import json


def save_to_file(lineup, output_dir=None):
    """라인업 정보 파일 저장"""
    if not lineup:
        print("저장할 라인업 정보가 없습니다.")
        return

    # 출력 디렉토리 설정
    if not output_dir:
        output_dir = 'lineups'

    # 디렉토리가 없으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 파일명 생성
    date_str = lineup['날짜'].replace('-', '')
    away_team = lineup['원정팀']['팀명']
    home_team = lineup['홈팀']['팀명']
    filename = f"{output_dir}/{date_str}_{away_team}_vs_{home_team}.json"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(lineup, f, ensure_ascii=False, indent=2)

        print(f"\n선발 명단이 {filename} 파일로 저장되었습니다.")
        return filename
    except Exception as e:
        print(f"\n파일 저장 중 오류가 발생했습니다: {str(e)}")
        return None 