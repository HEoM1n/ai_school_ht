# import streamlit as st

# # 페이지 설정
# st.set_page_config(
#     page_title="Voice Phishing Detection",
#     page_icon="🎙️",
#     layout="wide"
# )

# # API 설정을 전역으로 공유
# if 'API_BASE_URL' not in st.session_state:
#     st.session_state.API_BASE_URL = "http://localhost:8000"

# # 페이지 정의
# upload_page = st.Page(
#     "pages/upload_page.py", 
#     title="파일 업로드", 
#     icon="📤",
#     default=True
# )

# result_page = st.Page(
#     "pages/result_page.py", 
#     title="분석 결과", 
#     icon="📊"
# )

# # 네비게이션 설정
# pg = st.navigation([upload_page, result_page])

# # 페이지 실행
# pg.run()


import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="Voice Phishing Detection",
    page_icon="🎙️",
    layout="wide"
)

# API 설정을 전역으로 공유
if 'API_BASE_URL' not in st.session_state:
    st.session_state.API_BASE_URL = "http://localhost:8000"

# 페이지 정의
upload_page = st.Page(
    "pages/upload_page.py", 
    title="보이스 피싱 분석", 
    icon="🎙️",
    default=True
)

phone_page = st.Page(
    "pages/phone_page.py",
    title="전화번호 검색",
    icon="📞"
)

result_page = st.Page(
    "pages/result_page.py", 
    title="분석 결과", 
    icon="📊"
)

# 네비게이션 설정
pg = st.navigation([upload_page, phone_page, result_page])

# 페이지 실행
pg.run()
