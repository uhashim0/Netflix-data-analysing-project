# 넷플릭스 콘텐츠 데이터 분석 프로젝트

## 프로젝트 개요
Kaggle의 넷플릭스 공개 데이터셋(8,800개 콘텐츠)을 활용하여
한국이 다른 나라에 비해 TV Show 장르 비율이 높다는 것을
데이터로 검증하고 인사이트를 도출한 프로젝트입니다.

## 사용 기술
- Python (pandas) — 데이터 정제 및 가공
- SQLite — DB 설계 및 구조화
- SQL — 데이터 분석 쿼리
- Excel — 결과 정리 및 시각화

## 프로젝트 구조
```
netflix_project/
├── netflix_titles.csv       # 캐글 원본 데이터
├── 01_data_cleaning.py      # 데이터 정제 및 DB 적재
├── 03_sql_analysis.sql      # 분석 쿼리 모음
├── 04_excel_export.py       # 엑셀 내보내기
├── netflix.db               # SQLite DB
├── netflix_analysis.xlsx    # 분석 결과
└── ERD.png                  # 테이블 관계도
```

## 데이터 구조 (ERD)
![ERD](ERD.png)

| 테이블 | 설명 |
|--------|------|
| works | 콘텐츠 기본 정보 |
| works_genres_raw | 콘텐츠-장르 연결 테이블 |
| cast_members | 출연진 정보 |

## 분석 과정

### 1. 데이터 정제
- 원본 CSV 8,800행 로드
- 결측치 처리 (country, director, cast)
- date_added 날짜 형식 변환
- listed_in 장르 컬럼 분리

### 2. DB 구조화
- 원본 CSV 1개 → 정규화된 테이블 3개로 분리
- 장르, 출연진 다중값 컬럼을 별도 테이블로 설계
- SQLite DB로 적재

### 3. SQL 분석
- 총 9개 쿼리 작성
- 전체 현황 파악 (1~6번)
- 한국 콘텐츠 집중 분석 (7~9번)

## 핵심 인사이트
- 한국의 TV Show 비율은 79.4%로 주요 국가 중 1위
- 한국 콘텐츠에서 가장 많은 장르 3개는 
    1. International TV Shows 
    2. Korean TV Shows 
    3. Romantic TV Shows
- 한국 TV Show는 2019년 44개로 정점을 기록하며 2017년 대비 37.5% 증가, 
  넷플릭스의 한국 콘텐츠 투자가 본격화된 시점으로 분석됨

## 데이터 출처
- [Kaggle — Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows)

