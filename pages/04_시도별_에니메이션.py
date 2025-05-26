import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 선택한 시도의 연도별 총인구수 애니메이션 (2010~2024)")

# CSV 불러오기
try:
    df = pd.read_csv("201012_202412_연령별인구현황_연간.csv", encoding="cp949")
except Exception as e:
    st.error(f"CSV 파일을 불러오는 중 오류 발생: {e}")
    st.stop()

# 지역명 추출
df["지역명"] = df["행정구역"].str.extract(r"^([\w\s]+)").squeeze()

# 총인구수 컬럼만 추출
total_cols = [col for col in df.columns if "거주자_총인구수" in col and "연령구간" not in col]

# long-form 변환
df_long = pd.melt(
    df,
    id_vars="지역명",
    value_vars=total_cols,
    var_name="연도",
    value_name="인구수"
)

# 연도 정리: '2010년_거주자_총인구수' → '2010'
df_long["연도"] = df_long["연도"].str.extract(r"(\d{4})")

# 인구수 숫자 변환
df_long["인구수"] = (
    df_long["인구수"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
    .replace("", "0")
    .astype(float)
    .fillna(0)
    .astype(int)
)

# 지역 선택
region_list = sorted(df_long["지역명"].dropna().unique())
selected_region = st.selectbox("📍 시도를 선택하세요", region_list)

# 선택한 지역 필터링
df_selected = df_long[df_long["지역명"] == selected_region]

# 가로 막대 애니메이션 그래프 생성
fig = px.bar(
    df_selected,
    x="인구수",
    y="연도",
    orientation="h",
    animation_frame="연도",
    range_x=[0, df_selected["인구수"].max() * 1.1],
    labels={"인구수": "총인구수", "연도": "연도"},
    title=f"📈 {selected_region}의 연도별 총인구수 변화 (가로 막대 애니메이션)"
)

fig.update_layout(
    height=600,
    xaxis_title="총인구 수",
    yaxis_title="연도",
    yaxis=dict(autorange="reversed"),  # 최근 연도가 위에 오도록
    plot_bgcolor="white",
    xaxis=dict(
        showline=True,
        linecolor="black",
        showgrid=True,
        gridcolor="lightgray"
    ),
    yaxis=dict(
        showline=True,
        linecolor="black",
        showgrid=True,
        gridcolor="lightgray"
    )
)

# 시각화 출력
st.plotly_chart(fig, use_container_width=True)
