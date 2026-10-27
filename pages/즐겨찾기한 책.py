
import streamlit as st
import requests

st.set_page_config(
    page_title="도서 즐겨찾기",
    page_icon="📚",
    layout="centered"
)

# =====================================
# 디자인
# =====================================
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
}
div[data-testid="stButton"] button:hover {
    background-color: #edc5d9;
    border-color: #dda8c2;
}
div[data-testid="stTextInput"] input {
    border: 1px solid #edc4d7;
    border-radius: 10px;
    background-color: white;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    border-radius: 10px;
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

# =====================================
# 추천 도서 데이터
# =====================================
recommendations = [
    {
        "title": "아몬드",
        "author": "손원평",
        "category": "소설",
        "description": "감정과 공감, 인간관계를 생각해 볼 수 있는 이야기"
    },
    {
        "title": "불편한 편의점",
        "author": "김호연",
        "category": "소설",
        "description": "일상 속 사람들의 관계와 따뜻함을 담은 소설"
    },
    {
        "title": "완득이",
        "author": "김려령",
        "category": "청소년",
        "description": "성장과 가족, 주변 사람들과의 관계를 다룬 이야기"
    },
    {
        "title": "체리새우: 비밀글입니다",
        "author": "황영미",
        "category": "청소년",
        "description": "친구 관계와 자신의 모습을 돌아보게 하는 소설"
    },
    {
        "title": "코스모스",
        "author": "칼 세이건",
        "category": "과학",
        "description": "우주와 생명, 인간의 존재를 탐구하는 과학 교양서"
    },
    {
        "title": "떨림과 울림",
        "author": "김상욱",
        "category": "과학",
        "description": "일상 속 현상을 물리학의 관점에서 바라보는 책"
    },
    {
        "title": "아픔이 길이 되려면",
        "author": "김승섭",
        "category": "보건·의학",
        "description": "사회 환경과 건강의 관계를 살펴보는 책"
    },
    {
        "title": "나는 간호사, 사람입니다",
        "author": "김현아",
        "category": "간호·의학",
        "description": "간호 현장과 환자를 돌보는 일에 대해 생각해 보는 책"
    },
    {
        "title": "팩트풀니스",
        "author": "한스 로슬링",
        "category": "인문·사회",
        "description": "세상을 데이터와 사실에 기반해 이해하도록 돕는 책"
    },
    {
        "title": "아주 작은 습관의 힘",
        "author": "제임스 클리어",
        "category": "자기계발",
        "description": "작은 행동을 지속하는 방법을 다룬 책"
    },
    {
        "title": "돈의 속성",
        "author": "김승호",
        "category": "경제",
        "description": "돈과 경제생활에 관한 관점을 다룬 책"
    },
    {
        "title": "클린 코드",
        "author": "로버트 C. 마틴",
        "category": "컴퓨터",
        "description": "읽기 쉽고 유지하기 좋은 코드를 작성하는 방법"
    }
]

# =====================================
# 세션 상태
# =====================================
if "favorites" not in st.session_state:
    st.session_state.favorites = {}

if "search_keyword" not in st.session_state:
    st.session_state.search_keyword = ""

if "search_page" not in st.session_state:
    st.session_state.search_page = 1

if "search_language" not in st.session_state:
    st.session_state.search_language = "모든 언어"

# =====================================
# 온라인 검색 함수
# =====================================
@st.cache_data(ttl=600, show_spinner=False)
def search_books(keyword, page, language):
    url = "https://openlibrary.org/search.json"

    params = {
        "q": keyword,
        "fields": "key,title,author_name,first_publish_year",
        "limit": 100,
        "page": page
    }

    if language == "한국어 도서":
        params["language"] = "kor"
    elif language == "영어 도서":
        params["language"] = "eng"

    response = requests.get(
        url,
        params=params,
        headers={"User-Agent": "StudentBookFavorites/1.0"},
        timeout=25
    )
    response.raise_for_status()

    data = response.json()
    results = []

    for item in data.get("docs", []):
        book_id = item.get("key")
        if not book_id:
            continue

        authors = item.get("author_name", [])
        results.append({
            "id": book_id,
            "title": item.get("title", "제목 정보 없음"),
            "author": ", ".join(authors[:3]) if authors
                      else "저자 정보 없음",
            "year": item.get("first_publish_year", "정보 없음")
        })

    return results, data.get("num_found", 0)

# =====================================
# 즐겨찾기 표시 함수
# =====================================
def show_book(book, key_prefix, category=None, description=None):
    book_id = book["id"]

    with st.container(border=True):
        st.markdown(f"### 📖 {book['title']}")
        st.write(f"저자: {book['author']}")

        if "year" in book:
            st.caption(f"출판 연도: {book['year']}")

        if category:
            st.write(f"분야: {category}")

        if description:
            st.caption(description)

        if book_id in st.session_state.favorites:
            st.button(
                "⭐ 즐겨찾기에 저장됨",
                key=f"saved_{key_prefix}_{book_id}",
                disabled=True,
                use_container_width=True
            )

            if st.button(
                "즐겨찾기에서 삭제",
                key=f"remove_{key_prefix}_{book_id}",
                use_container_width=True
            ):
                del st.session_state.favorites[book_id]
                st.rerun()
        else:
            if st.button(
                "♡ 즐겨찾기 추가",
                key=f"add_{key_prefix}_{book_id}",
                use_container_width=True
            ):
                st.session_state.favorites[book_id] = book
                st.rerun()

# =====================================
# 상단
# =====================================
st.title("📚 도서 즐겨찾기")
st.caption("추천 도서를 둘러보고 관심 있는 책을 저장하세요.")
st.divider()

# 추천 책 ID 만들기
for book in recommendations:
    book["id"] = "recommendation:" + book["title"]
    book["year"] = "정보 없음"

# =====================================
# 탭
# =====================================
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 추천 도서",
    "📚 분야별 도서",
    "🔎 도서 검색",
    "⭐ 즐겨찾기"
])

# =====================================
# 탭 1: 추천 도서
# =====================================
with tab1:
    st.subheader("추천 도서")
    st.write("다양한 분야에서 읽어 볼 만한 책을 모았어요.")

    for i, book in enumerate(recommendations):
        show_book(
            book,
            f"recommend_{i}",
            category=book["category"],
            description=book["description"]
        )

# =====================================
# 탭 2: 분야별 도서
# =====================================
with tab2:
    st.subheader("분야별 도서")

    categories = sorted(set(
        book["category"] for book in recommendations
    ))

    selected_category = st.selectbox(
        "원하는 분야를 선택하세요.",
        ["전체"] + categories
    )

    if selected_category == "전체":
        category_books = recommendations
    else:
        category_books = [
            book for book in recommendations
            if book["category"] == selected_category
        ]

    st.caption(f"도서 수: {len(category_books)}권")

    for i, book in enumerate(category_books):
        show_book(
            book,
            f"category_{selected_category}_{i}",
            category=book["category"],
            description=book["description"]
        )

    st.divider()
    st.caption(
        "더 많은 책은 도서 검색 탭에서 온라인으로 검색할 수 있어요."
    )

# =====================================
# 탭 3: 온라인 도서 검색
# =====================================
with tab3:
    st.subheader("온라인 도서 검색")

    with st.form("search_form"):
        keyword = st.text_input(
            "책 제목 또는 저자",
            value=st.session_state.search_keyword,
            placeholder="예: 간호학, 아몬드, 김호연"
        )

        language = st.selectbox(
            "검색 언어",
            ["모든 언어", "한국어 도서", "영어 도서"],
            index=[
                "모든 언어", "한국어 도서", "영어 도서"
            ].index(st.session_state.search_language)
        )

        submitted = st.form_submit_button(
            "책 검색",
            use_container_width=True
        )

    if submitted:
        if keyword.strip():
            st.session_state.search_keyword = keyword.strip()
            st.session_state.search_language = language
            st.session_state.search_page = 1
        else:
            st.warning("검색어를 입력해 주세요.")

    current_keyword = st.session_state.search_keyword

    if current_keyword:
        page = st.session_state.search_page

        try:
            with st.spinner("도서 정보를 불러오는 중..."):
                results, total = search_books(
                    current_keyword,
                    page,
                    st.session_state.search_language
                )

            st.caption(
                f"전체 검색 결과 약 {total:,}건 · {page}페이지"
            )

            if results:
                for i, book in enumerate(results):
                    show_book(book, f"online_{page}_{i}")

                previous_col, next_col = st.columns(2)

                with previous_col:
                    if page > 1:
                        if st.button(
                            "← 이전 페이지",
                            use_container_width=True
                        ):
                            st.session_state.search_page -= 1
                            st.rerun()

                with next_col:
                    if page * 100 < total:
                        if st.button(
                            "다음 페이지 →",
                            use_container_width=True
                        ):
                            st.session_state.search_page += 1
                            st.rerun()
            else:
                st.info("검색 결과가 없습니다.")

        except requests.RequestException:
            st.error(
                "온라인 도서 정보를 불러오지 못했습니다. "
                "인터넷 연결을 확인하고 다시 시도해 주세요."
            )
        except (ValueError, KeyError):
            st.error("도서 정보를 처리하지 못했습니다.")

    else:
        st.info("검색어를 입력하면 온라인 도서를 찾아볼 수 있어요.")

# =====================================
# 탭 4: 즐겨찾기
# =====================================
with tab4:
    st.subheader("⭐ 나의 즐겨찾기")

    favorites = st.session_state.favorites

    if favorites:
        st.write(f"저장한 책: **{len(favorites)}권**")

        for book_id, book in list(favorites.items()):
            with st.container(border=True):
                st.markdown(f"### 📖 {book['title']}")
                st.write(f"저자: {book['author']}")

                if book.get("year"):
                    st.caption(f"출판 연도: {book['year']}")

                if st.button(
                    "즐겨찾기에서 삭제",
                    key=f"favorite_delete_{book_id}",
                    use_container_width=True
                ):
                    del st.session_state.favorites[book_id]
                    st.rerun()

        st.divider()

        if st.button("전체 삭제", use_container_width=True):
            st.session_state.favorites = {}
            st.rerun()

    else:
        st.info("즐겨찾기에 저장한 책이 없습니다.")

# =====================================
# 하단
# =====================================
st.divider()
st.caption("도서 정보 검색: Open Library")
st.caption(
    "온라인 검색 결과는 실제 학교 도서관의 소장 여부와 다를 수 있습니다."
)
