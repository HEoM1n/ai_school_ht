import streamlit as st
import requests

def upload_file_to_server(uploaded_file):
    """서버에 파일 업로드"""
    url = f"{st.session_state.API_BASE_URL}/upload"
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    
    try:
        response = requests.post(url, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"업로드 실패: {e}")
        return None

def analyze_file(file_path):
    """파일 분석 요청"""
    url = f"{st.session_state.API_BASE_URL}/analyze"
    
    try:
        response = requests.post(url, json={"file_path": file_path})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"분석 요청 실패: {e}")
        return None

# 페이지 제목
st.title("🎙️ 보이스 피싱 분석")
st.markdown("---")

# 시스템 상태 체크
with st.sidebar:
    st.header("📊 시스템 상태")
    try:
        response = requests.get(f"{st.session_state.API_BASE_URL}/health")
        if response.status_code == 200:
            st.success("✅ 서버 연결됨")
        else:
            st.error("❌ 서버 연결 실패")
    except:
        st.error("❌ 서버 연결 불가")

# 두 가지 분석 옵션 제공
st.subheader("🛡️ 보이스 피싱 탐지 옵션")

# 탭으로 두 기능 분리
tab1, tab2 = st.tabs(["📞 전화번호 검색", "🎙️ 음성 파일 분석"])

with tab1:
    st.info("**먼저 전화번호를 확인해보세요!** 이미 알려진 보이스피싱 번호라면 즉시 확인 가능합니다.")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        quick_phone = st.text_input("전화번호 입력", placeholder="010-1234-5678")
    with col2:
        if st.button("🔍 번호 검색", type="primary"):
            if quick_phone:
                # 전화번호 검색 페이지로 이동
                st.session_state.temp_phone = quick_phone
                st.switch_page("pages/phone_page.py")

with tab2:
    st.info("전화번호가 DB에 없거나, 음성 통화 내용을 분석하고 싶다면 음성 파일을 업로드하세요.")
    
    # 메인 업로드 섹션
    st.subheader("📤 음성 파일 업로드")

    uploaded_file = st.file_uploader(
        "음성 파일을 선택하세요",
        type=['wav', 'mp3', 'ogg'],
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        # 파일 정보 표시
        with st.expander("📄 파일 정보", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("파일명", uploaded_file.name)
            with col2:
                st.metric("파일 크기", f"{uploaded_file.size:,} bytes")
            with col3:
                st.metric("파일 타입", uploaded_file.type)
        
        st.markdown("---")
        
        # 업로드 및 분석 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🚀 업로드 및 분석 시작", type="primary", use_container_width=True):
                with st.spinner("파일 업로드 중..."):
                    upload_result = upload_file_to_server(uploaded_file)
                    
                    if upload_result:
                        st.success("✅ 파일 업로드 완료!")
                        
                        # 세션 상태에 결과 저장
                        st.session_state['upload_result'] = upload_result
                        st.session_state['uploaded_file_name'] = uploaded_file.name
                        
                        # 분석 진행
                        with st.spinner("AI 모델 분석 중... 잠시만 기다려주세요"):
                            analysis_result = analyze_file(upload_result['file_path'])
                            
                            if analysis_result:
                                st.session_state['analysis_result'] = analysis_result
                                st.success("🎉 분석 완료! 결과 페이지로 이동합니다.")
                                
                                # 결과 페이지로 자동 이동
                                st.balloons()
                                st.switch_page("pages/result_page.py")
                            else:
                                st.error("분석 실패. 다시 시도해주세요.")
    else:
        st.markdown("### 💡 사용법")
        st.info("""
        1. **전화번호 검색**: 의심스러운 번호를 먼저 검색해보세요
        2. **음성 파일 분석**: 통화 녹음 파일을 업로드하여 AI 분석을 받으세요
        3. **지원 형식**: WAV, MP3, OGG 파일
        """)

# 주의사항
st.markdown("---")
st.markdown("### ⚠️ 개인정보 보호 안내")
st.warning("""
- 업로드된 음성 파일은 분석 후 자동으로 삭제됩니다
- 개인정보가 포함된 통화 내용은 신중히 업로드해주세요
- 분석 결과는 참고용이며, 의심스러운 경우 관련 기관에 신고하세요
""")
