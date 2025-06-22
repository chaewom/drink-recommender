import streamlit as st
import pandas as pd

# CSV 파일 불러오기
df = pd.read_csv("음료_영양정보_국내브랜드_총150개.csv")

st.title("☕ 건강한 음료 추천 시스템")

# 사용자 입력
st.sidebar.header("👤 사용자 정보 입력")
diabetes = st.sidebar.selectbox("당뇨가 있으신가요?", ("아니요", "예"))
caffeine_sensitive = st.sidebar.selectbox("카페인에 민감하신가요?", ("아니요", "예"))
height = st.sidebar.number_input("키 (cm)", min_value=100.0, max_value=250.0, value=165.0)
weight = st.sidebar.number_input("몸무게 (kg)", min_value=30.0, max_value=200.0, value=60.0)
brand = st.sidebar.multiselect("원하는 브랜드 선택 (선택 안하면 전체)", options=df["브랜드"].unique())

# BMI 계산
bmi = weight / ((height / 100) ** 2)
st.sidebar.markdown(f"📊 당신의 BMI는 **{bmi:.1f}** 입니다.")

# 필터링
filtered = df.copy()

if diabetes == "예":
    filtered = filtered[filtered["당(g)"] <= 10]

if caffeine_sensitive == "예":
    filtered = filtered[filtered["카페인(mg)"] <= 50]

if bmi >= 23:  # 과체중 기준
    filtered = filtered[filtered["칼로리"] <= 150]

if brand:
    filtered = filtered[filtered["브랜드"].isin(brand)]

st.subheader("💡 맞춤형 추천 음료")
st.write(f"총 {len(filtered)}개의 음료가 조건을 만족합니다.")
st.dataframe(filtered[["브랜드", "음료명", "칼로리", "당(g)", "카페인(mg)"]].reset_index(drop=True))

