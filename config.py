"""
설정 파일
웹사이트 URL, 크롤링 대상 연도/월 등을 설정합니다.
"""

# 신문윤리위원회 웹사이트 기본 URL
BASE_URL = "https://www.ikpec.or.kr"

# 심의결정현황 페이지 URL 패턴
# 예: https://www.ikpec.or.kr/m2/sub2_1.asp?Year=2025&Month=01
DECISION_LIST_URL = f"{BASE_URL}/m2/sub2_1.asp"

# 개별 심의 페이지 URL 패턴
# 예: https://www.ikpec.or.kr/m2/sub2_1_1.asp?Year=2025&DecideBaseNo=Y20250709&DecideNo=2025-1268
DECISION_DETAIL_URL = f"{BASE_URL}/m2/sub2_1_1.asp"

# 크롤링 대상 연도 및 월
# 형식: [(연도, 월), ...]
TARGET_PERIODS = [
    (2025, 1),   # 2025년 1월
    (2025, 2),   # 2025년 2월
    # 필요한 기간을 추가하세요
]

# Selenium 설정
SELENIUM_TIMEOUT = 10  # 페이지 로딩 대기 시간 (초)
HEADLESS_MODE = True   # True: 브라우저 창을 보이지 않게 실행

# 출력 디렉토리
OUTPUT_DIR = "output"

# 요청 간 대기 시간 (초) - 서버 부하 방지
REQUEST_DELAY = 1.0

# 인코딩 설정
ENCODING = "euc-kr"  # 신문윤리위원회 웹사이트는 EUC-KR 사용
