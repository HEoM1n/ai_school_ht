import streamlit as st
import requests
import re

def check_phone_number(phone_number):
    """전화번호 DB 검색 요청"""
    url = f"{st.session_state.API_BASE_URL}/check-phone"
    
    try:
        response = requests.post(url, json={"phone_number": phone_number})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"검색 실패: {e}")
        return None

def validate_phone_number(phone_number):
    """전화번호 유효성 검사"""
    # 한국 전화번호 형식 체크
    pattern = r'^01[0-9]-?[0-9]{3,4}-?[0-9]{4}$'
    return re.match(pattern, phone_number.replace(" ", "")) is not None

col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    if st.button("🏠 홈으로", type="secondary"):
        st.switch_page("pages/home.py")  # home.py로 변경

# 페이지 제목
st.title("📞 전화번호 검색")
st.markdown("---")

# 설명
st.info("🔍 의심스러운 전화번호를 입력하여 보이스피싱 신고 이력을 즉시 확인하세요.")

# 전화번호 입력
col1, col2 = st.columns([3, 1])

with col1:
    phone_input = st.text_input(
        "전화번호를 입력하세요",
        placeholder="예: 010-1234-5678",
        help="하이픈(-) 포함 또는 제외 모두 가능합니다"
    )

with col2:
    search_button = st.button("🔍 검색", type="primary", use_container_width=True)

if search_button and phone_input:
    if not validate_phone_number(phone_input):
        st.error("올바른 전화번호 형식을 입력해주세요. (예: 010-1234-5678)")
    else:
        with st.spinner("전화번호 검색 중..."):
            result = check_phone_number(phone_input)
            
            if result:
                st.markdown("---")
                
                # 검색 결과 표시
                if result["is_phishing"]:
                    st.error("🚨 **보이스피싱 위험 번호 감지!**")
                    st.warning(result["message"])
                    
                    # 상세 정보 표시
                    if result.get("details"):
                        details = result["details"]
                        
                        with st.expander("📋 상세 정보", expanded=True):
                            col_left, col_right = st.columns(2)
                            with col_left:
                                st.write(f"**신고 횟수:** {details.get('report_count', 0)}")
                            if details.get('description'):
                                st.markdown("**상세 설명:**")
                                st.write(details['description'])
                    
                    # 주의사항
                    st.markdown("### ⚠️ 긴급 대처 방법")
                    st.error("""
                    1. 🚫 **즉시 통화 차단** - 더 이상 대화하지 마세요
                    2. 🔒 **개인정보 보호** - 이름, 주민번호, 계좌번호 절대 말하지 마세요  
                    3. 📞 **신고하기** - 경찰서(112) 또는 금융감독원(1332)에 즉시 신고
                    4. 🏦 **금융기관 확인** - 의심스러면 해당 기관에 직접 전화로 확인
                    """)
                    
                else:
                    st.success("✅ **안전한 번호입니다**")
                    st.info(result["message"])
                    st.write(f"**신뢰도:** {result['confidence']:.1%}")
                    
                    st.markdown("### 💡 안내사항")
                    st.info("""
                    - 현재 DB에서 보이스피싱 이력이 발견되지 않았습니다
                    - 새로운 번호이거나 최근에 생성된 번호일 수 있으니 여전히 주의하세요
                    - 의심스러운 내용의 통화라면 개인정보 제공을 피하세요
                    """)
                    
                    # 추가 분석 제안
                    st.markdown("---")
                    if st.button("🎙️ 통화 내용도 분석해보기", type="secondary"):
                        st.switch_page("pages/analysis_page.py")

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
        st.switch_page("pages/home.py")  # 🔥 변경: app.py → pages/home.py
    
    if st.button("🎙️ 통화 분석", key="nav_analysis"):
        st.switch_page("pages/analysis_page.py")