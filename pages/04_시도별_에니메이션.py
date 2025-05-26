import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
file_path = "201012_202412_연령별인구현황_연간.csv"
df = pd.read_csv(file_path, encoding='cp949')

# 서울특별시 데이터 추출 및 전처리
seoul_row = df[df['행정구역'].str.contains("서울특별시")].iloc[0, 1:]
seoul_population = seoul_row.str.replace(',', '').astype(int)
years = seoul_population.index.str.extract(r'(\d{4})')[0]

# 데이터프레임 생성
seoul_df = pd.DataFrame({'연도': years, '인구수': seoul_population.values})
seoul_df['인구수_백만명'] = seoul_df['인구수'] / 1_000_000

# Streamlit 제목
st.title("서울특별시 연도별 인구 변화")

# 애니메이션 차트 (가로축: 연도, 세로축: 인구수)
fig = px.bar(
    seoul_df,
    x='연도',
    y='인구수_백만명',
    animation_frame='연도',
    range_y=[0, seoul_df['인구수_백만명'].max() + 0.5],
    labels={'인구수_백만명': '인구수 (백만 명)', '연도': '연도'},
    title="서울특별시 연도별 인구수 (단위: 백만 명)"
)

# 차트 표시
st.plotly_chart(fig)
