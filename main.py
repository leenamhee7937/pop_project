import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 경로
csv_file = "201512_202012_연령별인구현황_연간.csv"

# 데이터 로드
df = pd.read_csv(csv_file, encoding='cp949')

# 연도별 총인구 컬럼 추출
total_columns = [col for col in df.columns if '거주자_총인구수' in col]
years = [col.split('_')[0] for col in total_columns]

# 행정구역 이름만 추출 (괄호 제거)
df['행정구역명'] = df['행정구역'].str.extract(r'([\w\s]+)')

# 선택 가능한 동 목록
available_regions = df['행정구역명'].unique()
selected_region = st.selectbox("📍 동(행정구역)을 선택하세요", available_regions)

# 선택된 동 필터링
row = df[df['행정구역명'] == selected_region]

# 인구 수 정리
population = row[total_columns].iloc[0].str.replace(',', '').astype(int)

# Plotly 그래프
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=years,
    y=population,
    mode='lines+markers',
    name=selected_region,
    line=dict(color='royalblue'),
    marker=dict(size=8)
))

fig.update_layout(
    title=f"{selected_region} 총인구 변화 (2015~2020)",
    xaxis_title="연도",
    yaxis_title="총인구 수",
    height=500
)

# 출력
st.title("👨‍👩‍👧‍👦 연도별 동별 총인구 시각화 (2015~2020)")
st.plotly_chart(fig, use_container_width=True)
