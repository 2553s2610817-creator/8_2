import streamlit as st
import pandas as pd
import json
import os

# Streamlit 페이지 기본 설정
st.set_page_config(
    page_title="스마트 도서관 길잡이",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------------
# [초기 데이터 준비] - 도서관 샘플 데이터 생성
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
            "shelf_row": "3번째 칸",
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
            "shelf_row": "1번째 칸",
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
            "shelf_row": "2번째 칸",
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
            "shelf_row": "4번째 칸",
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
            "shelf_row": "2번째 칸",
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
            "shelf_row": "5번째 칸",
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
            "shelf_row": "1번째 칸",
            "status": "대출가능"
        }
    ])

# 세션 상태 초기화 (즐겨찾기 목록 저장)
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

books_df = load_sample_books()

# -------------------------------------------------------------------
# [사이드바] 메뉴 및 안내
# -------------------------------------------------------------------
st.sidebar.title("📚 스마트 도서관")
st.sidebar.caption("헤매지 않고 빠르게 책 찾기")

menu = st.sidebar.radio(
    "메뉴 선택",
    ["📖 도서 검색 및 위치 안내", "⭐ 즐겨찾는 책 (내 탐색 목록)", "💡 AI 도서관 도우미"]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **도서 찾기 팁**\n\n"
    "1. **청구기호**의 앞 세 자리는 학문 분야입니다.\n"
    "2. 서가 측면의 **구역 번호(예: A-08)**를 먼저 찾아가세요.\n"
    "3. 위에서부터 몇 번째 칸인지 확인하면 시간을 훨씬 단축할 수 있습니다."
)

# -------------------------------------------------------------------
# [메뉴 1] 도서 검색 및 위치 안내
# -------------------------------------------------------------------
if menu == "📖 도서 검색 및 위치 안내":
    st.title("🔍 도서 검색 & 서가 위치 찾기")
    st.write("찾고 싶은 책의 이름, 저자, 카테고리를 검색하여 정확한 위치를 확인하세요.")

    # 검색 입력 창
    search_term = st.text_input("책 제목, 저자, 또는 카테고리를 입력하세요", "")

    # 검색 필터링
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
        st.warning("찾으시는 도서가 없습니다. 다른 검색어를 입력해 보세요.")
    else:
        for idx, row in filtered_df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"### **{row['title']}**")
                    st.write(f"✍️ 저자: {row['author']} | 🏢 출판사: {row['publisher']} | 🏷️ 카테고리: {row['category']}")
                    st.markdown(f"🏷️ **청구기호:** `{row['call_number']}`")

                with col2:
                    st.markdown(f"📍 **위치:** {row['location_floor']}")
                    st.markdown(f"📌 **서가 번호:** `{row['shelf_no']}` ({row['shelf_row']})")
                    if row['status'] == "대출가능":
                        st.success(f"상태: {row['status']}")
                    else:
                        st.error(f"상태: {row['status']}")

                with col3:
                    # 즐겨찾기 버튼
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
# [메뉴 2] 즐겨찾는 책 (내 탐색 목록)
# -------------------------------------------------------------------
elif menu == "⭐ 즐겨찾는 책 (내 탐색 목록)":
    st.title("⭐ 내가 찾으려는 책 목록 & 위치 모아보기")
    st.write("방문 시 한 번에 찾을 수 있도록 즐겨찾기한 도서들의 동선과 위치를 안내합니다.")

    fav_ids = st.session_state["favorites"]
    fav_books = books_df[books_df['id'].isin(fav_ids)]

    if fav_books.empty:
        st.info("현재 즐겨찾기에 담긴 책이 없습니다. '도서 검색' 메뉴에서 책을 추가해 보세요!")
    else:
        st.success(f"총 {len(fav_books)}권의 책이 즐겨찾기에 등록되어 있습니다.")

        # 즐겨찾기 목록 요약 데이터 프레임
        st.dataframe(
            fav_books[["title", "location_floor", "shelf_no", "shelf_row", "call_number", "status"]],
            column_config={
                "title": "도서명",
                "location_floor": "위치(층/실)",
                "shelf_no": "서가 번호",
                "shelf_row": "세부 선반",
                "call_number": "청구기호",
                "status": "대출 상태"
            },
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🗺️ 서가 방문 동선 가이드")
        st.write("층 및 서가 구역별로 묶어서 찾으시면 시간을 단축할 수 있습니다:")

        # 층별 그룹화 안내
        grouped = fav_books.groupby("location_floor")
        for floor, group in grouped:
            with st.expander(f"📍 **{floor}** 에서 찾아야 할 책 ({len(group)}권)", expanded=True):
                for _, book in group.iterrows():
                    st.write(f"- **{book['title']}** → 서가 **{book['shelf_no']}** [{book['shelf_row']}] (청구기호: `{book['call_number']}`)")

        # 전체 비우기 버튼
        if st.button("🗑️ 즐겨찾기 전체 삭제"):
            st.session_state["favorites"] = []
            st.rerun()

# -------------------------------------------------------------------
# [메뉴 3] AI 도서관 도우미 (Gemini API 활용)
# -------------------------------------------------------------------
elif menu == "💡 AI 도서관 도우미":
    st.title("💡 AI 도서관 도우미")
    st.write("책의 청구기호 해석이나, 넓은 도서관에서 효율적으로 책을 찾는 팁을 질문해 보세요.")

    # Gemini API 설정
    api_key = st.secrets.get("GEMINI_API_KEY", None)

    user_query = st.text_area(
        "도서관 이용 질문 입력",
        placeholder="예: 청구기호 '005.133-권36파'가 무슨 뜻인가요? 또는 책을 빨리 찾는 순서 규칙을 알려주세요."
    )

    if st.button("🤖 AI에게 질문하기"):
        if not user_query.strip():
            st.warning("질문을 입력해 주세요.")
        elif not api_key:
            st.error("Secrets에 `GEMINI_API_KEY`가 설정되어 있지 않습니다. 기본 가이드를 참조하세요.")
            st.info("💡 **기본 청구기호 읽는 법**: 000번대는 총류(컴퓨터 등), 800번대는 문학입니다. 숫자 뒤 문자는 저자의 성씨를 의미합니다.")
        else:
            try:
                import google.generativeai as genai

                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash-lite")

                prompt = f"""
                당신은 도서관 이용을 돕는 친절한 사서 AI입니다.
                사용자의 도서관 위치 및 책 찾기 관련 질문에 명쾌하고 알기 쉽게 답변해 주세요.

                질문: {user_query}
                """

                with st.spinner("AI 사서가 답변을 작성 중입니다..."):
                    response = model.generate_content(prompt)
                    st.markdown("### 💬 AI 사서의 답변:")
                    st.write(response.text)

            except Exception as e:
                st.error(f"API 호출 중 오류가 발생했습니다: {str(e)}")
