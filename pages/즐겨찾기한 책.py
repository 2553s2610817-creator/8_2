
import streamlit as st

st.set_page_config(
    page_title="도서 즐겨찾기",
    page_icon="📚",
    layout="centered"
)

# -------------------------
# 디자인: 파스텔 핑크
# -------------------------
st.markdown("""
<style>
.stApp {
    background-color: #fff8fb;
    color: #594653;
}

h1, h2, h3 {
    color: #b96f91 !important;
}

div[data-testid="stButton"] button {
    background-color: #f7dce8;
    color: #765268;
    border: 1px solid #edc4d7;
    border-radius: 10px;
    transition: 0.2s;
}

div[data-testid="stButton"] button:hover {
    background-color: #edc5d9;
    border-color: #dda8c2;
    color: #68435a;
}

div[data-testid="stTextInput"] input {
    border: 1px solid #edc4d7;
    border-radius: 10px;
    background-color: white;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #f0dce6;
    border-radius: 14px;
    background-color: white;
}

hr {
    border-color: #f0dce6;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 도서 목록 30권
# 위치는 프로젝트용 예시
# -------------------------
books = [
    {"제목": "아몬드", "저자": "손원평", "분야": "소설", "위치": "1층 문학자료실"},
    {"제목": "불편한 편의점", "저자": "김호연", "분야": "소설", "위치": "1층 문학자료실"},
    {"제목": "완득이", "저자": "김려령", "분야": "소설", "위치": "1층 문학자료실"},
    {"제목": "페인트", "저자": "이희영", "분야": "소설", "위치": "1층 문학자료실"},
    {"제목": "체리새우: 비밀글입니다", "저자": "황영미", "분야": "소설", "위치": "1층 문학자료실"},
    {"제목": "순례 주택", "저자": "유은실", "분야": "소설", "위치": "1층 문학자료실"},
    {"제목": "모순", "저자": "양귀자", "분야": "소설", "위치": "1층 문학자료실"},
    {"제목": "소년이 온다", "저자": "한강", "분야": "소설", "위치": "1층 문학자료실"},
    {"제목": "채식주의자", "저자": "한강", "분야": "소설", "위치": "1층 문학자료실"},
    {"제목": "나미야 잡화점의 기적", "저자": "히가시노 게이고", "분야": "소설", "위치": "1층 문학자료실"},
    {"제목": "해리 포터와 마법사의 돌", "저자": "J.K. 롤링", "분야": "판타지", "위치": "1층 문학자료실"},
    {"제목": "어린 왕자", "저자": "앙투안 드 생텍쥐페리", "분야": "고전", "위치": "1층 문학자료실"},
    {"제목": "데미안", "저자": "헤르만 헤세", "분야": "고전", "위치": "1층 문학자료실"},
    {"제목": "1984", "저자": "조지 오웰", "분야": "고전", "위치": "1층 문학자료실"},
    {"제목": "위대한 개츠비", "저자": "F. 스콧 피츠제럴드", "분야": "고전", "위치": "1층 문학자료실"},
    {"제목": "미움받을 용기", "저자": "기시미 이치로, 고가 후미타케", "분야": "인문", "위치": "1층 인문사회실"},
    {"제목": "아주 작은 습관의 힘", "저자": "제임스 클리어", "분야": "자기계발", "위치": "1층 인문사회실"},
    {"제목": "역행자", "저자": "자청", "분야": "자기계발", "위치": "1층 인문사회실"},
    {"제목": "돈의 속성", "저자": "김승호", "분야": "경제", "위치": "1층 인문사회실"},
    {"제목": "부자 아빠 가난한 아빠", "저자": "로버트 기요사키", "분야": "경제", "위치": "1층 인문사회실"},
    {"제목": "코스모스", "저자": "칼 세이건", "분야": "과학", "위치": "2층 자연과학실"},
    {"제목": "이기적 유전자", "저자": "리처드 도킨스", "분야": "과학", "위치": "2층 자연과학실"},
    {"제목": "시간은 흐르지 않는다", "저자": "카를로 로벨리", "분야": "과학", "위치": "2층 자연과학실"},
    {"제목": "떨림과 울림", "저자": "김상욱", "분야": "과학", "위치": "2층 자연과학실"},
    {"제목": "클린 코드", "저자": "로버트 C. 마틴", "분야": "컴퓨터", "위치": "2층 자연과학실"},
    {"제목": "파이썬 머신러닝 완벽 가이드", "저자": "권철민", "분야": "컴퓨터", "위치": "2층 자연과학실"},
    {"제목": "세상을 바꾼 의학의 역사", "저자": "관련 의학 교양 도서", "분야": "의학", "위치": "2층 자연과학실"},
    {"제목": "나는 간호사, 사람입니다", "저자": "김현아", "분야": "간호", "위치": "2층 자연과학실"},
    {"제목": "아픔이 길이 되려면", "저자": "김승섭", "분야": "보건", "위치": "2층 자연과학실"},
    {"제목": "팩트풀니스", "저자": "한스 로슬링", "분야": "교양", "위치": "1층 인문사회실"}
]

# -------------------------
# 즐겨찾기 초기화
# -------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# -------------------------
# 제목
# -------------------------
st.title("📚 도서 즐겨찾기")
st.caption("책을 검색하고 관심 있는 도서를 저장해 보세요.")

st.divider()

tab1, tab2 = st.tabs(["🔎 도서 검색", "⭐ 즐겨찾기"])

# -------------------------
# 탭 1: 검색 및 추가
# -------------------------
with tab1:
    st.subheader("도서 검색")

    keyword = st.text_input(
        "책 제목 또는 저자 검색",
        placeholder="예: 아몬드, 손원평, 간호..."
    )

    category = st.selectbox(
        "분야 선택",
        ["전체", "소설", "판타지", "고전", "인문", "자기계발",
         "경제", "과학", "컴퓨터", "의학", "간호", "보건", "교양"]
    )

    filtered_books = []

    for book in books:
        matches_keyword = (
            keyword.strip().lower() in book["제목"].lower()
            or keyword.strip().lower() in book["저자"].lower()
            or keyword.strip().lower() in book["분야"].lower()
        )

        matches_category = (
            category == "전체" or book["분야"] == category
        )

        if matches_keyword and matches_category:
            filtered_books.append(book)

    st.caption(f"검색 결과: {len(filtered_books)}권")

    if filtered_books:
        for i, book in enumerate(filtered_books):
            with st.container(border=True):
                st.markdown(f"### 📖 {book['제목']}")
                st.write(f"저자: {book['저자']}")
                st.write(f"분야: {book['분야']}")
                st.write(f"도서관 위치(예시): {book['위치']}")

                if book in st.session_state.favorites:
                    st.button(
                        "⭐ 즐겨찾기에 저장됨",
                        key=f"saved_{i}_{book['제목']}",
                        disabled=True,
                        use_container_width=True
                    )
                else:
                    if st.button(
                        "♡ 즐겨찾기 추가",
                        key=f"add_{i}_{book['제목']}",
                        use_container_width=True
                    ):
                        st.session_state.favorites.append(book)
                        st.rerun()
    else:
        st.info("검색 결과가 없습니다. 다른 제목이나 저자를 입력해 보세요.")

# -------------------------
# 탭 2: 즐겨찾기 목록
# -------------------------
with tab2:
    st.subheader("⭐ 나의 즐겨찾기")

    favorites = st.session_state.favorites

    if favorites:
        st.write(f"저장한 책: **{len(favorites)}권**")

        for i, book in enumerate(favorites):
            with st.container(border=True):
                st.markdown(f"### 📖 {book['제목']}")
                st.write(f"저자: {book['저자']}")
                st.write(f"분야: {book['분야']}")
                st.write(f"도서관 위치(예시): {book['위치']}")

                if st.button(
                    "즐겨찾기에서 삭제",
                    key=f"delete_{i}_{book['제목']}",
                    use_container_width=True
                ):
                    st.session_state.favorites.remove(book)
                    st.rerun()

        st.divider()

        if st.button("전체 삭제", use_container_width=True):
            st.session_state.favorites = []
            st.rerun()
    else:
        st.info("즐겨찾기에 저장한 책이 없습니다.")

st.divider()
st.caption("도서 즐겨찾기 서비스 · 파스텔 핑크 테마")
