import streamlit as st
from datetime import datetime

# 페이지 제목
st.title("📊 분석 결과")
st.markdown("---")

# 결과 데이터 확인
if 'analysis_result' not in st.session_state:
    st.error("⚠️ 분석 결과가 없습니다.")
    if st.button("🏠 메인 페이지로 돌아가기"):
        st.switch_page("pages/upload_page.py")
    st.stop()

# 결과 데이터 가져오기
analysis_result = st.session_state['analysis_result']
upload_result = st.session_state.get('upload_result', {})
uploaded_file_name = st.session_state.get('uploaded_file_name', '알 수 없음')

# 파일 정보 표시
with st.expander("📄 분석된 파일 정보", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**파일명:** {uploaded_file_name}")
        st.write(f"**클라우드 경로:** `{analysis_result.get('cloud_path', 'N/A')}`")
    with col2:
        st.write(f"**분석 완료 시간:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"**파일 크기:** {upload_result.get('file_size', 0):,} bytes")

st.markdown("---")

# 메인 결과 표시
result_data = analysis_result['analysis_result']

# 위험도 표시
if result_data['is_phishing']:
    st.error("🚨 **보이스 피싱 위험 감지!**")
    st.markdown("### ⚠️ 주의사항")
    st.warning("이 통화는 보이스 피싱으로 의심됩니다. 개인정보나 금융정보를 제공하지 마세요!")
else:
    st.success("✅ **정상 통화로 판단됩니다**")
    st.info("분석 결과 보이스 피싱 위험이 낮습니다.")

# 핵심 메트릭 표시
st.markdown("### 📈 핵심 지표")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("전체 신뢰도", f"{result_data['confidence']:.1%}")

with col2:
    st.metric("딥페이크 확률", f"{result_data['deepfake_probability']:.1%}")

with col3:
    content_analysis = result_data['content_analysis']
    st.metric("긴급도", content_analysis['urgency_level'].upper())

with col4:
    st.metric("처리 시간", f"{result_data['processing_time']:.1f}초")

# 진행률 바로 위험도 시각화
st.markdown("### 📊 위험도 분석")
risk_score = result_data['confidence'] if result_data['is_phishing'] else (1 - result_data['confidence'])
st.progress(risk_score)

# 상세 분석 결과
st.markdown("### 🔍 상세 분석")

# 컨텐츠 분석
with st.expander("📝 컨텐츠 분석", expanded=True):
    st.markdown("**검출된 위험 키워드:**")
    
    # 키워드를 배지 형태로 표시
    keyword_cols = st.columns(len(content_analysis['risk_keywords']))
    for i, keyword in enumerate(content_analysis['risk_keywords']):
        with keyword_cols[i]:
            st.markdown(f"<span style='background-color: #ff4b4b; color: white; padding: 0.2em 0.6em; border-radius: 0.3em; font-size: 0.8em;'>{keyword}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("감정 점수", f"{content_analysis['sentiment_score']:.2f}")
    with col2:
        st.metric("긴급도 레벨", content_analysis['urgency_level'].upper())

# 오디오 특성
with st.expander("🎵 오디오 특성 분석"):
    audio_features = result_data['audio_features']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("재생 시간", f"{audio_features['duration']:.1f}초")
    with col2:
        st.metric("샘플링 레이트", f"{audio_features['sample_rate']:,} Hz")
    with col3:
        st.metric("채널 수", audio_features['channels'])

# Raw Data (개발자용)
with st.expander("🔧 Raw Data (고급 사용자용)"):
    st.json(analysis_result)

# 하단 액션 버튼들
st.markdown("---")
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🏠 새로운 분석", type="primary", use_container_width=True):
        # 세션 상태 초기화
        if 'analysis_result' in st.session_state:
            del st.session_state['analysis_result']
        if 'upload_result' in st.session_state:
            del st.session_state['upload_result']
        st.switch_page("pages/upload_page.py")

with col2:
    if st.button("📋 결과 복사", use_container_width=True):
        result_text = f"""
보이스 피싱 탐지 결과
==================
파일명: {uploaded_file_name}
위험 여부: {'위험' if result_data['is_phishing'] else '안전'}
신뢰도: {result_data['confidence']:.1%}
딥페이크 확률: {result_data['deepfake_probability']:.1%}
분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        st.code(result_text)
        st.success("결과가 표시되었습니다. 복사해서 사용하세요!")

with col3:
    if st.button("📊 다른 파일 비교", use_container_width=True):
        st.info("새로운 파일을 업로드하여 비교 분석을 진행하세요.")
        st.switch_page("pages/upload_page.py")
