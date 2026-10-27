
import streamlit as st

# -------------------------
# 페이지 설정
# -------------------------
st.set_page_config(
    page_title="도서 즐겨찾기",
    page_icon="📚",
    layout="centered"
)

# -------------------------
# 파스텔 핑크 디자인
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

p, label {
    color: #594653;
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
    background-color: #ffffff;
}

div[data-testid="stTabs"] button[role="tab"] {
    color: #9b6681;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #b96f91;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #f0dce6;
    border-radius: 14px;
    background-color: #ffffff;
}

hr {
    border-color: #f0dce6;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 도서 데이터
# -------------------------
books = [
    {
        "제목": "파이썬 머신러닝 완벽 가이드",
        "저자": "권철민",
        "위치": "2층 자연과학실",
        "서가": "B-04 서가 3번째 선반",
        "청구기호": "005.133-권36파"
    },
    {
        "제목": "클린 코드",
        "저자": "로버트 C. 마틴",
        "위치": "2층 자연과학실",
        "서가": "B-02 서가 1번째 선반",
        "청구기호": "005.11-마898클"
    },
    {
        "제목": "돈의 속성",
        "저자": "김승호",
        "위치": "1층 인문사회실",
        "서가": "A-08 서가 2번째 선반",
        "청구기호": "320.1-김897돈"
    },
    {
        "제목": "코스모스",
        "저자": "칼 세이건",
        "위치": "2층 자연과학실",
        "서가": "C-01 서가 4번째 선반",
        "청구기호": "440.1-세04코"
    },
    {
        "제목": "불편한 편의점",
        "저자": "김호연",
        "위치": "1층 문학자료실",
        "서가": "M-05 서가 2번째 선반",
        "청구기호": "813.7-김96불"
    }
]

# -------------------------
# 즐겨찾기 초기화
# -------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# -------------------------
# 상단 제목
# -------------------------
st.title("📚 도서 즐겨찾기")
st.caption("관심 있는 책을 저장하고 편리하게 확인하세요.")

st.divider()

# 탭 구성
tab1, tab2 = st.tabs([
    "📖 도서 목록",
    "⭐ 즐겨찾기"
])

# -------------------------
# 탭 1: 도서 목록
# -------------------------
with tab1:
    st.subheader("도서 목록")
    st.write("마음에 드는 책을 즐겨찾기에 추가해 보세요.")

    for i, book in enumerate(books):
        with st.container(border=True):
            st.markdown(f"### {book['제목']}")
            st.write(f"저자: {book['저자']}")
            st.write(f"위치: {book['위치']}")
            st.write(f"서가: {book['서가']}")
            st.caption(f"청구기호: {book['청구기호']}")

            if book in st.session_state.favorites:
                st.button(
                    "⭐ 즐겨찾기 저장됨",
                    key=f"saved_{i}",
                    disabled=True,
                    use_container_width=True
                )

                if st.button(
                    "즐겨찾기에서 삭제",
                    key=f"remove_{i}",
                    use_container_width=True
                ):
                    st.session_state.favorites.remove(book)
                    st.rerun()

            else:
                if st.button(
                    "♡ 즐겨찾기 추가",
                    key=f"add_{i}",
                    use_container_width=True
                ):
                    st.session_state.favorites.append(book)
                    st.rerun()

# -------------------------
# 탭 2: 즐겨찾기 목록
# -------------------------
with tab2:
    st.subheader("⭐ 나의 즐겨찾기")

    favorites = st.session_state.favorites

    if len(favorites) > 0:
        st.write(f"저장한 책: **{len(favorites)}권**")

        for i, book in enumerate(favorites):
            with st.container(border=True):
                st.markdown(f"### {book['제목']}")
                st.write(f"저자: {book['저자']}")
                st.write(f"위치: {book['위치']}")
                st.write(f"서가: {book['서가']}")
                st.caption(f"청구기호: {book['청구기호']}")

                if st.button(
                    "삭제",
                    key=f"delete_{i}",
                    use_container_width=True
                ):
                    st.session_state.favorites.remove(book)
                    st.rerun()

        st.divider()

        if st.button(
            "전체 삭제",
            use_container_width=True
        ):
            st.session_state.favorites = []
            st.rerun()

    else:
        st.info(
            "아직 저장된 책이 없습니다. "
            "도서 목록에서 관심 있는 책을 추가해 보세요."
        )

# -------------------------
# 하단 안내
# -------------------------
st.divider()
st.caption("도서 즐겨찾기 서비스")
