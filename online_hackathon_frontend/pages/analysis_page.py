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

# 뒤로 가기 버튼
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    if st.button("🏠 홈으로", type="secondary"):
        st.switch_page("pages/home.py")  # 🔥 변경

# 페이지 제목
st.title("🎙️ 통화 내용 분석")
st.markdown("---")

# 설명
st.info("🤖 녹음된 통화 파일을 업로드하면 AI가 보이스피싱 여부를 종합적으로 분석합니다.")

# 메인 업로드 섹션
st.subheader("📤 음성 파일 업로드")

uploaded_file = st.file_uploader(
    "음성 파일을 선택하세요",
    type=['wav', 'mp3', 'ogg'],
    accept_multiple_files=False,
    help="지원 형식: WAV, MP3, OGG (최대 50MB)"
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
        if st.button("🚀 업로드 및 AI 분석 시작", type="primary", use_container_width=True):
            with st.spinner("파일 업로드 중..."):
                upload_result = upload_file_to_server(uploaded_file)
                
                if upload_result:
                    st.success("✅ 파일 업로드 완료!")
                    
                    # 세션 상태에 결과 저장
                    st.session_state['upload_result'] = upload_result
                    st.session_state['uploaded_file_name'] = uploaded_file.name
                    
                    # 분석 진행
                    with st.spinner("🤖 AI 모델이 분석 중입니다... (약 30초 소요)"):
                        analysis_result = analyze_file(upload_result['file_path'])
                        
                        if analysis_result:
                            st.session_state['analysis_result'] = analysis_result
                            st.success("🎉 분석 완료! 결과 페이지로 이동합니다.")
                            
                            # 결과 페이지로 자동 이동
                            st.balloons()
                            st.switch_page("pages/result_page.py")
                        else:
                            st.error("❌ 분석 실패. 다시 시도해주세요.")
else:
    # 사용법 안내
    st.markdown("### 💡 사용법 안내")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 📁 지원하는 파일 형식
        - **WAV**: 고품질 음성 (권장)
        - **MP3**: 압축된 음성 파일
        - **OGG**: 오픈 소스 음성 형식
        
        #### ⏱️ 분석 소요 시간
        - 파일 크기에 따라 30초~2분
        - 평균 1분 내외 완료
        """)
    
    with col2:
        st.markdown("""
        #### 🎯 분석 항목
        - **키워드 분석**: 보이스피싱 관련 단어
        - **감정 분석**: 화자의 의도 파악
        - **음성 특성**: 주파수, 톤 등 분석
        
        #### 📊 결과 제공 정보
        """)

# 주의사항
st.markdown("---")
st.markdown("### ⚠️ 개인정보 보호 안내")

st.warning("""
**🔒 파일 보안 정책:**
- 업로드된 음성 파일은 분석 완료 후 1시간 내 자동 삭제됩니다
- 개인 식별이 가능한 정보(이름, 주민번호 등)가 포함된 통화는 신중히 업로드하세요
- 분석 결과는 세션 종료 시 함께 삭제되며 서버에 저장되지 않습니다

**⚖️ 법적 고지:**
- 타인의 동의 없는 통화 녹음은 불법일 수 있습니다
- 분석 결과는 참고용이며 법적 증거로 사용할 수 없습니다
- 보이스피싱 피해 시 관련 기관에 정식 신고하시기 바랍니다
""")

# 시스템 상태
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
    
    st.markdown("---")
    st.header("🧭 네비게이션")
    
    if st.button("🏠 홈으로 이동", key="nav_home"):
        st.switch_page("pages/home.py")  # 🔥 변경
    
    if st.button("📞 번호 검색", key="nav_phone"):
        st.switch_page("pages/phone_page.py")

    # 미리보기 기능
    st.markdown("---")
    st.header("🎭 개발/테스트")
    
    if st.button("👀 결과 미리보기", help="가짜 데이터로 결과 페이지를 미리 볼 수 있습니다"):
        # 임시 테스트 데이터 생성
        st.session_state['analysis_result'] = {
            "file_path": "uploads/test-sample.wav",
            "cloud_path": "gs://voice-analysis-bucket/test-sample.wav",
            "analysis_result": {
                "is_phishing": True,
                "confidence": 0.87,
                "deepfake_probability": 0.72,
                "content_analysis": {
                    "risk_keywords": ["긴급", "계좌이체", "확인"],
                    "sentiment_score": -0.65,
                    "urgency_level": "high"
                },
                "audio_features": {
                    "duration": 45.2,
                    "sample_rate": 16000,
                    "channels": 1
                },
                "processing_time": 2.3
            }
        }
        st.session_state['upload_result'] = {
            "filename": "test-sample.wav",
            "file_path": "uploads/test-sample.wav",
            "file_size": 1048576,
            "content_type": "audio/wav"
        }
        st.session_state['uploaded_file_name'] = "🎭 테스트-샘플.wav"
        
        st.switch_page("pages/result_page.py")
