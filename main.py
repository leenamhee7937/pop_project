import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 경로
csv_file = "201012_202412_연령별인구현황_연간_전국.csv"

# 데이터 로드
df = pd.read_csv(csv_file, encoding='cp949')

# 총인구수 컬럼만 추출
total_columns = [col for col in df.columns if '총인구수' in col and '거주자' in col]
years = [col.split('_')[0] for col in total_columns]

# 지역 이름 정리 (예: '서울특별시  (1100000000)' → '서울특별시')
df['지역명'] = df['행정구역'].str.extract(r'([\w\s]+)')

# 지역 선택
region_options = df['지역명'].unique()
selected_region = st.selectbox("📍 지역을 선택하세요", region_options)

# 해당 지역의 총인구 데이터만 추출
region_row = df[df['지역명'] == selected_region]
pop_data = region_row[total_columns].iloc[0].str.replace(',', '').astype(int)

# Plotly 시각화
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=years,
    y=pop_data,
    mode='lines+markers',
    name='총인구수',
    line=dict(color='green'),
    marker=dict(size=8)
))

fig.update_layout(
    title=f"{selected_region} 총인구 변화 (2010~2024)",
    xaxis_title="연도",
    yaxis_title="총인구 수",
    height=500
)

# Streamlit 출력
st.title("📈 연도별 지역별 총인구 변화 (2010~2024)")
st.plotly_chart(fig, use_container_width=True)
