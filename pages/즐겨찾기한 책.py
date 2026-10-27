
import streamlit as st
import requests

# =====================================
# 페이지 설정
# =====================================
st.set_page_config(
    page_title="도서 즐겨찾기",
    page_icon="📚",
    layout="centered"
)

# =====================================
# 파스텔 핑크 디자인
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

div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    border-radius: 10px;
}

hr {
    border-color: #f0dce6;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# 세션 상태
# =====================================
if "favorites" not in st.session_state:
    st.session_state.favorites = {}

if "search_keyword" not in st.session_state:
    st.session_state.search_keyword = ""

if "page" not in st.session_state:
    st.session_state.page = 1

# =====================================
# 온라인 도서 검색
# Open Library Search API
# =====================================
@st.cache_data(ttl=600, show_spinner=False)
def search_books(keyword, page, language):
    url = "https://openlibrary.org/search.json"

    params = {
        "q": keyword,
        "fields": "key,title,author_name,first_publish_year,edition_count",
        "limit": 100,
        "page": page
    }

    if language == "한국어 도서":
        params["language"] = "kor"
    elif language == "영어 도서":
        params["language"] = "eng"

    headers = {
        "User-Agent": "BookFavoritesStudentProject/1.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=25
    )
    response.raise_for_status()

    data = response.json()
    results = []

    for item in data.get("docs", []):
        title = item.get("title", "제목 정보 없음")
        authors = item.get("author_name", [])
        author = ", ".join(authors[:3]) if authors else "저자 정보 없음"
        year = item.get("first_publish_year", "정보 없음")
        book_id = item.get("key")

        if not book_id:
            continue

        results.append({
            "id": book_id,
            "제목": title,
            "저자": author,
            "출판연도": year,
            "판본수": item.get("edition_count", 0)
        })

    return results, data.get("num_found", 0)

# =====================================
# 상단 제목
# =====================================
st.title("📚 도서 즐겨찾기")
st.caption("읽고 싶은 책을 검색하고 관심 도서를 저장하세요.")
st.divider()

tab1, tab2 = st.tabs([
    "🔎 도서 검색",
    "⭐ 즐겨찾기"
])

# =====================================
# 탭 1: 도서 검색
# =====================================
with tab1:
    st.subheader("도서 검색")

    with st.form("search_form"):
        keyword = st.text_input(
            "책 제목 또는 저자 이름",
            value=st.session_state.search_keyword,
            placeholder="예: 아몬드, 해리 포터, 김호연"
        )

        language = st.selectbox(
            "검색 언어",
            ["모든 언어", "한국어 도서", "영어 도서"]
        )

        submitted = st.form_submit_button(
            "책 검색",
            use_container_width=True
        )

    if submitted:
        if keyword.strip():
            st.session_state.search_keyword = keyword.strip()
            st.session_state.search_language = language
            st.session_state.page = 1
        else:
            st.warning("검색어를 입력해 주세요.")

    current_keyword = st.session_state.search_keyword
    current_language = st.session_state.get(
        "search_language", "모든 언어"
    )

    if current_keyword:
        page = st.session_state.page

        try:
            with st.spinner("도서 정보를 불러오는 중입니다..."):
                results, total = search_books(
                    current_keyword,
                    page,
                    current_language
                )

            st.write(f"검색어: **{current_keyword}**")
            st.caption(
                f"전체 검색 결과 약 {total:,}건 · {page}페이지"
            )

            if results:
                for i, book in enumerate(results):
                    with st.container(border=True):
                        st.markdown(f"### 📖 {book['제목']}")
                        st.write(f"저자: {book['저자']}")
                        st.write(f"출판 연도: {book['출판연도']}")

                        if book["판본수"]:
                            st.caption(
                                f"등록된 판본 수: {book['판본수']}"
                            )

                        book_id = book["id"]

                        if book_id in st.session_state.favorites:
                            st.button(
                                "⭐ 즐겨찾기에 저장됨",
                                key=f"saved_{page}_{i}_{book_id}",
                                disabled=True,
                                use_container_width=True
                            )

                            if st.button(
                                "즐겨찾기에서 삭제",
                                key=f"remove_{page}_{i}_{book_id}",
                                use_container_width=True
                            ):
                                del st.session_state.favorites[book_id]
                                st.rerun()

                        else:
                            if st.button(
                                "♡ 즐겨찾기 추가",
                                key=f"add_{page}_{i}_{book_id}",
                                use_container_width=True
                            ):
                                st.session_state.favorites[book_id] = book
                                st.rerun()

                st.divider()

                previous_col, next_col = st.columns(2)

                with previous_col:
                    if page > 1:
                        if st.button(
                            "← 이전 페이지",
                            use_container_width=True
                        ):
                            st.session_state.page -= 1
                            st.rerun()

                with next_col:
                    if page * 100 < total:
                        if st.button(
                            "다음 페이지 →",
                            use_container_width=True
                        ):
                            st.session_state.page += 1
                            st.rerun()

            else:
                st.info(
                    "검색 결과가 없습니다. "
                    "다른 제목이나 저자 이름을 입력해 보세요."
                )

        except requests.RequestException:
            st.error(
                "도서 정보를 불러오지 못했습니다. "
                "인터넷 연결을 확인한 뒤 다시 시도해 주세요."
            )

        except (ValueError, KeyError):
            st.error("도서 정보를 처리하지 못했습니다.")

    else:
        st.info("검색창에 책 제목이나 저자 이름을 입력해 주세요.")

# =====================================
# 탭 2: 즐겨찾기
# =====================================
with tab2:
    st.subheader("⭐ 나의 즐겨찾기")

    favorites = st.session_state.favorites

    if favorites:
        st.write(f"저장한 책: **{len(favorites)}권**")

        for book_id, book in list(favorites.items()):
            with st.container(border=True):
                st.markdown(f"### 📖 {book['제목']}")
                st.write(f"저자: {book['저자']}")
                st.write(f"출판 연도: {book['출판연도']}")

                if st.button(
                    "즐겨찾기에서 삭제",
                    key=f"delete_{book_id}",
                    use_container_width=True
                ):
                    del st.session_state.favorites[book_id]
                    st.rerun()

        st.divider()

        if st.button(
            "전체 삭제",
            use_container_width=True
        ):
            st.session_state.favorites = {}
            st.rerun()

    else:
        st.info(
            "저장한 책이 없습니다. "
            "도서 검색에서 원하는 책을 추가해 보세요."
        )

# =====================================
# 하단 안내
# =====================================
st.divider()
st.caption("도서 정보: Open Library")

st.caption(
    "※ 온라인 도서 검색 결과는 실제 학교 도서관의 "
    "소장 여부와 다를 수 있습니다."
)
