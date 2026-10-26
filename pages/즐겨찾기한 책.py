import streamlit as st
import pandas as pd

# -------------------------------------------------------------------
# 1. 페이지 설정
# -------------------------------------------------------------------
st.set_page_config(
    page_title="도서관 위치 탐색기",
    page_icon="📚",
    layout="wide"
)

# -------------------------------------------------------------------
# 2. 샘플 데이터 준비
# -------------------------------------------------------------------
@st.cache_data
def load_data():
    return pd.DataFrame([
        {
            "id": 1,
            "title": "파이썬 머신러닝 완벽 가이드",
            "author": "권철민",
            "publisher": "위키북스",
            "category": "컴퓨터/IT",
            "call_number": "005.133-권36파",
            "location": "2층 자연과학실",
            "shelf": "B-04 서가 3번째 선반",
            "status": "대출가능"
        },
        {
            "id": 2,
            "title": "클린 코드 (Clean Code)",
            "author": "로버트 C. 마틴",
            "publisher": "인사이트",
            "category": "컴퓨터/IT",
            "call_number": "005.11-마898클",
            "location": "2층 자연과학실",
            "shelf": "B-02 서가 1번째 선반",
            "status": "대출가능"
        },
        {
            "id": 3,
            "title": "돈의 속성",
            "author": "김승호",
            "publisher": "스노우폭스북스",
            "category": "경제/경영",
            "call_number": "320.1-김897돈",
            "location": "1층 인문사회실",
            "shelf": "A-08 서가 2번째 선반",
            "status": "대출가능"
        },
        {
            "id": 4,
            "title": "코스모스 (Cosmos)",
            "author": "칼 세이건",
            "publisher": "사이언스북스",
            "category": "자연과학",
            "call_number": "440.1-세04코",
            "location": "2층 자연과학실",
            "shelf": "C-01 서가 4번째 선반",
            "status": "대출중"
        },
        {
            "id": 5,
            "title": "불편한 편의점",
            "author": "김호연",
            "publisher": "나무옆의자",
            "category": "문학",
            "call_number": "813.7-김96불",
            "location": "1층 문학자료실",
            "shelf": "M-05 서가 2번째 선반",
            "status": "대출가능"
        },
        {
            "id": 6,
            "title": "아몬드",
            "author": "손원평",
            "publisher": "창비",
            "category": "문학",
            "call_number": "813.7-손75아",
            "location": "1층 문학자료실",
            "shelf": "M-03 서가 5번째 선반",
            "status": "대출가능"
        }
    ])

# 세션 상태(즐겨찾기 저장소) 초기화
if "fav_list" not in st.session_state:
    st.session_state["fav_list"] = []

df = load_data()

# -------------------------------------------------------------------
# 3. 사이드바 (메뉴)
# -------------------------------------------------------------------
st.sidebar.title("📚 도서관 스마트 도우미")
menu = st.sidebar.radio("메뉴를 선택하세요", ["📖 책 검색 & 위치 찾기", "⭐ 내 즐겨찾기 (방문 목록)", "💡 AI 사서에게 물어보기"])

# -------------------------------------------------------------------
# 4. [메뉴 1] 도서 검색 및 위치 확인
# -------------------------------------------------------------------
if menu == "📖 책 검색 & 위치 찾기":
    st.title("🔍 도서 검색 및 위치 확인")
    st.write("원하는 책의 제목이나 저자를 검색하면 정확한 서가 위치를 알려드립니다.")

    query = st.text_input("검색어 입력 (제목, 저자, 카테고리)", "")

    if query:
        result = df[
            df['title'].str.contains(query, case=False, na=False) |
            df['author'].str.contains(query, case=False, na=False) |
            df['category'].str.contains(query, case=False, na=False)
        ]
    else:
        result = df

    st.subheader(f"총 {len(result)}권의 도서가 있습니다.")
    st.divider()

    for idx, item in result.iterrows():
        col1, col2, col3 = st.columns([3, 2, 1])

        with col1:
            st.markdown(f"### 📖 {item['title']}")
            st.write(f"✍️ 저자: {item['author']} | 🏢 출판사: {item['publisher']}")
            st.code(f"청구기호: {item['call_number']}")

        with col2:
            st.markdown(f"📍 **위치:** {item['location']}")
            st.markdown(f"📌 **서가:** {item['shelf']}")
            if item['status'] == "대출가능":
                st.success(f"상태: {item['status']}")
            else:
                st.error(f"상태: {item['status']}")

        with col3:
            book_id = item['id']
            if book_id in st.session_state["fav_list"]:
                if st.button("❌ 담기 취소", key=f"btn_remove_{book_id}"):
                    st.session_state["fav_list"].remove(book_id)
                    st.rerun()
            else:
                if st.button("⭐ 위치 담기", key=f"btn_add_{book_id}"):
                    st.session_state["fav_list"].append(book_id)
                    st.rerun()

        st.divider()

# -------------------------------------------------------------------
# 5. [메뉴 2] 즐겨찾기 목록 및 이동 동선
# -------------------------------------------------------------------
elif menu == "⭐ 내 즐겨찾기 (방문 목록)":
    st.title("⭐ 내가 찾아야 할 책 목록")
    st.write("선택한 책들의 위치를 층별로 모아서 가장 효율적인 동선을 안내합니다.")

    fav_ids = st.session_state["fav_list"]
    fav_df = df[df['id'].isin(fav_ids)]

    if fav_df.empty:
        st.warning("아직 담은 책이 없습니다. '책 검색' 메뉴에서 찾아야 할 책을 추가해 보세요!")
    else:
        st.success(f"현재 총 {len(fav_df)}권의 책이 저장되어 있습니다.")

        # 목록 테이블 표시
        st.dataframe(
            fav_df[["title", "location", "shelf", "call_number", "status"]],
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🗺️ Recommended Floor Path (층별 찾아가는 순서)")
        
        # 층별 그룹화 안내
        grouped = fav_df.groupby("location")
        for loc, group in grouped:
            st.markdown(f"#### 📍 **{loc}**")
            for _, b in group.iterrows():
                st.write(f"- **{b['title']}** → [{b['shelf']}] (청구기호: `{b['call_number']}`)")
            st.write("")

        if st.button("🗑️ 전체 목록 비우기"):
            st.session_state["fav_list"] = []
            st.rerun()

# -------------------------------------------------------------------
# 6. [메뉴 3] AI 사서 기능
# -------------------------------------------------------------------
elif menu == "💡 AI 사서에게 물어보기":
    st.title("💡 AI 도서관 도우미")
    st.write("도서관 이용법이나 청구기호 읽는 방법에 대해 궁금한 점을 질문하세요.")

    api_key = st.secrets.get("GEMINI_API_KEY", None)
    user_q = st.text_area("질문을 작성하세요", placeholder="예: 청구기호 '005.133'이 어떤 분야를 나타내는지 알려주세요.")

    if st.button("질문 보내기"):
        if not user_q.strip():
            st.warning("질문 내용을 입력해 주세요.")
        elif not api_key:
            st.error("Secrets 설정에 GEMINI_API_KEY가 없습니다.")
            st.info("💡 **기본 안내**: 청구기호 앞자리가 000이면 IT/컴퓨터, 800이면 문학 분야 서가입니다.")
        else:
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash-lite")
                
                with st.spinner("AI가 답변을 생성 중입니다..."):
                    res = model.generate_content(f"도서관 사서로서 친절히 답해주세요: {user_q}")
                    st.markdown("### 💬 AI 답변")
                    st.write(res.text)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
