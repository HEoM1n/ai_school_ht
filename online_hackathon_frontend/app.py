import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="Voice Phishing Detection",
    page_icon="🎙️",
    layout="wide"
)

# API 설정
if 'API_BASE_URL' not in st.session_state:
    st.session_state.API_BASE_URL = "http://backend:8001"

# 페이지 정의
home_page = st.Page(
    "pages/home.py",
    title="홈",
    icon="🏠",
    default=True  # 기본 페이지
)

phone_page = st.Page(
    "pages/phone_page.py",
    title="전화번호 검색",
    icon="📞"
)

analysis_page = st.Page(  # 🔥 변경: upload_page → analysis_page
    "pages/analysis_page.py",  # 🔥 변경
    title="통화 분석",
    icon="🎙️"
)

result_page = st.Page(
    "pages/result_page.py",
    title="분석 결과",
    icon="📊"
)

# 네비게이션 설정 (숨김)
pg = st.navigation([home_page, phone_page, analysis_page, result_page], position="hidden")  # 🔥 변경

# 페이지 실행
pg.run()
