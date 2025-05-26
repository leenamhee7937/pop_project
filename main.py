import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 경로
csv_file = "201012_202412_연령별인구현황_연간_전국.csv"

# 데이터 로드
df = pd.read_csv(csv_file, encoding='cp949')

# 지역명 추출: '서울특별시  (1100000000)' → '서울특별시'
df['지역명'] = df['행정구역'].str.extract(r'^([\w\s]+)').iloc[:, 0]

# 총인구수 컬럼만 추출 (연령구간 제외)
total_cols = [col for col in df.columns if '총인구수' in col and '연령구간' not in col]
years = [col.split('년')[0] for col in total_cols]

# 지역 선택
region_list = sorted(df['지역명'].dropna().unique())
selected_region = st.selectbox("📍 지역을 선택하세요", region_list)

# 선택한 지역 데이터 필터링
region_data = df[df['지역명'] == selected_region]

if region_data.empty:
    st.warning("선택한 지역의 데이터가 없습니다.")
else:
    # 총인구수 데이터 전처리
    pop_data = (
        region_data[total_cols]
        .iloc[0]
        .astype(str)
        .str.replace(',', '', regex=False)
        .str.strip()
        .replace('', '0')
        .astype(float)
        .fillna(0)
        .astype(int)
    )

    # Plotly 그래프
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=pop_data,
        mode='lines+markers',
        name='총인구수',
        line=dict(color='green'),
        marker=dict(size=8)
    ))

    # 레이아웃 스타일 업데이트
    fig.update_layout(
        title=f"{selected_region} 총인구 변화 (2010~2024)",
        xaxis_title="연도",
        yaxis_title="총인구 수",
        height=500,
        xaxis=dict(
            showline=True,
            linecolor='black',
            linewidth=1.5,
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=0.5,
            zeroline=False
        ),
        yaxis=dict(
            showline=True,
            linecolor='black',
            linewidth=1.5,
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=0.5,
            zeroline=False
        ),
        plot_bgcolor='white'
    )

    # 출력
    st.title("📈 연도별 지역별 총인구 변화 (2010~2024)")
    st.plotly_chart(fig, use_container_width=True)
