#!/usr/bin/env python3
"""
신문윤리위원회 심의결정 스크레이퍼 메인 실행 스크립트

사용법:
    python main.py
"""

import os
import sys
import time
import logging
from typing import List, Dict

import config
from scraper import IkpecScraper
from parser import parse_decision_list, parse_decision_detail
from markdown_writer import (
    create_decision_markdown,
    save_markdown_file,
    create_index_markdown,
    sanitize_filename
)


# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('scraper.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


def scrape_monthly_decisions(scraper: IkpecScraper, year: int, month: int) -> List[Dict]:
    """
    특정 연월의 심의 결정을 스크레이핑합니다.

    Args:
        scraper: IkpecScraper 인스턴스
        year: 연도
        month: 월

    Returns:
        추출된 심의 데이터 리스트
    """
    logger.info(f"=== {year}년 {month}월 심의 결정 스크레이핑 시작 ===")

    # 1. 월별 목록 페이지에서 링크 추출
    decision_links = scraper.get_decision_links_from_page(year, month)

    if not decision_links:
        logger.warning(f"{year}년 {month}월에 심의 결정이 없습니다.")
        return []

    logger.info(f"총 {len(decision_links)}건의 심의 발견")

    # 2. 각 심의 페이지에서 상세 내용 추출
    decisions_data = []

    for idx, link_info in enumerate(decision_links, 1):
        logger.info(f"[{idx}/{len(decision_links)}] 처리 중: {link_info['title']}")

        try:
            # 개별 페이지 접근
            html_content = scraper.get_decision_detail(link_info['url'])

            # HTML 파싱
            detail_data = parse_decision_detail(html_content)

            # 링크 정보 추가
            detail_data['url'] = link_info['url']
            detail_data['list_title'] = link_info['title']

            # 제목이 없으면 리스트의 제목 사용
            if not detail_data.get('title'):
                detail_data['title'] = link_info['title']

            decisions_data.append(detail_data)

            # 서버 부하 방지를 위한 대기
            time.sleep(config.REQUEST_DELAY)

        except Exception as e:
            logger.error(f"심의 페이지 처리 중 오류: {link_info['url']}")
            logger.error(f"오류 내용: {e}")
            continue

    logger.info(f"=== {year}년 {month}월 스크레이핑 완료: {len(decisions_data)}건 ===")
    return decisions_data


def save_decisions_as_markdown(decisions_data: List[Dict], year: int, month: int):
    """
    추출한 심의 데이터를 마크다운 파일로 저장합니다.

    Args:
        decisions_data: 심의 데이터 리스트
        year: 연도
        month: 월
    """
    if not decisions_data:
        logger.warning("저장할 데이터가 없습니다.")
        return

    # 출력 디렉토리 생성 (연도/월별)
    output_dir = os.path.join(config.OUTPUT_DIR, f"{year}", f"{month:02d}")
    os.makedirs(output_dir, exist_ok=True)

    logger.info(f"마크다운 파일 저장 시작: {output_dir}")

    saved_files = []

    for idx, decision in enumerate(decisions_data, 1):
        try:
            # 마크다운 생성
            md_content = create_decision_markdown(decision)

            # 파일명 생성
            title = decision.get('title', f'decision_{idx}')
            decision_no = decision.get('decision_no', '')

            if decision_no:
                filename = f"{decision_no}_{title}"
            else:
                filename = f"{year}{month:02d}_{idx:03d}_{title}"

            # 파일 저장
            filepath = save_markdown_file(md_content, filename, output_dir)
            logger.info(f"[{idx}/{len(decisions_data)}] 저장 완료: {os.path.basename(filepath)}")

            # 인덱스 생성을 위한 정보 저장
            decision['filename'] = os.path.basename(filepath)
            saved_files.append(decision)

        except Exception as e:
            logger.error(f"마크다운 저장 중 오류: {decision.get('title', 'unknown')}")
            logger.error(f"오류 내용: {e}")
            continue

    # 인덱스 파일 생성
    if saved_files:
        try:
            index_path = create_index_markdown(saved_files, year, month, output_dir)
            logger.info(f"인덱스 파일 생성: {index_path}")
        except Exception as e:
            logger.error(f"인덱스 파일 생성 중 오류: {e}")

    logger.info(f"총 {len(saved_files)}개 파일 저장 완료")


def main():
    """메인 실행 함수"""
    logger.info("===== 신문윤리위원회 심의결정 스크레이퍼 시작 =====")

    # 출력 디렉토리 확인
    if not os.path.exists(config.OUTPUT_DIR):
        os.makedirs(config.OUTPUT_DIR)
        logger.info(f"출력 디렉토리 생성: {config.OUTPUT_DIR}")

    # 스크레이핑 대상 확인
    if not config.TARGET_PERIODS:
        logger.error("config.py에서 TARGET_PERIODS를 설정해주세요.")
        sys.exit(1)

    logger.info(f"스크레이핑 대상: {len(config.TARGET_PERIODS)}개 기간")
    for year, month in config.TARGET_PERIODS:
        logger.info(f"  - {year}년 {month}월")

    # 스크레이퍼 실행
    with IkpecScraper(headless=config.HEADLESS_MODE) as scraper:
        for year, month in config.TARGET_PERIODS:
            try:
                # 월별 심의 스크레이핑
                decisions_data = scrape_monthly_decisions(scraper, year, month)

                # 마크다운 파일로 저장
                save_decisions_as_markdown(decisions_data, year, month)

                # 다음 월 처리 전 대기
                time.sleep(1)

            except Exception as e:
                logger.error(f"{year}년 {month}월 처리 중 오류 발생: {e}")
                continue

    logger.info("===== 스크레이핑 완료 =====")
    logger.info(f"결과 파일 위치: {os.path.abspath(config.OUTPUT_DIR)}")


if __name__ == "__main__":
    main()
