import logging
import os
from datetime import datetime


def setup_logger(log_level=logging.INFO):
    """로깅 설정"""
    # 로그 디렉토리 생성
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 로그 파일명 생성 (날짜 기반)
    today = datetime.now().strftime('%Y%m%d')
    log_file = f"{log_dir}/kbo_lineup_{today}.log"
    
    # 로거 설정
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # 기존 핸들러 제거
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    
    # 파일 핸들러 설정
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_format = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    file_handler.setFormatter(file_format)
    logger.addHandler(file_handler)
    
    # 콘솔 핸들러 설정
    console_handler = logging.StreamHandler()
    console_format = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    return logger
