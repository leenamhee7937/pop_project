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

# 지역 이름 정리
df['지역명'] = df['행정구역'].str.extract(r'([\w\s]+)')

# 지역 선택 (두 개)
region_list = df['지역명'].unique()
col1, col2 = st.columns(2)
with col1:
    region1 = st.selectbox("📍 첫 번째 지역 선택", region_list, index=0)
with col2:
    region2 = st.selectbox("📍 두 번째 지역 선택", region_list, index=1)

# 각 지역 데이터 추출
row1 = df[df['지역명'] == region1]
row2 = df[df['지역명'] == region2]

pop1 = row1[total_columns].iloc[0].str.replace(',', '').astype(int)
pop2 = row2[total_columns].iloc[0].str.replace(',', '').astype(int)

# Plotly 시각화
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=years,
    y=pop1,
    mode='lines+markers',
    name=region1,
    line=dict(color='blue')
))

fig.add_trace(go.Scatter(
    x=years,
    y=pop2,
    mode='lines+markers',
    name=region2,
    line=dict(color='orange')
))

fig.update_layout(
    title=f"📊 {region1} vs {region2} 총인구 비교 (2010~2024)",
    xaxis_title="연도",
    yaxis_title="총인구 수",
    height=600,
    hovermode='x unified'
)

# 출력
st.title("👥 지역별 총인구 비교 (2010~2024)")
st.plotly_chart(fig, use_container_width=True)
