import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 로드
df = pd.read_csv("2024년_연령별인구현황.csv", encoding='cp949')

# 지역명 추출 (예: '서울특별시  (1100000000)' → '서울특별시')
df["지역명"] = df["행정구역"].str.extract(r"([\w\s]+)")

# 사용할 연령대 컬럼 추출
age_columns = [col for col in df.columns if "~" in col or "100세" in col]
selected_age = st.selectbox("📅 연령대를 선택하세요", age_columns)

# 인구 데이터를 숫자형으로 변환
df[selected_age] = df[selected_age].str.replace(",", "").astype(int)

# Plotly 막대그래프 생성
fig = px.bar(
    df,
    x="지역명",
    y=selected_age,
    title=f"2024년 {selected_age} 인구 - 시도별 비교",
    labels={selected_age: "인구 수", "지역명": "지역"},
    text=selected_age,
)

fig.update_layout(xaxis_tickangle=-45)

# Streamlit 출력
st.title("👶 연령대별 시도별 인구 비교 (2024년)")
st.plotly_chart(fig, use_container_width=True)
