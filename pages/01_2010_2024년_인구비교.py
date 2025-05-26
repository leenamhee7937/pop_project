import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 경로
mf_file = "202504_202504_연령별인구현황_월간_남여구분.csv"
total_file = "202504_202504_연령별인구현황_월간_남여합계.csv"

# 파일 로드
df_mf = pd.read_csv(mf_file, encoding='cp949')
df_total = pd.read_csv(total_file, encoding='cp949')

# 시도명 리스트 생성
region_list = df_total['행정구역'].str.extract(r'([\w\s]+)\s+\(')[0].dropna().unique()

# 사용자 선택
selected_region = st.selectbox("📍 지역을 선택하세요", region_list)

# 선택된 지역 데이터 필터링
df_mf_region = df_mf[df_mf['행정구역'].str.contains(selected_region)]
df_total_region = df_total[df_total['행정구역'].str.contains(selected_region)]

# 컬럼 분류
male_cols = [col for col in df_mf.columns if '2025년04월_남_' in col and '세' in col]
female_cols = [col for col in df_mf.columns if '2025년04월_여_' in col and '세' in col]
total_cols = [col for col in df_total.columns if '2025년04월_계_' in col and '세' in col]
ages = [col.split('_')[-1] for col in total_cols]

# 문자열 → 숫자 변환 함수
def clean_data(series):
    return (
        series
        .str.replace(',', '', regex=False)
        .astype(float)
        .fillna(0)
        .astype(int)
        .values
    )

# 남/여/합계 데이터 추출
male_pop = clean_data(df_mf_region[male_cols].iloc[0])
female_pop = clean_data(df_mf_region[female_cols].iloc[0])
total_pop = clean_data(df_total_region[total_cols].iloc[0])

# 📊 막대그래프 (합계)
bar_fig = go.Figure()
bar_fig.add_trace(go.Bar(x=ages, y=total_pop, name='전체', marker=dict(color='royalblue')))
bar_fig.update_layout(
    title=f'{selected_region} - 연령별 인구 합계 (2025년 4월)',
    xaxis_title='연령',
    yaxis_title='인구 수',
    bargap=0.2,
    height=500
)

# 📈 선그래프 (남 vs 여)
line_fig = go.Figure()
line_fig.add_trace(go.Scatter(x=ages, y=male_pop, mode='lines+markers', name='남성'))
line_fig.add_trace(go.Scatter(x=ages, y=female_pop, mode='lines+markers', name='여성'))
line_fig.update_layout(
    title=f'{selected_region} - 연령별 남녀 인구 비교 (2025년 4월)',
    xaxis_title='연령',
    yaxis_title='인구 수',
    hovermode='x unified',
    height=500
)

# 출력
st.title("📊 2025년 4월 지역별 연령별 인구 통계 시각화")
st.plotly_chart(bar_fig, use_container_width=True)
st.plotly_chart(line_fig, use_container_width=True)
