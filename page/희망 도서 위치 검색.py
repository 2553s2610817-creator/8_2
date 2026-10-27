import html

import streamlit as st

st.set_page_config(page_title="희망 도서 위치 찾기", page_icon="📖", layout="centered")

# ------------------------------------------------------------------
# 1. 데이터 (도서 목록 / 책장 정보) - 필요하면 여기에 책을 추가하세요
# ------------------------------------------------------------------
SHELF_GRID = [
    ["A-10", "A-11", "A-12", "A-13"],  # 안쪽 줄 (위)
    ["A-14", "A-15", "A-16", "A-17"],  # 입구 쪽 줄 (아래)
]

SHELF_TOPIC = {
    "A-10": "한국 문학",
    "A-11": "한국 소설",
    "A-12": "세계 문학 (독일·미국)",
    "A-13": "세계 문학 (프랑스·미국)",
    "A-14": "인문·역사",
    "A-15": "과학",
    "A-16": "사회·경제",
    "A-17": "컴퓨터·IT",
}

BOOKS = [
    {"title": "데미안", "author": "헤르만 헤세", "publisher": "민음사", "year": 2012, "shelf": "A-12", "color": "#1F2A4D", "available": True},
    {"title": "호밀밭의 파수꾼", "author": "J.D. 샐린저", "publisher": "민음사", "year": 2001, "shelf": "A-12", "color": "#B5533C", "available": True},
    {"title": "어린 왕자", "author": "생텍쥐페리", "publisher": "열린책들", "year": 2015, "shelf": "A-10", "color": "#3C7A89", "available": True},
    {"title": "채식주의자", "author": "한강", "publisher": "창비", "year": 2007, "shelf": "A-10", "color": "#5B7F3A", "available": False},
    {"title": "나미야 잡화점의 기적", "author": "히가시노 게이고", "publisher": "현대문학", "year": 2012, "shelf": "A-11", "color": "#C28E2B", "available": True},
    {"title": "아몬드", "author": "손원평", "publisher": "창비", "year": 2017, "shelf": "A-11", "color": "#8C5A7A", "available": True},
    {"title": "불편한 편의점", "author": "김호연", "publisher": "나무옆의자", "year": 2021, "shelf": "A-11", "color": "#2F6F8F", "available": True},
    {"title": "이방인", "author": "알베르 카뮈", "publisher": "민음사", "year": 2019, "shelf": "A-13", "color": "#6B6B6B", "available": True},
    {"title": "위대한 개츠비", "author": "F. 스콧 피츠제럴드", "publisher": "민음사", "year": 2012, "shelf": "A-13", "color": "#0F5C5C", "available": True},
    {"title": "사피엔스", "author": "유발 하라리", "publisher": "김영사", "year": 2015, "shelf": "A-14", "color": "#9A4B2E", "available": True},
    {"title": "총, 균, 쇠", "author": "재레드 다이아몬드", "publisher": "문학사상", "year": 2005, "shelf": "A-14", "color": "#4A5D23", "available": False},
    {"title": "코스모스", "author": "칼 세이건", "publisher": "사이언스북스", "year": 2006, "shelf": "A-15", "color": "#1B1F5E", "available": True},
    {"title": "이기적 유전자", "author": "리처드 도킨스", "publisher": "을유문화사", "year": 2018, "shelf": "A-15", "color": "#7A3E65", "available": True},
    {"title": "정의란 무엇인가", "author": "마이클 샌델", "publisher": "김영사", "year": 2014, "shelf": "A-16", "color": "#A33B3B", "available": True},
    {"title": "넛지", "author": "리처드 탈러", "publisher": "리더스북", "year": 2009, "shelf": "A-16", "color": "#2E7D6B", "available": True},
    {"title": "클린 코드", "author": "로버트 C. 마틴", "publisher": "인사이트", "year": 2013, "shelf": "A-17", "color": "#333D4B", "available": True},
    {"title": "점프 투 파이썬", "author": "박응용", "publisher": "이지스퍼블리싱", "year": 2019, "shelf": "A-17", "color": "#2D6CA2", "available": True},
]

QUICK_PICKS = ["데미안", "사피엔스", "클린 코드", "어린 왕자"]

# ------------------------------------------------------------------
# 2. 스타일 (이미지처럼 네이비 + 연한 파랑 모바일 카드 디자인)
# ------------------------------------------------------------------
CSS = """
<style>
.stApp { background: #E9F0F8; }
.block-container { max-width: 460px; padding-top: 1.2rem; padding-bottom: 2rem; }
footer { visibility: hidden; }
.app-top { background: linear-gradient(135deg, #DDE9F6, #F4F8FC); border: 2px solid #34476B;
  border-radius: 18px; padding: 16px 18px; margin-bottom: 14px; }
.app-top .t { font-size: 1.25rem; font-weight: 800; color: #1F2D4D; }
.app-top .s { font-size: 0.85rem; color: #4A5C7C; margin-top: 2px; }
.page-title { text-align: center; font-weight: 800; color: #1F2D4D; font-size: 1.05rem; margin: 6px 0 10px 0; }
.step-badge { display: inline-block; background: #34476B; color: #fff; border-radius: 999px;
  padding: 2px 12px; font-size: 0.78rem; font-weight: 700; margin-bottom: 6px; }
.card { background: #fff; border: 1px solid #C9D6E8; border-radius: 14px; padding: 14px; margin-bottom: 8px; }
.book-row { display: flex; gap: 14px; align-items: center; }
.cover { width: 62px; min-width: 62px; height: 88px; border-radius: 5px; color: #fff; font-weight: 700;
  font-size: 0.72rem; display: flex; align-items: center; justify-content: center; text-align: center;
  padding: 4px; line-height: 1.2; box-shadow: 2px 3px 6px rgba(0,0,0,0.25); word-break: keep-all; }
.b-title { font-size: 1.15rem; font-weight: 800; color: #1F2D4D; }
.b-author { color: #5A6B88; font-size: 0.88rem; margin-bottom: 4px; }
.b-meta { font-size: 0.8rem; color: #5A6B88; }
.ok { color: #2E7D32; font-weight: 700; }
.no { color: #C62828; font-weight: 700; }
.shelf-box { display: flex; align-items: center; justify-content: space-between; background: #EEF3FA;
  border-radius: 10px; padding: 10px 14px; margin-top: 12px; }
.shelf-box .l { color: #34476B; font-weight: 700; font-size: 0.9rem; }
.shelf-box .v { background: #DCE7F6; color: #1F2D4D; font-weight: 800; border-radius: 8px; padding: 3px 14px; }
.map-title { font-weight: 800; color: #1F2D4D; margin: 12px 0 6px 0; }
.map-wrap { display: flex; gap: 6px; background: #fff; border: 1px solid #C9D6E8; border-radius: 12px; padding: 10px; }
.side { width: 12px; background: #D3DFEE; border-radius: 4px; }
.grid { flex: 1; display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
.cell { background: #E8EEF7; border: 1px solid #B9C8DE; border-radius: 6px; text-align: center;
  padding: 14px 0; font-size: 0.8rem; color: #34476B; font-weight: 600; position: relative; }
.cell.target { background: #EF8A84; border: 2px solid #C94B43; color: #fff; font-weight: 800; }
.cell .pin { position: absolute; top: -13px; left: 50%; transform: translateX(-50%); font-size: 1.2rem; }
.entrance { text-align: center; color: #5A6B88; font-size: 0.8rem; margin-top: 8px; }
.compass { float: right; font-size: 0.75rem; color: #34476B; font-weight: 700; }
.where-box { background: #fff; border: 1px solid #C9D6E8; border-radius: 12px; padding: 12px 14px; margin-top: 10px; }
.where-box .big { font-size: 1.05rem; font-weight: 800; color: #1F2D4D; }
.where-box .sm { font-size: 0.85rem; color: #5A6B88; margin-top: 2px; }
.steps { margin: 8px 0 0 0; padding-left: 18px; color: #34476B; font-size: 0.88rem; }
div.stButton > button, div[data-testid="stFormSubmitButton"] > button {
  width: 100%; background: #4C6A9C; color: #fff; border: none; border-radius: 10px;
  font-weight: 700; padding: 0.55rem 0; }
div.stButton > button:hover, div[data-testid="stFormSubmitButton"] > button:hover { background: #34476B; color: #fff; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------------------------
# 3. 상태 관리 (화면 전환)
# ------------------------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "search"
if "query" not in st.session_state:
    st.session_state.query = ""
if "selected" not in st.session_state:
    st.session_state.selected = None
if "notice" not in st.session_state:
    st.session_state.notice = ""


def esc(text):
    return html.escape(str(text))


def search_books(query):
    """제목/저자에서 공백 무시, 대소문자 무시로 검색"""
    try:
        q = query.replace(" ", "").lower()
        if not q:
            return []
        found = []
        for b in BOOKS:
            title = b["title"].replace(" ", "").lower()
            author = b["author"].replace(" ", "").lower()
            if q in title or q in author:
                found.append(b)
        return found
    except Exception:
        return []


def do_search(query):
    query = (query or "").strip()
    if not query:
        st.session_state.notice = "책 제목을 입력해 주세요."
        st.session_state.page = "search"
        return
    st.session_state.notice = ""
    st.session_state.query = query
    st.session_state.page = "results"


def quick_search(title):
    st.session_state["query_input"] = title
    do_search(title)


def go_location(index):
    st.session_state.selected = index
    st.session_state.page = "location"


def go_page(name):
    st.session_state.page = name
    if name == "search":
        st.session_state.notice = ""


def cover_html(book):
    return '<div class="cover" style="background:%s">%s</div>' % (esc(book["color"]), esc(book["title"]))


def status_html(book):
    if book["available"]:
        return '<span class="ok">● 대출 가능</span>'
    return '<span class="no">● 대출 중</span>'


def shelf_position(code):
    for r, row in enumerate(SHELF_GRID):
        if code in row:
            return r, row.index(code)
    return None, None


def directions(code):
    r, c = shelf_position(code)
    if r is None:
        return ["사서에게 문의해 주세요."]
    line = "입구 쪽 앞줄(아래쪽 줄)" if r == 1 else "안쪽 줄(위쪽 줄)"
    return [
        "출입구로 들어와 정면으로 이동합니다.",
        "%s로 가세요." % line,
        "왼쪽에서 %d번째 책장 %s을(를) 찾으세요." % (c + 1, code),
    ]


def map_html(target):
    cells = ""
    for row in SHELF_GRID:
        for code in row:
            if code == target:
                cells += '<div class="cell target"><span class="pin">📍</span>%s</div>' % esc(code)
            else:
                cells += '<div class="cell">%s</div>' % esc(code)
    return (
        '<div class="map-wrap"><div class="side"></div>'
        '<div class="grid">' + cells + "</div>"
        '<div class="side"></div></div>'
        '<div class="entrance">▲ 출입구 <span class="compass">N ↑</span></div>'
    )


# ------------------------------------------------------------------
# 4. 화면 ① 도서 검색
# ------------------------------------------------------------------
def page_search():
    st.markdown(
        '<div class="app-top"><div class="t">📖 희망 도서 위치 검색</div>'
        '<div class="s">원하는 책을 더 쉽게 찾아보세요!</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="page-title">찾고 싶은 책의 제목을 입력하세요.</div>', unsafe_allow_html=True)

    with st.form("search_form"):
        q = st.text_input(
            "책 제목",
            key="query_input",
            placeholder="책 제목을 입력하세요. (예: 데미안)",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("🔍 도서 검색")
    if submitted:
        do_search(q)
        st.rerun()

    if st.session_state.notice:
        st.warning(st.session_state.notice)

    st.caption("추천 검색어")
    cols = st.columns(2)
    for i, title in enumerate(QUICK_PICKS):
        with cols[i % 2]:
            st.button(title, key="quick_%d" % i, on_click=quick_search, args=(title,))

    st.info("책을 찾느라 헤매지 마세요. 책 제목(또는 저자)만 입력하면 책장 번호와 지도를 알려드려요.")


# ------------------------------------------------------------------
# 5. 화면 ② 검색 결과
# ------------------------------------------------------------------
def page_results():
    st.button("← 뒤로", key="back1", on_click=go_page, args=("search",))
    st.markdown('<div class="page-title">희망 도서 위치 검색</div>', unsafe_allow_html=True)
    st.markdown("🔎 **%s**" % esc(st.session_state.query))

    results = search_books(st.session_state.query)
    st.markdown("##### 검색 결과 %d건" % len(results))

    if not results:
        st.warning("검색 결과가 없습니다. 제목을 다시 확인하거나 저자 이름으로 검색해 보세요.")
        return

    for book in results:
        try:
            idx = BOOKS.index(book)
        except ValueError:
            continue
        st.markdown(
            '<div class="card"><div class="book-row">'
            + cover_html(book)
            + '<div><div class="b-title">%s</div><div class="b-author">%s</div>'
            '<div class="b-meta">출판사 &nbsp; %s<br>발행년도 &nbsp; %s<br>%s</div></div></div>'
            '<div class="shelf-box"><span class="l">📚 책장 번호</span><span class="v">%s</span></div></div>'
            % (esc(book["title"]), esc(book["author"]), esc(book["publisher"]), esc(book["year"]),
               status_html(book), esc(book["shelf"])),
            unsafe_allow_html=True,
        )
        st.button("📍 위치 확인", key="loc_%d" % idx, on_click=go_location, args=(idx,))


# ------------------------------------------------------------------
# 6. 화면 ③ 위치 안내
# ------------------------------------------------------------------
def page_location():
    idx = st.session_state.selected
    if idx is None or idx < 0 or idx >= len(BOOKS):
        st.warning("선택된 도서가 없습니다.")
        st.button("처음으로", key="home_err", on_click=go_page, args=("search",))
        return

    book = BOOKS[idx]
    code = book["shelf"]

    st.button("← 뒤로", key="back2", on_click=go_page, args=("results",))
    st.markdown('<div class="page-title">위치 안내</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="card"><div class="book-row">' + cover_html(book)
        + '<div><div class="b-title">%s</div><div class="b-author">%s</div><div class="b-meta">%s</div></div></div>'
        '<div class="shelf-box"><span class="l">📚 책장 번호</span><span class="v">%s</span></div></div>'
        % (esc(book["title"]), esc(book["author"]), status_html(book), esc(code)),
        unsafe_allow_html=True,
    )

    st.markdown('<div class="map-title">📍 도서관 내부 지도</div>', unsafe_allow_html=True)
    st.markdown(map_html(code), unsafe_allow_html=True)

    steps = "".join("<li>%s</li>" % esc(s) for s in directions(code))
    st.markdown(
        '<div class="where-box"><div class="big">📌 책장 번호 : %s</div>'
        '<div class="sm">지도에 표시된 책장으로 이동하세요. (분야: %s)</div>'
        '<ol class="steps">%s</ol></div>' % (esc(code), esc(SHELF_TOPIC.get(code, "-")), steps),
        unsafe_allow_html=True,
    )

    if not book["available"]:
        st.warning("이 책은 현재 대출 중이라 책장에 없을 수 있어요. 대출대에 문의해 보세요.")

    same = [b["title"] for b in BOOKS if b["shelf"] == code and b["title"] != book["title"]]
    if same:
        st.caption("같은 책장에 있는 다른 책: " + ", ".join(same))

    st.button("🔁 다른 책 찾기", key="home", on_click=go_page, args=("search",))


# ------------------------------------------------------------------
# 7. 실행
# ------------------------------------------------------------------
try:
    page = st.session_state.page
    if page == "results":
        page_results()
    elif page == "location":
        page_location()
    else:
        page_search()
except Exception as e:
    st.error("앱 실행 중 문제가 발생했습니다. 처음 화면으로 돌아가 주세요.")
    st.button("처음으로", key="home_fatal", on_click=go_page, args=("search",))
