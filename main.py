import argparse
import logging
from src.crawlers.naver_lineup_crawler import NaverLineupCrawler
from src.utils.display import display_lineup
from src.utils.file_handler import save_to_file
from src.utils.logger import setup_logger


def main():
    """메인 함수"""
    # 로거 설정
    logger = setup_logger()
    
    # 명령행 인자 파싱
    parser = argparse.ArgumentParser(description='네이버 스포츠에서 KBO 선발 라인업 정보 가져오기')
    parser.add_argument('game_id', nargs='?', help='게임 ID (예: 20250525LTHH02025)')
    parser.add_argument('-d', '--date', help='날짜 (YYYYMMDD 형식)')
    parser.add_argument('-o', '--output', help='출력 디렉토리')
    
    args = parser.parse_args()
    
    # 크롤러 인스턴스 생성
    crawler = NaverLineupCrawler()
    
    # 게임 ID가 직접 제공되었으면 해당 게임 정보만 가져오기
    if args.game_id:
        logger.info(f"게임 ID로 라인업 정보 가져오기: {args.game_id}")
        lineup = crawler.get_naver_lineup(args.game_id)
        
        if lineup:
            display_lineup(lineup)
            save_to_file(lineup, args.output)
        else:
            logger.error("라인업 정보를 가져오지 못했습니다.")
    
    # 날짜가 제공되었으면 해당 날짜의 모든 게임 정보 가져오기
    elif args.date:
        # 날짜의 모든 게임을 가져오는 코드는 추가 구현 필요
        logger.info(f"날짜 {args.date}의 모든 게임 라인업 정보 가져오기는 아직 구현되지 않았습니다.")
    
    # 아무 인자도 없으면 오늘 날짜의 게임 정보 가져오기
    else:
        logger.info("오늘 날짜의 모든 게임 라인업 정보 가져오기는 아직 구현되지 않았습니다.")
        logger.info("사용법: python main.py 게임ID")
        logger.info("예시: python main.py 20250525LTHH02025")

if __name__ == "__main__":
    main()
