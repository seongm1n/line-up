# KBO 라인업 크롤러

네이버 스포츠 API를 이용하여 KBO 경기의 라인업 정보를 자동으로 크롤링하는 서비스입니다.

## 기능

- 특정 경기 ID로 라인업 정보 조회
- 라인업 정보를 콘솔에 표시
- 라인업 정보를 JSON 파일로 저장

## 사용 방법

### 설치

1. 필요 패키지 설치:
```
pip install -r requirements.txt
```

### 실행

특정 경기 ID로 라인업 정보 가져오기:
```
python main.py 게임ID
```

예시:
```
python main.py 20250525LTHH02025
```

출력 디렉토리 지정 (기본값: lineups):
```
python main.py 게임ID -o 출력디렉토리
```

### 구조

```
KBOLineUp/
├── main.py               # 메인 실행 파일
├── requirements.txt      # 필요 패키지 목록
├── src/                  # 소스 코드
│   ├── crawlers/         # 크롤러 모듈
│   │   ├── __init__.py
│   │   ├── kbo_lineup_crawler.py  # KBO 공식 사이트 크롤러 (미구현)
│   │   └── naver_lineup_crawler.py # 네이버 스포츠 크롤러
│   ├── models/           # 데이터 모델
│   │   ├── __init__.py
│   │   └── lineup.py     # 라인업 데이터 모델
│   └── utils/            # 유틸리티 함수
│       ├── __init__.py
│       ├── display.py    # 콘솔 출력 기능
│       ├── file_handler.py # 파일 저장 기능
│       └── logger.py     # 로깅 기능
```

## TODO

- 특정 날짜의 모든 경기 라인업 조회 기능 구현
- KBO 공식 사이트 크롤링 기능 구현
- 웹 인터페이스 추가
- 데이터베이스 연동 