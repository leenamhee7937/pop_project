import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 불러오기
df = pd.read_csv("2024년_연령별인구현황.csv", encoding='cp949')

# 지역명 추출
df["지역명"] = df["행정구역"].str.extract(r"([가-힣]+[시도])")

# '전국' 제외
df = df[df["지역명"] != "전국"]

# 연령대 컬럼 필터링
age_columns = [col for col in df.columns if ("세" in col and "~" in col) or "100세 이상" in col]

# 문자열 -> 숫자형으로 변환
for col in age_columns:
    df[col] = df[col].str.replace(",", "").astype(int)

# melt를 이용해 연령대를 행으로 변환
df_melted = df.melt(id_vars=["지역명"], value_vars=age_columns,
                    var_name="연령대", value_name="인구수")

# Streamlit 제목
st.title("🏙️ 시도별 연령대 인구 분포 (누적 막대그래프)")

# Plotly 누적 막대 그래프
fig = px.bar(
    df_melted,
    x="지역명",
    y="인구수",
    color="연령대",
    title="2024년 시도별 연령대별 인구 (누적)",
    labels={"지역명": "지역", "인구수": "인구 수"},
    text_auto=True
)

# 시각화 스타일 조정
fig.update_layout(
    xaxis_tickangle=-45,
    yaxis_tickformat=",",
    barmode='stack',  # 누적 막대그래프
    legend_title_text="연령대"
)

# 그래프 출력
st.plotly_chart(fig, use_container_width=True)
