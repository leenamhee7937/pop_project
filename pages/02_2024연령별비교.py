import streamlit as st
import pandas as pd
import plotly.express as px

# CSV 파일 로드
df = pd.read_csv("2024년_연령별인구현황.csv", encoding='cp949')

# 지역명 추출
df["지역명"] = df["행정구역"].str.extract(r"([\w\s]+)")

# 연령대 컬럼 필터링: 총인구수는 제외
age_columns = [col for col in df.columns if (("~" in col or "100세" in col) and "총인구수" not in col)]
selected_age = st.selectbox("📅 연령대를 선택하세요", age_columns)

# 숫자형 변환
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

fig.update_traces(texttemplate='%{text:,}', textposition='outside')
fig.update_layout(
    xaxis_tickangle=-45,
    yaxis_tickformat=",",
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

# Streamlit 출력
st.title("👶 연령대별 시도별 인구 비교 (2024년)")
st.plotly_chart(fig, use_container_width=True)
