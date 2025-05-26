import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 선택한 시도의 연도별 총인구수 변화 애니메이션")

# CSV 파일 불러오기
try:
    df = pd.read_csv("201012_202412_연령별인구현황_연간.csv", encoding='cp949')
except Exception as e:
    st.error(f"CSV 파일을 불러오는 중 오류 발생: {e}")
    st.stop()

# 지역명 추출 및 정리
df['지역명'] = df['행정구역'].str.extract(r'([\w\s]+)')
df = df[df['지역명'] != '전국']

# 총인구수 컬럼 필터링
total_cols = [col for col in df.columns if '거주자_총인구수' in col and '연령구간' not in col]
if not total_cols:
    st.error("총인구수 관련 컬럼을 찾을 수 없습니다.")
    st.stop()

# 연도 추출
df_long = pd.melt(
    df,
    id_vars='지역명',
    value_vars=total_cols,
    var_name='연도',
    value_name='인구수'
)
df_long['연도'] = df_long['연도'].str.extract(r'(\d{4})')

# 숫자 변환 (쉼표, 공백, NaN 처리 포함)
df_long['인구수'] = (
    df_long['인구수']
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.replace(" ", "", regex=False)
    .replace("", "0")
    .astype(float)
    .fillna(0)
    .astype(int)
)

# ✅ 시도 선택 드롭다운
selected_region = st.selectbox("📍 시도를 선택하세요", sorted(df_long['지역명'].unique()))

# 선택한 지역만 필터링
df_selected = df_long[df_long['지역명'] == selected_region]

# Plotly 애니메이션 그래프 생성
fig = px.bar(
    df_selected,
    x="연도",
    y="인구수",
    color="연도",
    animation_frame="연도",
    range_y=[0, df_selected['인구수'].max() * 1.1],
    labels={"인구수": "총인구수", "연도": "연도"},
    title=f"{selected_region}의 연도별 총인구수 변화 (2010~2024)"
)

fig.update_layout(
    showlegend=False,
    height=600
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)
