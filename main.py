import argparse
import logging
import datetime
from src.crawlers.naver_lineup_crawler import NaverLineupCrawler
from src.crawlers.naver_schedule_crawler import NaverScheduleCrawler
from src.utils.display import display_lineup
from src.utils.file_handler import save_to_file
from src.utils.logger import setup_logger


def get_today_games_lineups(output_dir=None):
    """오늘 날짜의 모든 KBO 경기 라인업을 가져옵니다."""
    logger = logging.getLogger()
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    
    logger.info(f"오늘({date_str}) 모든 KBO 경기 라인업 정보 가져오기")
    
    # 경기 일정 크롤러 인스턴스 생성
    schedule_crawler = NaverScheduleCrawler()
    daily_games = schedule_crawler.get_daily_games()
    
    if not daily_games:
        logger.info(f"오늘({date_str}) 예정된 KBO 경기가 없습니다.")
        return
    
    logger.info(f"오늘 총 {len(daily_games)}개의 KBO 경기가 예정되어 있습니다.")
    
    # 라인업 크롤러 인스턴스 생성
    lineup_crawler = NaverLineupCrawler()
    
    # 각 경기의 라인업 정보 가져오기
    lineups = []
    for game in daily_games:
        game_id = game['game_id']
        logger.info(f"경기 ID {game_id} 라인업 정보 가져오기")
        
        lineup = lineup_crawler.get_naver_lineup(game_id)
        if lineup:
            display_lineup(lineup)
            saved_file = save_to_file(lineup, output_dir)
            if saved_file:
                lineups.append(lineup)
    
    return lineups


def main():
    """메인 함수"""
    # 로거 설정
    logger = setup_logger()
    
    # 명령행 인자 파싱
    parser = argparse.ArgumentParser(description='네이버 스포츠에서 KBO 선발 라인업 정보 가져오기')
    parser.add_argument('game_id', nargs='?', help='게임 ID (예: 20250525LTHH02025)')
    parser.add_argument('-d', '--date', help='날짜 (YYYYMMDD 형식)')
    parser.add_argument('-o', '--output', help='출력 디렉토리')
    parser.add_argument('-t', '--today', action='store_true', help='오늘 모든 경기 라인업 정보 가져오기')
    
    args = parser.parse_args()
    
    # 오늘 모든 경기 라인업 정보 가져오기
    if args.today:
        get_today_games_lineups(args.output)
        return
    
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
    
    # 날짜가 제공되었으면 해당 날짜의 모든 경기 정보 가져오기
    elif args.date:
        try:
            # YYYYMMDD 형식의 날짜 파싱
            if len(args.date) == 8:
                date = datetime.datetime.strptime(args.date, "%Y%m%d").date()
                
                # 스케줄 크롤러 인스턴스 생성
                schedule_crawler = NaverScheduleCrawler()
                daily_games = schedule_crawler.get_daily_games(date)
                
                if not daily_games:
                    logger.info(f"{args.date} 날짜에 예정된 KBO 경기가 없습니다.")
                    return
                
                logger.info(f"{args.date} 날짜에 총 {len(daily_games)}개의 KBO 경기가 있습니다.")
                
                # 각 경기의 라인업 정보 가져오기
                for game in daily_games:
                    game_id = game['game_id']
                    logger.info(f"경기 ID {game_id} 라인업 정보 가져오기")
                    
                    lineup = crawler.get_naver_lineup(game_id)
                    if lineup:
                        display_lineup(lineup)
                        save_to_file(lineup, args.output)
            else:
                logger.error("날짜 형식이 올바르지 않습니다. YYYYMMDD 형식으로 입력해주세요.")
        except ValueError:
            logger.error("날짜 형식이 올바르지 않습니다. YYYYMMDD 형식으로 입력해주세요.")
    
    # 아무 인자도 없으면 오늘 날짜의 게임 정보 가져오기
    else:
        logger.info("오늘 날짜의 모든 게임 라인업 정보를 가져오려면 -t 또는 --today 옵션을 사용하세요.")
        logger.info("사용법: python main.py -t")
        logger.info("특정 게임 라인업: python main.py 게임ID")
        logger.info("특정 날짜 모든 게임 라인업: python main.py -d YYYYMMDD")


if __name__ == "__main__":
    main()
