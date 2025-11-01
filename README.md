# 신문윤리위원회 심의결정 스크레이퍼

신문윤리위원회(https://www.ikpec.or.kr) 웹사이트에서 월별 심의결정 내용을 자동으로 추출하여 마크다운 파일로 저장하는 프로그램입니다.

## 주요 기능

- 월별 심의결정 목록 자동 수집
- 개별 심의 페이지 상세 내용 추출
- 마크다운(MD) 형식으로 변환 및 저장
- JavaScript 동적 로딩 지원 (Selenium 사용)
- EUC-KR 인코딩 자동 처리

## 기술 스택

- **Python 3.8+**
- **Selenium**: 브라우저 자동화, JavaScript 렌더링 처리
- **BeautifulSoup4**: HTML 파싱
- **ChromeDriver**: Chrome 브라우저 제어

## 설치 방법

### 1. 필수 요구사항

- Python 3.8 이상
- Chrome 브라우저 (최신 버전 권장)

### 2. 저장소 클론 및 패키지 설치

```bash
# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# 필수 패키지 설치
pip install -r requirements.txt
```

## 사용 방법

### 1. 설정 파일 수정

`config.py` 파일을 열어 크롤링할 연도와 월을 설정합니다:

```python
# 크롤링 대상 연도 및 월
TARGET_PERIODS = [
    (2025, 1),   # 2025년 1월
    (2025, 2),   # 2025년 2월
    (2024, 12),  # 2024년 12월
    # 필요한 기간을 추가하세요
]

# 기타 설정
HEADLESS_MODE = True       # False로 설정하면 브라우저 창이 보입니다
REQUEST_DELAY = 1.0        # 요청 간 대기 시간 (초)
SELENIUM_TIMEOUT = 10      # 페이지 로딩 타임아웃 (초)
```

### 2. 프로그램 실행

```bash
python main.py
```

### 3. 실행 결과

프로그램이 실행되면:

1. Chrome 브라우저가 자동으로 실행됩니다 (headless 모드에서는 보이지 않음)
2. 설정한 월별 페이지에 접근하여 심의 목록을 가져옵니다
3. 각 심의 페이지를 순회하며 상세 내용을 추출합니다
4. 마크다운 파일로 변환하여 `output/` 디렉토리에 저장합니다

### 4. 출력 파일 구조

```
output/
├── 2025/
│   ├── 01/
│   │   ├── INDEX_2025_01.md          # 월별 인덱스 파일
│   │   ├── 2025-1234_심의제목1.md
│   │   ├── 2025-1235_심의제목2.md
│   │   └── ...
│   └── 02/
│       ├── INDEX_2025_02.md
│       └── ...
└── scraper.log                        # 실행 로그
```

## 파일 설명

- **main.py**: 메인 실행 스크립트
- **config.py**: 설정 파일 (URL, 크롤링 대상 등)
- **scraper.py**: Selenium 기반 웹 스크레이퍼
- **parser.py**: HTML 파싱 로직
- **markdown_writer.py**: 마크다운 파일 생성
- **requirements.txt**: 필요한 Python 패키지 목록

## 문제 해결

### Chrome 브라우저 버전 오류

```
WebDriver 버전이 맞지 않습니다
```

**해결 방법**: `webdriver-manager`가 자동으로 호환되는 ChromeDriver를 다운로드합니다. Chrome 브라우저를 최신 버전으로 업데이트하세요.

### 인코딩 문제 (한글 깨짐)

신문윤리위원회 웹사이트는 EUC-KR 인코딩을 사용합니다. Selenium이 자동으로 처리하지만, 문제가 발생하면 `config.py`의 `ENCODING` 설정을 확인하세요.

### 페이지 로딩 타임아웃

```
TimeoutException: 페이지 로딩 시간 초과
```

**해결 방법**: `config.py`에서 `SELENIUM_TIMEOUT` 값을 늘립니다:

```python
SELENIUM_TIMEOUT = 20  # 10 → 20초로 증가
```

### 너무 많은 요청으로 차단됨

**해결 방법**: `config.py`에서 `REQUEST_DELAY`를 늘립니다:

```python
REQUEST_DELAY = 2.0  # 1.0 → 2.0초로 증가
```

## 주의사항

1. **서버 부하**: 과도한 요청은 서버에 부담을 줄 수 있습니다. `REQUEST_DELAY` 설정을 적절히 유지하세요.
2. **개인 사용**: 이 프로그램은 개인적인 학습 및 정보 수집 목적으로만 사용하세요.
3. **웹사이트 변경**: 웹사이트 구조가 변경되면 `parser.py`의 HTML 파싱 로직을 수정해야 할 수 있습니다.
4. **로봇 배제 표준**: 웹사이트의 `robots.txt`를 확인하고 준수하세요.

## 라이선스

개인 사용 목적의 프로그램입니다.

## 버전 히스토리

- **v1.0.0** (2025-01-29)
  - 초기 버전 릴리스
  - Selenium 기반 스크레이핑
  - EUC-KR 인코딩 지원
  - 마크다운 파일 생성

## 기여

버그 리포트나 개선 제안은 이슈 트래커를 통해 제출해주세요.

## 문의

문제가 발생하면 로그 파일(`scraper.log`)을 확인하세요. 자세한 오류 정보가 기록됩니다.