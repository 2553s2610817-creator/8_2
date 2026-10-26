import streamlit as st
import pandas as pd

# -------------------------------------------------------------------
# 1. 페이지 설정
# -------------------------------------------------------------------
st.set_page_config(
    page_title="스마트 도서관 길잡이",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------
# 2. 커스텀 CSS 스타일 적용 (SyntaxError 방지를 위해 st.markdown 내부 커버)
# -------------------------------------------------------------------
st.markdown("""
<style>
    /* 메인 커스텀 스타일 */
    .book-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e0e0e0;
    }
    
    /* 서가 표식 그래디언트 배너 */
    .cover-banner {
        background: linear-gradient(135deg, #A7C7E7 0%, #7DA0C4 100%);
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 8px;
    }

    .call-number-badge {
        background-color: #f1f3f5;
        color: #333;
        padding: 4px 8px;
        border-radius: 4px;
        font-family: monospace;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# 3. 샘플 데이터 준비 및 세션 상태 초기화
# -------------------------------------------------------------------
@st.cache_data
def load_sample_books():
    return pd.DataFrame([
        {
            "id": 1,
            "title": "파이썬 머신러닝 완벽 가이드",
            "author": "권철민",
            "publisher": "위키북스",
            "category": "컴퓨터/IT",
            "call_number": "005.133-권36파",
            "location_floor": "2층 자연과학실",
            "shelf_no": "B-04",
            "shelf_row": "3번째 선반",
            "status": "대출가능"
        },
        {
            "id": 2,
            "title": "클린 코드 (Clean Code)",
            "author": "로버트 C. 마틴",
            "publisher": "인사이트",
            "category": "컴퓨터/IT",
            "call_number": "005.11-마898클",
            "location_floor": "2층 자연과학실",
            "shelf_no": "B-02",
            "shelf_row": "1번째 선반",
            "status": "대출가능"
        },
        {
            "id": 3,
            "title": "돈의 속성",
            "author": "김승호",
            "publisher": "스노우폭스북스",
            "category": "경제/경영",
            "call_number": "320.1-김897돈",
            "location_floor": "1층 인문사회실",
            "shelf_no": "A-08",
            "shelf_row": "2번째 선반",
            "status": "대출가능"
        },
        {
            "id": 4,
            "title": "코스모스 (Cosmos)",
            "author": "칼 세이건",
            "publisher": "사이언스북스",
            "category": "자연과학",
            "call_number": "440.1-세04코",
            "location_floor": "2층 자연과학실",
            "shelf_no": "C-01",
            "shelf_row": "4번째 선반",
            "status": "대출중"
        },
        {
            "id": 5,
            "title": "불편한 편의점",
            "author": "김호연",
            "publisher": "나무옆의자",
            "category": "문학",
            "call_number": "813.7-김96불",
            "location_floor": "1층 문학자료실",
            "shelf_no": "M-05",
            "shelf_row": "2번째 선반",
            "status": "대출가능"
        },
        {
            "id": 6,
            "title": "아몬드",
            "author": "손원평",
            "publisher": "창비",
            "category": "문학",
            "call_number": "813.7-손75아",
            "location_floor": "1층 문학자료실",
            "shelf_no": "M-03",
            "shelf_row": "5번째 선반",
            "status": "대출가능"
        },
        {
            "id": 7,
            "title": "사피엔스",
            "author": "유발 하라리",
            "publisher": "김영사",
            "category": "역사/문화",
            "call_number": "909-하95사",
            "location_floor": "1층 인문사회실",
            "shelf_no": "A-12",
            "shelf_row": "1번째 선반",
            "status": "대출가능"
        }
    ])

if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

books_df = load_sample_books()

# -------------------------------------------------------------------
# 4. 사이드바
# -------------------------------------------------------------------
st.sidebar.title("📚 스마트 도서관")
st.sidebar.caption("헤매지 않고 빠르게 책 찾기")

menu = st.sidebar.radio(
    "메뉴 선택",
    ["📖 도서 검색 및 위치 안내", "⭐ 즐겨찾는 책 (내 탐색 목록)", "💡 AI 도서관 도우미"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **도서 탐색 꿀팁**\n\n"
    "1. **위치(층/실)**와 **서가 번호(예: B-04)**를 먼자 찾으세요.\n"
    "2. 청구기호의 숫자는 분류 주제, 뒤의 문자는 저자 이름입니다."
)

# -------------------------------------------------------------------
# 5. [메뉴 1] 도서 검색 및 위치 안내
# -------------------------------------------------------------------
if menu == "📖 도서 검색 및 위치 안내":
    st.title("🔍 도서 검색 & 서가 위치 확인")
    st.write("찾으려는 책을 검색하고 서가 위치와 청구기호를 확인하세요.")

    search_term = st.text_input("책 제목, 저자, 또는 카테고리를 입력하세요", "")

    if search_term:
        filtered_df = books_df[
            books_df['title'].str.contains(search_term, case=False, na=False) |
            books_df['author'].str.contains(search_term, case=False, na=False) |
            books_df['category'].str.contains(search_term, case=False, na=False)
        ]
    else:
        filtered_df = books_df

    st.subheader(f"📚 검색 결과 ({len(filtered_df)}건)")

    if filtered_df.empty:
        st.warning("검색 결과가 없습니다.")
    else:
        for idx, row in filtered_df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"<div class='cover-banner'>구역: {row['shelf_no']}</div>", unsafe_allow_html=True)
                    st.markdown(f"### **{row['title']}**")
                    st.write(f"✍️ 저자: {row['author']} | 🏢 출판사: {row['publisher']}")
                    st.markdown(f"🏷️ 청구기호: <span class='call-number-badge'>{row['call_number']}</span>", unsafe_allow_html=True)

                with col2:
                    st.markdown(f"📍 **위치:** {row['location_floor']}")
                    st.markdown(f"📌 **서가:** `{row['shelf_no']}` ({row['shelf_row']})")
                    if row['status'] == "대출가능":
                        st.success(f"상태: {row['status']}")
                    else:
                        st.error(f"상태: {row['status']}")

                with col3:
                    is_fav = row['id'] in st.session_state["favorites"]
                    if is_fav:
                        if st.button("❌ 제거", key=f"del_{row['id']}"):
                            st.session_state["favorites"].remove(row['id'])
                            st.rerun()
                    else:
                        if st.button("⭐ 즐겨찾기", key=f"add_{row['id']}"):
                            st.session_state["favorites"].append(row['id'])
                            st.rerun()

            st.markdown("---")

# -------------------------------------------------------------------
# 6. [메뉴 2] 즐겨찾는 책 목록 & 동선 가이드
# -------------------------------------------------------------------
elif menu == "⭐ 즐겨찾는 책 (내 탐색 목록)":
    st.title("⭐ 내 탐색 목록 & 최적 동선")
    st.write("방문 시 한 번에 책을 찾을 수 있도록 동선을 정리해 드립니다.")

    fav_ids = st.session_state["favorites"]
    fav_books = books_df[books_df['id'].isin(fav_ids)]

    if fav_books.empty:
        st.info("즐겨찾기에 담긴 책이 없습니다. 검색 메뉴에서 책을 담아보세요!")
    else:
        st.success(f"총 {len(fav_books)}권의 책이 선택되었습니다.")

        st.dataframe(
            fav_books[["title", "location_floor", "shelf_no", "shelf_row", "call_number", "status"]],
            column_config={
                "title": "도서명",
                "location_floor": "위치(층)",
                "shelf_no": "서가 번호",
                "shelf_row": "세부 선반",
                "call_number": "청구기호",
                "status": "상태"
            },
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🗺️ 층별 추천 방문 경로")
        grouped = fav_books.groupby("location_floor")
        for floor, group in grouped:
            with st.expander(f"📍 **{floor}** ({len(group)}권)", expanded=True):
                for _, book in group.iterrows():
                    st.write(f"- **{book['title']}** 👉 서가 `{book['shelf_no']}` [{book['shelf_row']}] (청구기호: `{book['call_number']}`)")

        if st.button("🗑️ 전체 삭제"):
            st.session_state["favorites"] = []
            st.rerun()

# -------------------------------------------------------------------
# 7. [메뉴 3] AI 도서관 도우미
# -------------------------------------------------------------------
elif menu == "💡 AI 도서관 도우미":
    st.title("💡 AI 도서관 도우미")
    st.write("청구기호 뜻이나 도서관 탐색 관련 질문을 AI에게 물어보세요.")

    api_key = st.secrets.get("GEMINI_API_KEY", None)

    user_query = st.text_area(
        "질문 입력",
        placeholder="예: 청구기호 005.133이 무엇을 의미하나요?"
    )

    if st.button("🤖 AI 질문하기"):
        if not user_query.strip():
            st.warning("질문을 입력해 주세요.")
        elif not api_key:
            st.error("Secrets에 `GEMINI_API_KEY`가 설정되지 않았습니다.")
            st.info("💡 **기본 안내**: 000번대는 총류/컴퓨터공학, 800번대는 문학 분류입니다.")
        else:
            try:
                import google.generativeai as genai

                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash-lite")

                prompt = f"도서관 사서로서 친절하게 답변해 주세요:\n{user_query}"

                with st.spinner("답변을 생성하는 중입니다..."):
                    response = model.generate_content(prompt)
                    st.markdown("### 💬 AI 답변:")
                    st.write(response.text)

            except Exception as e:
                st.error(f"오류가 발생했습니다: {str(e)}")
