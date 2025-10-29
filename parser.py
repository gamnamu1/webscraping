"""
HTML 파싱 모듈
BeautifulSoup을 사용하여 HTML에서 필요한 데이터를 추출합니다.
"""

from bs4 import BeautifulSoup
from typing import List, Dict, Optional


def parse_decision_list(html_content: str) -> List[Dict[str, str]]:
    """
    월별 심의 결정 목록 페이지에서 개별 심의 링크를 추출합니다.

    Args:
        html_content: 페이지의 HTML 내용

    Returns:
        심의 정보 리스트 [{'title': '...', 'url': '...', 'decision_no': '...'}, ...]
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    decisions = []

    # 실제 페이지 구조에 맞게 수정 필요
    # 일반적으로 테이블이나 리스트 형태로 되어 있을 것으로 예상

    # 예시: 테이블에서 링크 추출
    # 실제 HTML 구조를 확인하여 수정해야 함
    links = soup.find_all('a', href=lambda href: href and 'sub2_1_1.asp' in href)

    for link in links:
        title = link.get_text(strip=True)
        url = link.get('href', '')

        # 상대 경로를 절대 경로로 변환
        if url and not url.startswith('http'):
            from config import BASE_URL
            if url.startswith('/'):
                url = BASE_URL + url
            else:
                url = BASE_URL + '/' + url

        decisions.append({
            'title': title,
            'url': url,
        })

    return decisions


def parse_decision_detail(html_content: str) -> Dict[str, any]:
    """
    개별 심의 페이지에서 상세 내용을 추출합니다.

    Args:
        html_content: 페이지의 HTML 내용

    Returns:
        심의 상세 정보 딕셔너리
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # 실제 페이지 구조에 맞게 수정 필요
    detail = {
        'title': '',
        'decision_no': '',
        'decision_date': '',
        'newspaper': '',
        'article_date': '',
        'content': '',
        'decision': '',
        'reason': '',
    }

    # 제목 추출 (예시)
    title_elem = soup.find('h1') or soup.find('h2') or soup.find('title')
    if title_elem:
        detail['title'] = title_elem.get_text(strip=True)

    # 본문 내용 추출 (예시)
    # 실제 HTML 구조를 확인하여 적절한 선택자 사용
    content_area = soup.find('div', class_='content') or soup.find('div', id='content')
    if content_area:
        detail['content'] = content_area.get_text(strip=True)

    # 테이블 형태의 정보 추출 (예시)
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['th', 'td'])
            if len(cells) >= 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)

                # 키워드 매칭
                if '결정번호' in key or '의결번호' in key:
                    detail['decision_no'] = value
                elif '결정일' in key or '의결일' in key:
                    detail['decision_date'] = value
                elif '신문' in key or '언론사' in key:
                    detail['newspaper'] = value
                elif '기사일' in key or '보도일' in key:
                    detail['article_date'] = value
                elif '결정내용' in key or '의결내용' in key:
                    detail['decision'] = value
                elif '사유' in key or '이유' in key:
                    detail['reason'] = value

    return detail


def extract_text_content(html_content: str) -> str:
    """
    HTML에서 모든 텍스트 내용을 추출합니다.

    Args:
        html_content: HTML 내용

    Returns:
        추출된 텍스트
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # 스크립트와 스타일 태그 제거
    for script in soup(['script', 'style']):
        script.decompose()

    # 텍스트 추출
    text = soup.get_text()

    # 공백 정리
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text
