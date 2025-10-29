#!/usr/bin/env python3
"""
웹사이트 HTML 구조 확인용 테스트 스크립트

실제 웹사이트에 접속하여 HTML 구조를 파일로 저장합니다.
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 테스트할 URL
TEST_YEAR = 2025
TEST_MONTH = 1

# 월별 목록 페이지
LIST_URL = f"https://www.ikpec.or.kr/m2/sub2_1.asp?Year={TEST_YEAR}&Month={TEST_MONTH:02d}"

print("=" * 80)
print("신문윤리위원회 웹사이트 HTML 구조 테스트")
print("=" * 80)

# Selenium 설정
print("\n[1] Chrome WebDriver 설정 중...")
chrome_options = Options()
chrome_options.add_argument('--headless=new')  # 최신 headless 모드
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--lang=ko-KR')
chrome_options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/120.0.0.0 Safari/537.36'
)

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    print("✓ WebDriver 설정 완료")

    # 월별 목록 페이지 접근
    print(f"\n[2] 월별 목록 페이지 접근 중...")
    print(f"    URL: {LIST_URL}")
    driver.get(LIST_URL)

    # JavaScript 렌더링 대기
    time.sleep(3)

    # 페이지 소스 저장
    list_html = driver.page_source

    # HTML 파일로 저장
    os.makedirs('test_output', exist_ok=True)

    list_file = f'test_output/list_page_{TEST_YEAR}_{TEST_MONTH:02d}.html'
    with open(list_file, 'w', encoding='utf-8') as f:
        f.write(list_html)

    print(f"✓ 월별 목록 페이지 HTML 저장: {list_file}")
    print(f"  파일 크기: {len(list_html):,} bytes")

    # 페이지 제목 확인
    print(f"  페이지 제목: {driver.title}")

    # 링크 개수 확인
    all_links = driver.find_elements(By.TAG_NAME, 'a')
    print(f"  전체 링크 수: {len(all_links)}")

    # sub2_1_1.asp 링크 찾기 (개별 심의 페이지)
    decision_links = []
    for link in all_links:
        href = link.get_attribute('href')
        if href and 'sub2_1_1.asp' in href:
            text = link.text.strip()
            if text:
                decision_links.append({
                    'text': text,
                    'href': href
                })

    print(f"\n[3] 심의 결정 링크 발견: {len(decision_links)}건")

    if decision_links:
        # 처음 3개 링크 출력
        print("\n  처음 3개 링크 샘플:")
        for i, link_info in enumerate(decision_links[:3], 1):
            print(f"    {i}. {link_info['text'][:50]}...")
            print(f"       → {link_info['href']}")

        # 첫 번째 심의 페이지에 접근
        print(f"\n[4] 첫 번째 심의 상세 페이지 접근 중...")
        first_url = decision_links[0]['href']
        print(f"    URL: {first_url[:80]}...")

        driver.get(first_url)
        time.sleep(3)

        detail_html = driver.page_source

        detail_file = 'test_output/detail_page_sample.html'
        with open(detail_file, 'w', encoding='utf-8') as f:
            f.write(detail_html)

        print(f"✓ 심의 상세 페이지 HTML 저장: {detail_file}")
        print(f"  파일 크기: {len(detail_html):,} bytes")
        print(f"  페이지 제목: {driver.title}")

        # 텍스트만 추출
        body_text = driver.find_element(By.TAG_NAME, 'body').text
        text_file = 'test_output/detail_page_text.txt'
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(body_text)

        print(f"✓ 텍스트만 추출: {text_file}")
        print(f"  텍스트 길이: {len(body_text):,} chars")

        # 테이블 확인
        tables = driver.find_elements(By.TAG_NAME, 'table')
        print(f"\n[5] HTML 구조 분석:")
        print(f"  테이블 개수: {len(tables)}")

        # div 확인
        divs = driver.find_elements(By.TAG_NAME, 'div')
        print(f"  DIV 개수: {len(divs)}")

    else:
        print("\n⚠ 심의 결정 링크를 찾지 못했습니다.")
        print("  페이지 구조가 예상과 다를 수 있습니다.")

    print("\n" + "=" * 80)
    print("테스트 완료!")
    print("=" * 80)
    print("\n다음 파일들이 생성되었습니다:")
    print(f"  1. {list_file} - 월별 목록 페이지 HTML")
    if decision_links:
        print(f"  2. {detail_file} - 심의 상세 페이지 HTML")
        print(f"  3. {text_file} - 심의 상세 페이지 텍스트")
    print("\n이 파일들을 열어서 HTML 구조를 확인하세요.")
    print("특히 다음을 확인하세요:")
    print("  - 목록 페이지: 어떤 태그로 심의 리스트가 구성되어 있는지")
    print("  - 상세 페이지: 결정번호, 제목, 본문 등이 어떤 태그에 있는지")

except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

finally:
    if 'driver' in locals():
        driver.quit()
        print("\n✓ WebDriver 종료")
