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
        심의 정보 리스트 [{'title': '...', 'url': '...', 'decision_no': '...', 'decision_type': '...'}, ...]
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    decisions = []

    # HTML 구조:
    # <div class="rst_list_l">
    #   <ul>
    #     <li>
    #       <a href="...">
    #         <span>결정번호</span>
    #         <strong>제목</strong>
    #         <u class="rl_btn green">주의</u>
    #       </a>
    #     </li>
    #   </ul>
    # </div>

    # rst_list_l 클래스의 div 찾기
    list_container = soup.find('div', class_='rst_list_l')

    if not list_container:
        return decisions

    # ul > li > a 구조에서 링크 추출
    list_items = list_container.find_all('li')

    for item in list_items:
        link = item.find('a', href=lambda href: href and 'sub2_1_1.asp' in href)

        if not link:
            continue

        # URL 추출
        url = link.get('href', '')

        # 상대 경로를 절대 경로로 변환
        if url and not url.startswith('http'):
            from config import BASE_URL
            if url.startswith('/'):
                url = BASE_URL + url
            else:
                url = BASE_URL + '/m2/' + url

        # 결정번호 추출 (span 태그)
        decision_no_elem = link.find('span')
        decision_no = decision_no_elem.get_text(strip=True) if decision_no_elem else ''

        # 제목 추출 (strong 태그)
        title_elem = link.find('strong')
        title = title_elem.get_text(strip=True) if title_elem else ''

        # 결정 유형 추출 (u 태그, 예: 주의, 경고 등)
        decision_type_elem = link.find('u', class_='rl_btn')
        decision_type = decision_type_elem.get_text(strip=True) if decision_type_elem else ''

        # title 속성도 확인 (백업)
        if not title:
            title = link.get('title', '')

        decisions.append({
            'title': title,
            'url': url,
            'decision_no': decision_no,
            'decision_type': decision_type,
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

    # HTML 구조:
    # <div class="rst_result_view">
    #   <div class="rst_titleW">
    #     <u class="rl_btn">결정유형</u>
    #     <h3><i>결정번호</i> 제목</h3>
    #     <dd>언론사  발행인 ...</dd>
    #   </div>
    #   <div class="rst_contW">
    #     <ul>
    #       <li><h3>주 문</h3><p>...</p></li>
    #       <li><h3>이 유</h3><p>...</p></li>
    #       <li><h3>적용 조항</h3><p>...</p></li>
    #     </ul>
    #   </div>
    # </div>

    detail = {
        'title': '',
        'decision_no': '',
        'decision_type': '',
        'newspaper': '',
        'publisher': '',
        'decision_text': '',      # 주문
        'reason': '',             # 이유
        'applied_rules': '',      # 적용 조항
        'full_content': '',       # 전체 내용
    }

    # 메인 컨테이너 찾기
    result_view = soup.find('div', class_='rst_result_view')
    if not result_view:
        return detail

    # 1. 제목 영역 파싱 (rst_titleW)
    title_area = result_view.find('div', class_='rst_titleW')
    if title_area:
        # 결정 유형 추출 (u.rl_btn)
        decision_type_elem = title_area.find('u', class_='rl_btn')
        if decision_type_elem:
            detail['decision_type'] = decision_type_elem.get_text(strip=True)

        # 제목 및 결정번호 추출 (h3 > i)
        h3_elem = title_area.find('h3', class_='type01')
        if h3_elem:
            # 결정번호는 <i> 태그 안에
            decision_no_elem = h3_elem.find('i')
            if decision_no_elem:
                detail['decision_no'] = decision_no_elem.get_text(strip=True)
                # <i> 태그를 제거하고 나머지 텍스트가 제목
                decision_no_elem.extract()

            # 제목 추출
            detail['title'] = h3_elem.get_text(strip=True)

        # 언론사 및 발행인 추출 (dd)
        dd_elem = title_area.find('dd')
        if dd_elem:
            dd_text = dd_elem.get_text(strip=True)
            # "중부매일      발행인  한  인  섭" 형태
            # 언론사와 발행인을 분리
            parts = dd_text.split('발행인')
            if len(parts) >= 1:
                detail['newspaper'] = parts[0].strip()
            if len(parts) >= 2:
                detail['publisher'] = '발행인 ' + parts[1].strip()

    # 2. 본문 영역 파싱 (rst_contW)
    content_area = result_view.find('div', class_='rst_contW')
    if content_area:
        # ul > li 구조에서 각 섹션 추출
        list_items = content_area.find_all('li')

        for item in list_items:
            # 섹션 제목 (h3)
            section_title_elem = item.find('h3', class_='type01')
            if not section_title_elem:
                continue

            section_title = section_title_elem.get_text(strip=True)

            # 섹션 내용 (p)
            section_content_elem = item.find('p')
            if not section_content_elem:
                continue

            section_content = section_content_elem.get_text(strip=True)

            # 섹션별로 분류
            if '주문' in section_title or '주 문' in section_title:
                detail['decision_text'] = section_content
            elif '이유' in section_title or '이 유' in section_title:
                detail['reason'] = section_content
            elif '적용' in section_title or '조항' in section_title:
                detail['applied_rules'] = section_content

        # 전체 본문 내용도 저장
        detail['full_content'] = content_area.get_text(separator='\n', strip=True)

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
