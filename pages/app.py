import streamlit as st
import pandas as pd

st.set_page_config(page_title="도서 찾기 앱", layout="wide")

st.title("📚 우리 동네 도서관 길잡이")
st.write("원하는 책이 도서관 어디에 있는지 쉽게 찾아보세요!")

# 1. 도서 데이터 (가장 단순화)
@st.cache_data
def get_data():
    return pd.DataFrame([
        {"도서명": "파이썬 완벽 가이드", "저자": "권철민", "위치": "2층 IT실", "서가": "B-04 (3번째 칸)", "청구기호": "005.133"},
        {"도서명": "돈의 속성", "저자": "김승호", "위치": "1층 경제실", "서가": "A-08 (2번째 칸)", "청구기호": "320.1"},
        {"도서명": "불편한 편의점", "저자": "김호연", "위치": "1층 문학실", "서가": "M-05 (1번째 칸)", "청구기호": "813.7"},
        {"도서명": "코스모스", "저자": "칼 세이건", "위치": "2층 과학실", "서가": "C-01 (4번째 칸)", "청구기호": "440.1"}
    ])

df = get_data()

# 세션(즐겨찾기) 저장소
if "bookmark" not in st.session_state:
    st.session_state.bookmark = []

# 2. 탭으로 화면 구성
tab1, tab2, tab3 = st.tabs(["🔍 책 찾기", "⭐ 내 즐겨찾기", "🤖 AI 도우미"])

# 첫 번째 탭: 책 찾기
with tab1:
    keyword = st.text_input("찾고 싶은 책 제목이나 저자를 입력하세요:")
    
    if keyword:
        result = df[df["도서명"].str.contains(keyword) | df["저자"].str.contains(keyword)]
    else:
        result = df
        
    for i, row in result.iterrows():
        st.markdown(f"### 📖 {row['도서명']} ({row['저자']})")
        st.write(f"📍 위치: **{row['위치']}** / 📌 서가: **{row['서가']}** / 🏷️ 청구기호: **{row['청구기호']}**")
        
        # 즐겨찾기 버튼 로직
        if row['도서명'] in st.session_state.bookmark:
            if st.button(f"❌ 즐겨찾기 취소 ({row['도서명']})"):
                st.session_state.bookmark.remove(row['도서명'])
                st.rerun()
        else:
            if st.button(f"⭐ 즐겨찾기 담기 ({row['도서명']})"):
                st.session_state.bookmark.append(row['도서명'])
                st.rerun()
        st.divider()

# 두 번째 탭: 즐겨찾기 목록
with tab2:
    st.subheader("내 탐색 목록")
    if not st.session_state.bookmark:
        st.info("아직 담아둔 책이 없습니다. 책을 검색하고 즐겨찾기에 담아보세요.")
    else:
        for book in st.session_state.bookmark:
            st.write(f"✅ **{book}**")
            
        if st.button("🗑️ 전체 삭제"):
            st.session_state.bookmark = []
            st.rerun()

# 세 번째 탭: AI 사서
with tab3:
    st.subheader("💡 도서관 AI 사서")
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    
    q = st.text_input("도서관 이용이나 책 위치 찾는 팁을 물어보세요.")
    
    if st.button("질문하기"):
        if not api_key:
            st.error("설정(Secrets)에 GEMINI_API_KEY가 등록되지 않았습니다.")
        elif q:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                
                with st.spinner("답변을 작성하고 있습니다..."):
                    res = model.generate_content(q)
                    st.write(res.text)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
