#!/usr/bin/env python3
"""
간단한 HTML 구조 확인 스크립트 (requests 사용)

Selenium 없이 requests로 HTML을 가져옵니다.
JavaScript 동적 로딩이 있다면 내용이 부족할 수 있습니다.
"""

import os
import requests
from bs4 import BeautifulSoup

# 테스트할 URL
TEST_YEAR = 2025
TEST_MONTH = 1

# 월별 목록 페이지
LIST_URL = f"https://www.ikpec.or.kr/m2/sub2_1.asp?Year={TEST_YEAR}&Month={TEST_MONTH:02d}"

print("=" * 80)
print("신문윤리위원회 웹사이트 HTML 구조 테스트 (requests)")
print("=" * 80)

try:
    # 월별 목록 페이지 가져오기
    print(f"\n[1] 월별 목록 페이지 접근 중...")
    print(f"    URL: {LIST_URL}")

    response = requests.get(LIST_URL, timeout=10)

    # 인코딩 자동 감지
    if response.encoding != response.apparent_encoding:
        print(f"    인코딩 감지: {response.apparent_encoding}")
        response.encoding = response.apparent_encoding

    print(f"✓ 페이지 가져오기 성공")
    print(f"  상태 코드: {response.status_code}")
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

        # 첫 번째 심의 페이지 가져오기
        print(f"\n[4] 첫 번째 심의 상세 페이지 접근 중...")
        first_url = decision_links[0]['href']
        print(f"    URL: {first_url[:100]}...")

        detail_response = requests.get(first_url, timeout=10)
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
            print(f"\n  첫 번째 테이블 내용 (앞 500자):")
            table_text = tables[0].get_text(separator=' | ', strip=True)[:500]
            print(f"    {table_text}...")

        # 텍스트 내용 미리보기
        print(f"\n  페이지 텍스트 내용 (앞 500자):")
        print(f"    {body_text[:500]}...")

    else:
        print("\n⚠ 심의 결정 링크를 찾지 못했습니다.")
        print("  JavaScript 동적 로딩이 필요할 수 있습니다.")
        print("  또는 페이지 구조가 예상과 다를 수 있습니다.")

        # HTML 내용 일부 출력
        print(f"\n  HTML 내용 (앞 1000자):")
        print(response.text[:1000])

    print("\n" + "=" * 80)
    print("테스트 완료!")
    print("=" * 80)
    print("\n다음 파일들이 생성되었습니다:")
    print(f"  1. {list_file} - 월별 목록 페이지 HTML")
    if decision_links:
        print(f"  2. {detail_file} - 심의 상세 페이지 HTML")
        print(f"  3. {text_file} - 심의 상세 페이지 텍스트")
    print("\n이 파일들을 열어서 HTML 구조를 확인하세요.")

except requests.exceptions.RequestException as e:
    print(f"\n❌ 네트워크 오류: {e}")
except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()
