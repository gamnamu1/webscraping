#!/usr/bin/env python3
"""
헤더를 추가하여 HTML 구조 확인

User-Agent와 기타 헤더를 추가하여 봇 차단을 우회합니다.
"""

import os
import requests
from bs4 import BeautifulSoup

# 테스트할 URL
TEST_YEAR = 2025
TEST_MONTH = 1

# 월별 목록 페이지
LIST_URL = f"https://www.ikpec.or.kr/m2/sub2_1.asp?Year={TEST_YEAR}&Month={TEST_MONTH:02d}"

# 브라우저를 모방한 헤더
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.ikpec.or.kr/',
}

print("=" * 80)
print("신문윤리위원회 웹사이트 HTML 구조 테스트 (헤더 추가)")
print("=" * 80)

try:
    # 월별 목록 페이지 가져오기
    print(f"\n[1] 월별 목록 페이지 접근 중...")
    print(f"    URL: {LIST_URL}")

    response = requests.get(LIST_URL, headers=HEADERS, timeout=10)

    print(f"✓ 응답 수신")
    print(f"  상태 코드: {response.status_code}")

    if response.status_code == 403:
        print("❌ 403 Access Denied - 웹사이트가 접근을 차단했습니다.")
        print("   Selenium + Chrome이 필요할 수 있습니다.")
        exit(1)

    # 인코딩 자동 감지
    if response.encoding != response.apparent_encoding:
        print(f"  인코딩 감지: {response.apparent_encoding}")
        response.encoding = response.apparent_encoding

    print(f"  인코딩: {response.encoding}")
    print(f"  콘텐츠 크기: {len(response.text):,} bytes")

    # HTML 파일로 저장
    os.makedirs('test_output', exist_ok=True)

    list_file = f'test_output/list_page_{TEST_YEAR}_{TEST_MONTH:02d}.html'
    with open(list_file, 'w', encoding='utf-8') as f:
        f.write(response.text)

    print(f"✓ HTML 저장: {list_file}")

    # BeautifulSoup으로 파싱
    print(f"\n[2] HTML 파싱 중...")
    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목 확인
    title = soup.find('title')
    if title:
        print(f"  페이지 제목: {title.get_text(strip=True)}")

    # 링크 찾기
    all_links = soup.find_all('a')
    print(f"  전체 링크 수: {len(all_links)}")

    # sub2_1_1.asp 링크 찾기 (개별 심의 페이지)
    decision_links = []
    for link in all_links:
        href = link.get('href', '')
        if 'sub2_1_1.asp' in href:
            text = link.get_text(strip=True)
            if text:
                # 상대 경로를 절대 경로로 변환
                if not href.startswith('http'):
                    if href.startswith('/'):
                        href = 'https://www.ikpec.or.kr' + href
                    else:
                        href = 'https://www.ikpec.or.kr/m2/' + href

                decision_links.append({
                    'text': text,
                    'href': href
                })

    print(f"\n[3] 심의 결정 링크 발견: {len(decision_links)}건")

    if decision_links:
        # 처음 5개 링크 출력
        print("\n  처음 5개 링크 샘플:")
        for i, link_info in enumerate(decision_links[:5], 1):
            print(f"    {i}. {link_info['text'][:60]}")
            print(f"       → {link_info['href'][:100]}")

        # 링크 정보를 파일로 저장
        links_file = 'test_output/decision_links.txt'
        with open(links_file, 'w', encoding='utf-8') as f:
            for i, link_info in enumerate(decision_links, 1):
                f.write(f"{i}. {link_info['text']}\n")
                f.write(f"   {link_info['href']}\n\n")
        print(f"✓ 링크 목록 저장: {links_file}")

        # 첫 번째 심의 페이지 가져오기
        print(f"\n[4] 첫 번째 심의 상세 페이지 접근 중...")
        first_url = decision_links[0]['href']
        print(f"    URL: {first_url[:100]}...")

        detail_response = requests.get(first_url, headers=HEADERS, timeout=10)
        detail_response.encoding = detail_response.apparent_encoding

        print(f"✓ 상세 페이지 가져오기 성공")
        print(f"  상태 코드: {detail_response.status_code}")
        print(f"  인코딩: {detail_response.encoding}")
        print(f"  콘텐츠 크기: {len(detail_response.text):,} bytes")

        # HTML 파일로 저장
        detail_file = 'test_output/detail_page_sample.html'
        with open(detail_file, 'w', encoding='utf-8') as f:
            f.write(detail_response.text)

        print(f"✓ HTML 저장: {detail_file}")

        # 상세 페이지 파싱
        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

        # 텍스트만 추출
        body_text = detail_soup.get_text(separator='\n', strip=True)
        text_file = 'test_output/detail_page_text.txt'
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(body_text)

        print(f"✓ 텍스트 추출: {text_file}")
        print(f"  텍스트 길이: {len(body_text):,} chars")

        # HTML 구조 분석
        print(f"\n[5] HTML 구조 분석:")
        tables = detail_soup.find_all('table')
        print(f"  테이블 개수: {len(tables)}")

        divs = detail_soup.find_all('div')
        print(f"  DIV 개수: {len(divs)}")

        # 첫 번째 테이블의 내용 미리보기 (있다면)
        if tables:
            print(f"\n  첫 번째 테이블 구조 분석:")
            rows = tables[0].find_all('tr')
            print(f"    행(tr) 개수: {len(rows)}")
            if rows:
                print(f"    첫 번째 행 내용:")
                first_row_text = rows[0].get_text(separator=' | ', strip=True)
                print(f"      {first_row_text[:200]}")

        # 텍스트 내용 미리보기
        print(f"\n  페이지 텍스트 내용 (앞 800자):")
        print("  " + "=" * 76)
        preview_lines = body_text[:800].split('\n')
        for line in preview_lines:
            if line.strip():
                print(f"  {line[:76]}")
        print("  " + "=" * 76)

    else:
        print("\n⚠ 심의 결정 링크를 찾지 못했습니다.")
        print("  페이지 구조 분석을 위해 HTML 내용을 확인하세요.")

        # HTML 구조 간단 분석
        print(f"\n  HTML 구조:")
        tables = soup.find_all('table')
        print(f"    테이블 개수: {len(tables)}")
        divs = soup.find_all('div')
        print(f"    DIV 개수: {len(divs)}")

        # HTML 내용 일부 출력
        print(f"\n  HTML 내용 (앞 2000자):")
        print("  " + "=" * 76)
        print(response.text[:2000])
        print("  " + "=" * 76)

    print("\n" + "=" * 80)
    print("테스트 완료!")
    print("=" * 80)
    print("\n생성된 파일:")
    print(f"  1. {list_file} - 월별 목록 페이지 HTML")
    if decision_links:
        print(f"  2. {detail_file} - 심의 상세 페이지 HTML")
        print(f"  3. {text_file} - 심의 상세 페이지 텍스트")
        print(f"  4. {links_file} - 심의 링크 목록")

except requests.exceptions.RequestException as e:
    print(f"\n❌ 네트워크 오류: {e}")
except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()
