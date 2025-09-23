import streamlit as st

# 홈페이지 내용
st.markdown("""
<div style='text-align: center;'>
    <h1>🛡️ 보이스 피싱 탐지 시스템</h1>
    <h3>Voice Phishing Detection System</h3>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# 시스템 소개
st.markdown("""
<div style='text-align: center; font-size: 18px; margin: 30px 0;'>
    <p>🔒 <strong>안전한 통화를 위한 AI 기반 보이스 피싱 탐지</strong></p>
    <p>의심스러운 전화를 받았나요? 두 가지 방법으로 확인해보세요!</p>
</div>
""", unsafe_allow_html=True)

# 두 개의 큰 버튼 옵션
st.markdown("### 📋 탐지 방법 선택")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # 전화번호 검색 버튼
    if st.button(
        "📞 전화번호 검색", 
        type="primary",
        use_container_width=True,
        help="의심스러운 전화번호가 보이스피싱 DB에 등록되어 있는지 즉시 확인"
    ):
        st.switch_page("pages/phone_page.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 통화 분석 버튼  
    if st.button(
        "🎙️ 통화 내용 분석",
        type="secondary", 
        use_container_width=True,
        help="녹음된 통화 파일을 업로드하여 AI가 보이스피싱 여부를 분석"
    ):
        st.switch_page("pages/analysis_page.py")

# 각 방법에 대한 설명
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    #### 📞 전화번호 검색
    
    **⚡ 빠른 확인 (즉시)**
    - 이미 신고된 보이스피싱 번호인지 DB에서 즉시 확인
    - 의심스러운 번호를 받았을 때 가장 먼저 시도
    - 신고 이력, 위험도, 상세 정보 제공
    """)

with col2:
    st.markdown("""
    #### 🎙️통화 내용 분석
    
    **🤖 AI 분석 (2-3분 소요)**
    - 녹음된 통화 파일을 AI가 종합 분석
    - 딥페이크 음성, 위험 키워드, 감정 등 다각도 검토
    - 전화번호 DB에 없는 신종 보이스피싱도 탐지
    """)

# 주의사항
st.markdown("---")
st.markdown("### ⚠️ 사용 시 주의사항")

st.info("""
**🚨 긴급상황 시:**
- 의심스러운 경우 즉시 통화 종료
- 개인정보나 금융정보 절대 제공 금지
- 경찰서(112) 또는 금융감독원(1332) 신고

**🔒 개인정보 보호:**
- 업로드된 파일은 분석 후 자동 삭제
- 개인 식별 정보가 포함된 내용 주의
- 분석 결과는 참고용으로만 활용
""")

# 시스템 상태
with st.sidebar:
    st.header("📊 시스템 상태")
    
    try:
        import requests
        response = requests.get(f"{st.session_state.API_BASE_URL}/health")
        if response.status_code == 200:
            st.success("✅ 서버 연결됨")
        else:
            st.error("❌ 서버 연결 실패")
    except:
        st.error("❌ 서버 연결 불가")
        st.caption("백엔드 서버를 먼저 실행해주세요")
