import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="스마트 도서관 길잡이", page_icon="📚", layout="wide")

# 2. 오류가 발생했던 CSS 스타일 코드를 100% 안전하게 수정
st.markdown("""
<style>
    .cover-1 { 
        background: linear-gradient(135deg, #A7C7E7 0%, #7DA0C4 100%); 
        padding: 8px 12px; 
        border-radius: 5px; 
        color: white; 
        font-weight: bold; 
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. 도서 샘플 데이터 생성
@st.cache_data
def load_books():
    return pd.DataFrame([
        {"id": 1, "title": "파이썬 머신러닝 완벽 가이드", "author": "권철민", "location": "2층 자연과학실", "shelf": "B-04 서가 3번째 선반", "call_number": "005.133-권36파"},
        {"id": 2, "title": "클린 코드", "author": "로버트 C. 마틴", "location": "2층 자연과학실", "shelf": "B-02 서가 1번째 선반", "call_number": "005.11-마898클"},
        {"id": 3, "title": "돈의 속성", "author": "김승호", "location": "1층 인문사회실", "shelf": "A-08 서가 2번째 선반", "call_number": "320.1-김897돈"},
        {"id": 4, "title": "코스모스", "author": "칼 세이건", "location": "2층 자연과학실", "shelf": "C-01 서가 4번째 선반", "call_number": "440.1-세04코"},
        {"id": 5, "title": "불편한 편의점", "author": "김호연", "location": "1층 문학자료실", "shelf": "M-05 서가 2번째 선반", "call_number": "813.7-김96불"}
    ])

books_df = load_books()

# 즐겨찾기 상태 초기화
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

st.title("📚 스마트 도서관 길잡이")
st.write("원하는 책의 위치를 쉽게 찾고 즐겨찾기에 담아 동선을 관리하세요.")

# 4. 탭으로 화면 분리
tab1, tab2, tab3 = st.tabs(["🔍 도서 검색 및 위치", "⭐ 내 즐겨찾기 목록", "🤖 AI 도우미"])

# 첫 번째 탭: 도서 검색
with tab1:
    search_query = st.text_input("책 제목이나 저자를 검색하세요", "")
    
    if search_query:
        filtered_df = books_df[
            books_df['title'].str.contains(search_query, case=False) | 
            books_df['author'].str.contains(search_query, case=False)
        ]
    else:
        filtered_df = books_df
        
    for _, row in filtered_df.iterrows():
        # HTML과 CSS를 적용한 배너 출력
        st.markdown(f"<div class='cover-1'>구역: {row['shelf'][:4]}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {row['title']}")
            st.write(f"✍️ 저자: {row['author']}")
            st.write(f"📍 **위치:** {row['location']} | 📌 **서가:** {row['shelf']} | 🏷️ **청구기호:** `{row['call_number']}`")
        
        with col2:
            # 즐겨찾기 추가/제거 버튼
            if row['id'] in st.session_state["favorites"]:
                if st.button(f"❌ 담기 취소", key=f"del_{row['id']}"):
                    st.session_state["favorites"].remove(row['id'])
                    st.rerun()
            else:
                if st.button(f"⭐ 위치 담기", key=f"add_{row['id']}"):
                    st.session_state["favorites"].append(row['id'])
                    st.rerun()
        st.divider()

# 두 번째 탭: 즐겨찾기 목록
with tab2:
    st.subheader("내가 찾을 책 목록 & 방문 위치")
    fav_books = books_df[books_df['id'].isin(st.session_state["favorites"])]
    
    if fav_books.empty:
        st.info("아직 즐겨찾기에 담긴 책이 없습니다. 도서 검색에서 책을 담아보세요.")
    else:
        st.dataframe(
            fav_books[["title", "location", "shelf", "call_number"]], 
            hide_index=True, 
            use_container_width=True,
            column_config={
                "title": "도서명",
                "location": "위치(층/실)",
                "shelf": "서가 번호",
                "call_number": "청구기호"
            }
        )
        if st.button("🗑️ 전체 삭제"):
            st.session_state["favorites"] = []
            st.rerun()

# 세 번째 탭: AI 도우미
with tab3:
    st.subheader("💡 도서관 AI 사서")
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    
    q = st.text_input("청구기호 뜻이나 도서관 이용 팁을 물어보세요.")
    
    if st.button("질문하기"):
        if not api_key:
            st.error("Streamlit Secrets에 GEMINI_API_KEY가 등록되지 않았습니다.")
        elif q:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                
                with st.spinner("답변을 작성하고 있습니다..."):
                    res = model.generate_content(q)
                    st.write(res.text)
            except Exception as e:
                st.error(f"API 오류가 발생했습니다: {e}")
