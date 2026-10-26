import difflib
import html

import streamlit as st

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(
    page_title="희망 도서 위치 검색",
    page_icon="📖",
    layout="centered",
)

MAP_COLS = 4   # 지도에서 한 줄에 있는 책장 수
MAP_ROWS = 5   # 지도의 줄 수 (4 x 5 = 20개 책장)
TOTAL_SHELVES = MAP_COLS * MAP_ROWS

# (제목, 저자, 출판사, 발행년도, 책장번호)  ※ 연습용 예시 데이터입니다.
BOOKS = [
    ("데미안", "헤르만 헤세", "민음사", 2012, 12),
    ("어린 왕자", "생텍쥐페리", "문학동네", 2015, 12),
    ("채식주의자", "한강", "창비", 2007, 14),
    ("소년이 온다", "한강", "창비", 2014, 14),
    ("아몬드", "손원평", "창비", 2017, 15),
    ("불편한 편의점", "김호연", "나무옆의자", 2021, 15),
    ("1984", "조지 오웰", "민음사", 2003, 16),
    ("해리 포터와 마법사의 돌", "J.K. 롤링", "문학수첩", 1999, 17),
    ("무소유", "법정", "범우사", 1999, 18),
    ("사피엔스", "유발 하라리", "김영사", 2015, 19),
    ("총, 균, 쇠", "재레드 다이아몬드", "문학사상", 2005, 19),
    ("난중일기", "이순신", "여해", 2019, 20),
    ("코스모스", "칼 세이건", "사이언스북스", 2006, 7),
    ("시간의 역사", "스티븐 호킹", "까치", 1998, 7),
    ("이기적 유전자", "리처드 도킨스", "을유문화사", 2018, 8),
    ("국부론", "애덤 스미스", "비봉출판사", 2007, 5),
    ("정의란 무엇인가", "마이클 샌델", "와이즈베리", 2014, 3),
    ("미움받을 용기", "기시미 이치로", "인플루엔셜", 2014, 3),
    ("점프 투 파이썬", "박응용", "이지스퍼블리싱", 2019, 1),
    ("클린 코드", "로버트 C. 마틴", "인사이트", 2013, 2),
]

COVER_GRADIENTS = [
    "linear-gradient(135deg,#A7C7E7 0%,#7DA0C4 100%)",
    "linear-gradient(135deg,#B8D8BA 0%,#7FAF86 100%)",
    "linear-gradient(135deg,#F2C6A0 0%,#D9976A 100%)",
    "linear-gradient(135deg,#C9B8E8 0%,#9A86C4 100%)",
    "linear-gradient(135deg,#F0B6BC 0%,#CF8590 100%)",
    "linear-gradient(135deg,#9FB6CD 0%,#5F7C99 100%)",
]

# ------------------------------------------------------------
# 스타일 (CSS)
# ------------------------------------------------------------
CSS = """
<style>
.block-container { max-width: 520px; padding-top: 1.5rem; padding-bottom: 3rem; }
header[data-testid="stHeader"] { background: transparent; }

.app-header { background: linear-gradient(135deg,#EAF2FB 0%,#D6E6F7 100%);
  border-radius: 16px; padding: 18px 18px; margin-bottom: 14px;
  display: flex; align-items: center; gap: 12px; }
.app-header .icon { font-size: 2.2rem; }
.app-header .t { font-size: 1.25rem; font-weight: 800; color: #2F4B6E; }
.app-header .s { font-size: .85rem; color: #5B7391; margin-top: 2px; }

.guide-text { text-align: center; font-weight: 800; font-size: 1.05rem;
  color: #2F4B6E; margin: 26px 0 10px 0; }
.bottom-note { text-align: center; color: #7A8CA3; font-size: .85rem;
  margin-top: 34px; line-height: 1.6; }
.bottom-note .big { font-size: 2.6rem; display: block; margin-bottom: 4px; }

.result-count { font-weight: 700; color: #2F4B6E; margin: 8px 0 8px 0; }

.book-row { display: flex; gap: 14px; align-items: flex-start; }
.cover { flex: 0 0 76px; height: 108px; border-radius: 6px 10px 10px 6px;
  display: flex; align-items: center; justify-content: center; text-align: center;
  color: #fff; font-weight: 800; font-size: .78rem; line-height: 1.3; padding: 6px;
  box-shadow: 3px 3px 8px rgba(0,0,0,.18); border-left: 5px solid rgba(0,0,0,.18);
  word-break: keep-all; }
.cover.small { flex: 0 0 60px; height: 86px; font-size: .66rem; }
.b-info { flex: 1; min-width: 0; }
.b-title { font-size: 1.15rem; font-weight: 800; color: #1F2D3D; }
.b-author { color: #5B6B7D; font-size: .9rem; margin-bottom: 6px; }
.b-meta { font-size: .82rem; color: #6B7B8C; display: flex; gap: 14px; }
.b-meta b { color: #2F3E50; margin-left: 4px; }

.shelf-row { display: flex; align-items: center; gap: 8px; background: #F1F5FA;
  border-radius: 10px; padding: 10px 12px; margin-top: 10px; color: #3C4F66;
  font-weight: 600; }
.chip { background: #DCE8F6; color: #2F4B6E; border-radius: 8px; padding: 3px 12px;
  font-weight: 800; font-size: 1.05rem; }

.section-title { font-weight: 800; color: #2F4B6E; margin: 16px 0 8px 0; }

.map-wrap { display: grid; grid-template-columns: 14px 1fr 14px; gap: 6px;
  background: #F7F9FC; border: 1px solid #D8E1EC; border-radius: 12px; padding: 12px 8px; }
.map-side { background: #DCE3EC; border-radius: 6px; }
.map-grid { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: 8px; }
.cell { position: relative; background: #E3EAF3; border: 1px solid #C9D5E3;
  border-radius: 6px; text-align: center; padding: 10px 0; font-size: .85rem;
  font-weight: 700; color: #50627A; }
.cell.hit { background: #F08A8A; border: 2px solid #D94F4F; color: #fff;
  box-shadow: 0 0 0 4px rgba(240,138,138,.35); }
.cell .pin { position: absolute; top: -16px; left: 50%; transform: translateX(-50%);
  font-size: 1.2rem; }
.map-foot { display: flex; justify-content: space-between; align-items: center;
  margin-top: 8px; color: #6B7B8C; font-size: .82rem; }
.entrance { background: #DCE3EC; border-radius: 8px; padding: 4px 16px; font-weight: 700; }
.compass { border: 1px solid #C9D5E3; border-radius: 50%; width: 34px; height: 34px;
  display: flex; align-items: center; justify-content: center; font-weight: 800;
  color: #2F4B6E; background: #fff; }

.where-box { border: 1px solid #D8E1EC; border-radius: 12px; padding: 12px 14px;
  margin-top: 12px; background: #fff; }
.where-box .w1 { font-weight: 800; color: #2F4B6E; font-size: 1.05rem; }
.where-box .w2 { color: #5B6B7D; font-size: .88rem; margin-top: 4px; line-height: 1.6; }

div.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button {
  background-color: #4A6C94; border-color: #4A6C94; color: #fff;
  border-radius: 10px; font-weight: 700; padding: .6rem 1rem; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ------------------------------------------------------------
# 도우미 함수
# ------------------------------------------------------------
def h(text):
    """HTML에 넣어도 안전하도록 글자를 변환합니다."""
    return html.escape(str(text))


def shelf_label(n):
    return "A-" + str(n)


def normalize(text):
    return str(text).lower().replace(" ", "")


def search_books(query):
    tokens = [normalize(t) for t in query.split() if t.strip()]
    if not tokens:
        return []
    found = []
    for idx, book in enumerate(BOOKS):
        blob = normalize(book[0] + " " + book[1])
        if all(t in blob for t in tokens):
            found.append(idx)
    return found


def cover_html(idx, small=False):
    title = BOOKS[idx][0]
    grad = COVER_GRADIENTS[idx % len(COVER_GRADIENTS)]
    cls = "cover small" if small else "cover"
    return '<div class="' + cls + '" style="background:' + grad + '">' + h(title) + "</div>"


def book_info_html(idx):
    title, author, publisher, year, _shelf = BOOKS[idx]
    return (
        '<div class="b-info">'
        '<div class="b-title">' + h(title) + "</div>"
        '<div class="b-author">' + h(author) + "</div>"
        '<div class="b-meta"><span>출판사<b>' + h(publisher) + "</b></span>"
        "<span>발행년도<b>" + h(year) + "</b></span></div>"
        "</div>"
    )


def render_header():
    st.markdown(
        '<div class="app-header"><div class="icon">📖</div><div>'
        '<div class="t">희망 도서 위치 검색</div>'
        '<div class="s">원하는 책을 더 쉽게 찾아보세요!</div>'
        "</div></div>",
        unsafe_allow_html=True,
    )


def render_map(target_shelf):
    cells = []
    for n in range(1, TOTAL_SHELVES + 1):
        if n == target_shelf:
            cells.append(
                '<div class="cell hit"><span class="pin">📍</span>' + shelf_label(n) + "</div>"
            )
        else:
            cells.append('<div class="cell">' + shelf_label(n) + "</div>")
    return (
        '<div class="map-wrap"><div class="map-side"></div>'
        '<div class="map-grid">' + "".join(cells) + "</div>"
        '<div class="map-side"></div></div>'
        '<div class="map-foot"><span></span>'
        '<span class="entrance">🚪 출입구</span>'
        '<span class="compass">N↑</span></div>'
    )


def walking_guide(shelf):
    row_from_top = (shelf - 1) // MAP_COLS          # 0부터 시작
    row_from_door = MAP_ROWS - row_from_top         # 출입구에서 몇 번째 줄인지
    col = (shelf - 1) % MAP_COLS + 1
    return (
        "출입구에서 들어와 앞으로 걸어서 <b>" + str(row_from_door) + "번째 줄</b>, "
        "왼쪽에서 <b>" + str(col) + "번째</b> 책장으로 이동하세요."
    )


# ------------------------------------------------------------
# 화면 이동 (session_state)
# ------------------------------------------------------------
if "screen" not in st.session_state:
    st.session_state.screen = "search"
if "query" not in st.session_state:
    st.session_state.query = ""
if "selected" not in st.session_state:
    st.session_state.selected = None


def go_search():
    st.session_state.screen = "search"
    st.session_state.selected = None


def go_result():
    st.session_state.screen = "result"
    st.session_state.selected = None


def go_map(idx):
    st.session_state.selected = idx
    st.session_state.screen = "map"


def search_form(key, default=""):
    """검색창 + 버튼 (엔터를 쳐도 검색돼요)"""
    with st.form(key, clear_on_submit=False):
        q = st.text_input(
            "책 제목",
            value=default,
            placeholder="🔍 책 제목을 입력하세요. (예: 데미안)",
            label_visibility="collapsed",
        )
        submitted = st.form_submit_button("🔍 도서 검색", use_container_width=True)
    if submitted:
        if not q.strip():
            st.warning("책 제목을 입력해 주세요.")
        else:
            st.session_state.query = q.strip()
            st.session_state.screen = "result"
            st.rerun()


# ------------------------------------------------------------
# 화면 ① 도서 검색
# ------------------------------------------------------------
def screen_search():
    render_header()
    st.markdown(
        '<div class="guide-text">찾고 싶은 책의 제목을 입력하세요.</div>',
        unsafe_allow_html=True,
    )
    search_form("form_search", st.session_state.query)
    st.markdown(
        '<div class="bottom-note"><span class="big">📖</span>'
        "책을 찾는 일이<br>조금 더 쉬워지도록,<br>도서관이 도와드릴게요.</div>",
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# 화면 ② 검색 결과
# ------------------------------------------------------------
def screen_result():
    st.button("← 뒤로", on_click=go_search, key="back_from_result")
    render_header()
    search_form("form_result", st.session_state.query)

    query = st.session_state.query
    try:
        found = search_books(query)
    except Exception as e:
        found = []
        st.error("검색 중 문제가 생겼어요: " + str(e))

    st.markdown(
        '<div class="result-count">검색 결과 ' + str(len(found)) + "건</div>",
        unsafe_allow_html=True,
    )

    if not found:
        st.warning("'" + query + "'에 해당하는 책을 찾지 못했어요 😢")
        titles = [b[0] for b in BOOKS]
        similar = difflib.get_close_matches(query, titles, n=3, cutoff=0.3)
        if similar:
            st.info("혹시 이 책인가요? → " + " / ".join(similar))
        st.caption("팁: 띄어쓰기를 줄이거나 저자 이름으로 검색해 보세요.")
        return

    for idx in found[:10]:
        shelf = BOOKS[idx][4]
        with st.container(border=True):
            st.markdown(
                '<div class="book-row">' + cover_html(idx) + book_info_html(idx) + "</div>"
                '<div class="shelf-row">📚 책장 번호 <span class="chip">'
                + shelf_label(shelf) + "</span></div>",
                unsafe_allow_html=True,
            )
            st.button(
                "📍 위치 확인",
                key="loc_" + str(idx),
                on_click=go_map,
                args=(idx,),
                type="primary",
                use_container_width=True,
            )
    if len(found) > 10:
        st.caption("결과가 많아 10권만 보여드려요. 더 자세히 검색해 보세요.")


# ------------------------------------------------------------
# 화면 ③ 위치 안내
# ------------------------------------------------------------
def screen_map():
    idx = st.session_state.selected
    if idx is None or idx < 0 or idx >= len(BOOKS):
        go_search()
        st.rerun()
        return

    st.button("← 뒤로", on_click=go_result, key="back_from_map")
    shelf = BOOKS[idx][4]

    with st.container(border=True):
        st.markdown(
            '<div class="book-row">' + cover_html(idx, small=True)
            + '<div class="b-info"><div class="b-title">' + h(BOOKS[idx][0]) + "</div>"
            '<div class="b-author">' + h(BOOKS[idx][1]) + "</div>"
            '<div class="shelf-row" style="margin-top:4px;">📚 책장 번호 '
            '<span class="chip">' + shelf_label(shelf) + "</span></div></div></div>",
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">📍 도서관 내부 지도</div>', unsafe_allow_html=True)
    st.markdown(render_map(shelf), unsafe_allow_html=True)

    st.markdown(
        '<div class="where-box"><div class="w1">📍 책장 번호 : ' + shelf_label(shelf) + "</div>"
        '<div class="w2">지도에 표시된 책장으로 이동하세요.<br>'
        + walking_guide(shelf) + "</div></div>",
        unsafe_allow_html=True,
    )

    st.write("")
    st.button(
        "🔍 다른 책 검색하기",
        on_click=go_search,
        key="new_search",
        type="primary",
        use_container_width=True,
    )


# ------------------------------------------------------------
# 실행
# ------------------------------------------------------------
try:
    if st.session_state.screen == "result":
        screen_result()
    elif st.session_state.screen == "map":
        screen_map()
    else:
        screen_search()
except Exception as e:
    st.error("앱에서 문제가 생겼어요. 새로고침 해주세요. (" + str(e) + ")")
