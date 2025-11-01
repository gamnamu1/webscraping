"""
마크다운 파일 생성 모듈
추출한 심의 내용을 마크다운 형식으로 변환하고 파일로 저장합니다.
"""

import os
from datetime import datetime
from typing import Dict, List
import re


def sanitize_filename(filename: str) -> str:
    """
    파일명에 사용할 수 없는 문자를 제거합니다.

    Args:
        filename: 원본 파일명

    Returns:
        정제된 파일명
    """
    # Windows 파일명에 사용할 수 없는 문자 제거
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # 연속된 공백을 하나로
    filename = re.sub(r'\s+', ' ', filename)
    # 앞뒤 공백 제거
    filename = filename.strip()
    # 길이 제한 (확장자 포함 최대 255자)
    if len(filename) > 200:
        filename = filename[:200]
    return filename


def create_decision_markdown(decision_data: Dict[str, any]) -> str:
    """
    심의 데이터를 마크다운 형식으로 변환합니다.

    Args:
        decision_data: 심의 상세 정보

    Returns:
        마크다운 형식의 문자열
    """
    md_content = []

    # 제목
    title = decision_data.get('title', '제목 없음')
    md_content.append(f"# {title}\n")

    # 메타 정보
    md_content.append("## 기본 정보\n")

    if decision_data.get('decision_no'):
        md_content.append(f"- **결정번호**: {decision_data['decision_no']}")

    if decision_data.get('decision_type'):
        md_content.append(f"- **결정유형**: {decision_data['decision_type']}")

    if decision_data.get('newspaper'):
        md_content.append(f"- **언론사**: {decision_data['newspaper']}")

    if decision_data.get('publisher'):
        md_content.append(f"- **발행인**: {decision_data['publisher']}")

    if decision_data.get('url'):
        md_content.append(f"- **원문 URL**: {decision_data['url']}")

    md_content.append("")  # 빈 줄

    # 주문 (결정 내용)
    if decision_data.get('decision_text'):
        md_content.append("## 주문\n")
        md_content.append(decision_data['decision_text'])
        md_content.append("")

    # 이유 (결정 사유)
    if decision_data.get('reason'):
        md_content.append("## 이유\n")
        md_content.append(decision_data['reason'])
        md_content.append("")

    # 적용 조항
    if decision_data.get('applied_rules'):
        md_content.append("## 적용 조항\n")
        md_content.append(decision_data['applied_rules'])
        md_content.append("")

    # 전체 내용 (백업용, 위 섹션들이 없을 경우)
    if decision_data.get('full_content') and not (
        decision_data.get('decision_text') or
        decision_data.get('reason') or
        decision_data.get('applied_rules')
    ):
        md_content.append("## 전체 내용\n")
        md_content.append(decision_data['full_content'])
        md_content.append("")

    # 푸터
    md_content.append("---")
    md_content.append(f"*생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    return "\n".join(md_content)


def save_markdown_file(content: str, filename: str, output_dir: str) -> str:
    """
    마크다운 내용을 파일로 저장합니다.

    Args:
        content: 마크다운 내용
        filename: 파일명 (확장자 제외)
        output_dir: 출력 디렉토리

    Returns:
        저장된 파일의 전체 경로
    """
    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    # 파일명 정제
    safe_filename = sanitize_filename(filename)
    if not safe_filename.endswith('.md'):
        safe_filename += '.md'

    # 전체 경로
    filepath = os.path.join(output_dir, safe_filename)

    # 파일 저장
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


def create_index_markdown(decisions: List[Dict[str, any]], year: int, month: int, output_dir: str) -> str:
    """
    월별 심의 목록의 인덱스 마크다운 파일을 생성합니다.

    Args:
        decisions: 심의 정보 리스트
        year: 연도
        month: 월
        output_dir: 출력 디렉토리

    Returns:
        저장된 인덱스 파일의 경로
    """
    md_content = []

    # 제목
    md_content.append(f"# 신문윤리위원회 심의결정 - {year}년 {month}월\n")

    # 메타 정보
    md_content.append(f"- **생성 시간**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    md_content.append(f"- **총 심의 건수**: {len(decisions)}건\n")

    # 목록
    md_content.append("## 심의 목록\n")

    for i, decision in enumerate(decisions, 1):
        title = decision.get('title', '제목 없음')
        filename = decision.get('filename', '')
        url = decision.get('url', '')

        if filename:
            md_content.append(f"{i}. [{title}](./{filename})")
        else:
            md_content.append(f"{i}. {title}")

        if url:
            md_content.append(f"   - 원문: {url}")

    # 파일 저장
    index_filename = f"INDEX_{year}_{month:02d}.md"
    filepath = save_markdown_file("\n".join(md_content), index_filename, output_dir)

    return filepath
