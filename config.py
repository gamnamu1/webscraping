"""
설정 파일
웹사이트 URL, 크롤링 대상 연도/월 등을 설정합니다.

[수정 사항]
- 월별 목록 페이지 URL을 직접 지정하는 방식으로 변경
- DecideBaseNo를 포함한 정확한 URL 사용
"""
import random

# 신문윤리위원회 웹사이트 기본 URL
BASE_URL = "https://www.ikpec.or.kr"

# 개별 심의 페이지 URL 패턴
DECISION_DETAIL_URL = f"{BASE_URL}/m2/sub2_1_1.asp"

# 크롤링 대상 월별 목록 페이지 URL
# 형식: (연도, 월, 해당 월의 목록 페이지 URL)
# 주의: 2019년, 2020년, 2021년, 2022년 모두 8월은 심의가 없음
TARGET_MONTH_URLS = [
    # 2019년
    (2019, 1, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2019&DecideBaseNo=Y20190109"),
    (2019, 2, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2019&DecideBaseNo=Y20190213"),
    (2019, 3, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2019&DecideBaseNo=Y20190313"),
    (2019, 4, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2019&DecideBaseNo=Y20190410"),
    (2019, 5, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2019&DecideBaseNo=Y20190508"),
    (2019, 6, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2019&DecideBaseNo=Y20190612"),
    (2019, 7, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2019&DecideBaseNo=Y20190710"),
    # 2019년 8월 없음
    (2019, 9, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2019&DecideBaseNo=Y20190910"),
    (2019, 10, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2019&DecideBaseNo=Y20191008"),
    (2019, 11, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2019&DecideBaseNo=Y20191113"),
    (2019, 12, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2019&DecideBaseNo=Y20191211"),
    
    # 2020년
    (2020, 1, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2020&DecideBaseNo=Y20200108"),
    (2020, 2, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2020&DecideBaseNo=Y20200212"),
    (2020, 3, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2020&DecideBaseNo=Y20200325"),
    (2020, 4, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2020&DecideBaseNo=Y20200408"),
    (2020, 5, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2020&DecideBaseNo=Y20200513"),
    (2020, 6, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2020&DecideBaseNo=Y20200610"),
    (2020, 7, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2020&DecideBaseNo=Y20200708"),
    # 2020년 8월 없음
    (2020, 9, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2020&DecideBaseNo=Y20200924"),
    (2020, 10, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2020&DecideBaseNo=Y20201014"),
    (2020, 11, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2020&DecideBaseNo=Y20201111"),
    (2020, 12, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2020&DecideBaseNo=Y20201209"),
    
    # 2021년
    (2021, 1, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2021&DecideBaseNo=Y20210113"),
    (2021, 2, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2021&DecideBaseNo=Y20210209"),
    (2021, 3, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2021&DecideBaseNo=Y20210310"),
    (2021, 4, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2021&DecideBaseNo=Y20210414"),
    (2021, 5, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2021&DecideBaseNo=Y20210512"),
    (2021, 6, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2021&DecideBaseNo=Y20210609"),
    (2021, 7, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2021&DecideBaseNo=Y20210714"),
    # 2021년 8월 없음
    (2021, 9, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2021&DecideBaseNo=Y20210908"),
    (2021, 10, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2021&DecideBaseNo=Y20211013"),
    (2021, 11, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2021&DecideBaseNo=Y20211110"),
    (2021, 12, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2021&DecideBaseNo=Y20211208"),
    
    # 2022년
    (2022, 1, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2022&DecideBaseNo=Y20220112"),
    (2022, 2, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2022&DecideBaseNo=Y20220209"),
    (2022, 3, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2022&DecideBaseNo=Y20220316"),
    (2022, 4, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2022&DecideBaseNo=Y20220413"),
    (2022, 5, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2022&DecideBaseNo=Y20220511"),
    (2022, 6, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2022&DecideBaseNo=Y20220608"),
    (2022, 7, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2022&DecideBaseNo=Y20220713"),
    # 2022년 8월 없음
    (2022, 9, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2022&DecideBaseNo=Y20220907"),
    (2022, 10, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2022&DecideBaseNo=Y20221012"),
    (2022, 11, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2022&DecideBaseNo=Y20221109"),
    (2022, 12, "https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2022&DecideBaseNo=Y20221207"),
]

# Selenium 설정
SELENIUM_TIMEOUT = 10  # 페이지 로딩 대기 시간 (초)
HEADLESS_MODE = True   # True: 브라우저 창을 보이지 않게 실행

# 출력 디렉토리
OUTPUT_DIR = "output"

# 요청 간 대기 시간 설정 (초) - 서버 부하 방지 및 탐지 회피
# (최소, 최대) 초 사이의 임의의 시간만큼 대기합니다.
REQUEST_DELAY_RANGE = (2.0, 4.0)  # 2초에서 4초 사이 랜덤 대기

# 인코딩 설정
ENCODING = "euc-kr"  # 신문윤리위원회 웹사이트는 EUC-KR 사용


def get_random_delay():
    """
    설정된 범위 내에서 랜덤한 대기 시간을 반환합니다.
    
    Returns:
        float: REQUEST_DELAY_RANGE 범위 내의 랜덤한 대기 시간 (초)
    """
    return random.uniform(REQUEST_DELAY_RANGE[0], REQUEST_DELAY_RANGE[1])
