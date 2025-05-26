import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv("201012_202412_연령별인구현황_연간_전국.csv", encoding='cp949')

# 지역명 추출 (예: '서울특별시 (1100000000)' → '서울특별시')
df['지역명'] = df['행정구역'].str.extract(r'([\w\s]+)')
df = df[df['지역명'] != '전국']  # 전국 제외

# 총인구수 관련 컬럼만 필터링
total_cols = [col for col in df.columns if '거주자_총인구수' in col and '연령구간' not in col]
years = [col.split('년')[0] for col in total_cols]

# 데이터 long-form으로 변환
df_long = pd.melt(
    df,
    id_vars='지역명',
    value_vars=total_cols,
    var_name='연도',
    value_name='인구수'
)

# 연도 문자열 정리: "2010년_거주자_총인구수" → "2010"
df_long['연도'] = df_long['연도'].str.extract(r'(\d{4})')

# 인구수 문자열 → 숫자형 변환 (에러 방지 처리 포함)
df_long['인구수'] = (
    df_long['인구수']
    .str.replace(",", "", regex=False)   # 쉼표 제거
    .astype(float)                       # float으로 변환
    .fillna(0)                           # NaN → 0
    .astype(int)                         # 정수형 변환
)

# Plotly 애니메이션 바 차트 생성
fig = px.bar(
    df_long,
    x="지역명",
    y="인구수",
    color="지역명",
    animation_frame="연도",
    animation_group="지역명",
    range_y=[0, df_long['인구수'].max() * 1.1],
    labels={"인구수": "총인구수
