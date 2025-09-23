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

def report_phone_number(phone_number, reporter_name, description):
    """보이스피싱 번호 신고"""
    url = f"{st.session_state.API_BASE_URL}/report-phone"
    
    try:
        response = requests.post(
            url, 
            params={
                "phone_number": phone_number,
                "reporter_name": reporter_name,
                "description": description
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"신고 실패: {e}")
        return None

def validate_phone_number(phone_number):
    """전화번호 유효성 검사"""
    # 한국 전화번호 형식 체크
    pattern = r'^01[0-9]-?[0-9]{3,4}-?[0-9]{4}$'
    return re.match(pattern, phone_number.replace(" ", "")) is not None

# 페이지 제목
st.title("📞 전화번호 검색")
st.markdown("---")

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

# 메인 검색 섹션
st.subheader("🔍 보이스피싱 번호 검색")
st.info("의심스러운 전화번호를 입력하여 보이스피싱 이력을 확인하세요.")

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
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**신고일:** {details['reported_date']}")
                                st.write(f"**신고자:** {details['reporter_name']}")
                            with col2:
                                st.write(f"**확인 상태:** {details['confirmation_status']}")
                                st.write(f"**신뢰도:** {result['confidence']:.1%}")
                            
                            if details['description']:
                                st.write(f"**상세 내용:** {details['description']}")
                    
                    # 주의사항
                    st.markdown("### ⚠️ 주의사항")
                    st.warning("""
                    - 이 번호로부터의 통화를 즉시 차단하세요
                    - 개인정보나 금융정보를 절대 제공하지 마세요
                    - 경찰서(112) 또는 금융감독원(1332)에 신고하세요
                    """)
                    
                else:
                    st.success("✅ **안전한 번호입니다**")
                    st.info(result["message"])
                    st.write(f"**신뢰도:** {result['confidence']:.1%}")
                    
                    st.markdown("### 💡 안내")
                    st.info("현재 DB에서 보이스피싱 이력이 발견되지 않았지만, 새로운 번호일 수 있으므로 항상 주의하세요.")

# 구분선
st.markdown("---")

# 신고 섹션
st.subheader("🚨 보이스피싱 번호 신고")

with st.expander("보이스피싱 번호 신고하기"):
    st.write("보이스피싱을 당했거나 의심스러운 번호가 있다면 신고해주세요.")
    
    # 신고 폼
    with st.form("report_form"):
        report_phone = st.text_input(
            "신고할 전화번호",
            placeholder="예: 010-9876-5432"
        )
        
        reporter_name = st.text_input(
            "신고자 이름 (선택사항)",
            placeholder="익명으로 신고하려면 비워두세요"
        )
        
        description = st.text_area(
            "상세 내용",
            placeholder="어떤 방식으로 피싱을 시도했는지 설명해주세요",
            height=100
        )
        
        submit_report = st.form_submit_button("🚨 신고하기", type="primary")
        
        if submit_report:
            if not report_phone:
                st.error("신고할 전화번호를 입력해주세요.")
            elif not validate_phone_number(report_phone):
                st.error("올바른 전화번호 형식을 입력해주세요.")
            else:
                with st.spinner("신고 접수 중..."):
                    report_result = report_phone_number(
                        report_phone,
                        reporter_name if reporter_name else "익명",
                        description
                    )
                    
                    if report_result:
                        if report_result["status"] == "success":
                            st.success("✅ 신고가 성공적으로 접수되었습니다!")
                            st.balloons()
                        elif report_result["status"] == "exists":
                            st.info("ℹ️ 이미 신고된 번호입니다.")
                        
                        st.write(report_result["message"])

# 하단 정보
st.markdown("---")
st.markdown("### 📞 긴급 신고처")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**경찰서**\n📞 112")
with col2:
    st.info("**금융감독원**\n📞 1332")
with col3:
    st.info("**사이버경찰청**\n🌐 [cyber.go.kr](https://cyber.go.kr)")
