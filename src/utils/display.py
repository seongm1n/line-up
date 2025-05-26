import pandas as pd


def display_lineup(lineup):
    """라인업 정보 표시"""
    if not lineup:
        print("라인업 정보를 가져오지 못했습니다.")
        return

    # 경기 정보 헤더
    print(f"\n{'=' * 50}")
    print(f"경기: {lineup['경기']} ({lineup['날짜']} {lineup['경기시간']})")
    print(f"경기장: {lineup['경기장']}")
    print(f"{'=' * 50}")

    # 원정팀 정보
    print(f"\n[{lineup['원정팀']['팀풀네임']}]")
    print(f"선발투수: {lineup['원정팀']['선발투수']}")
    print("\n타자 라인업:")
    if lineup['원정팀']['라인업']:
        # 타순으로 정렬
        sorted_lineup = sorted(lineup['원정팀']['라인업'], key=lambda x: int(x['순서']))
        df_away = pd.DataFrame(sorted_lineup)
        df_away = df_away[['순서', '포지션', '이름', '타격', '등번호']]  # 열 순서 지정
        print(df_away.to_string(index=False))
    else:
        print("라인업 정보가 없습니다.")

    # 홈팀 정보
    print(f"\n[{lineup['홈팀']['팀풀네임']}]")
    print(f"선발투수: {lineup['홈팀']['선발투수']}")
    print("\n타자 라인업:")
    if lineup['홈팀']['라인업']:
        # 타순으로 정렬
        sorted_lineup = sorted(lineup['홈팀']['라인업'], key=lambda x: int(x['순서']))
        df_home = pd.DataFrame(sorted_lineup)
        df_home = df_home[['순서', '포지션', '이름', '타격', '등번호']]  # 열 순서 지정
        print(df_home.to_string(index=False))
    else:
        print("라인업 정보가 없습니다.")

    print(f"\n{'=' * 50}") 