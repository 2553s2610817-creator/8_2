import io
import difflib

import pandas as pd
import streamlit as st

# ------------------------------------------------------------
# 기본 설정
# ------------------------------------------------------------
st.set_page_config(
    page_title="책 어디 있지? 도서관 위치 찾기",
    page_icon="📚",
    layout="wide",
)

REQUIRED_COLS = ["제목", "저자", "분류", "청구기호", "책장", "칸", "대출상태"]
COLS_PER_ROW = 6   # 지도에서 한 줄에 있는 책장 수
TOTAL_SHELVES = 24  # 책장 총 개수 (6 x 4)

# 책장 번호 -> 구역(분류)
ZONES = {
    "총류": [1],
    "철학": [2],
    "종교": [3],
    "사회과학": [4, 5, 6],
    "자연과학": [7, 8, 9],
    "기술과학": [10, 11, 12],
    "예술": [13, 14],
    "언어": [15, 16],
    "문학": [17, 18, 19, 20, 21, 22],
    "역사": [23, 24],
}
ZONE_COLORS = {
    "총류": "#E0E0E0",
    "철학": "#D1C4E9",
    "종교": "#F8BBD0",
    "사회과학": "#BBDEFB",
    "자연과학": "#C8E6C9",
    "기술과학": "#B2EBF2",
    "예술": "#FFE0B2",
    "언어": "#FFF9C4",
    "문학": "#FFCCBC",
    "역사": "#D7CCC8",
}
SHELF_ZONE = {}
for _zone, _shelves in ZONES.items():
    for _s in _shelves:
        SHELF_ZONE[_s] = _zone

# 예시 데이터 (실제 도서관 데이터가 아니라 연습용입니다)
SAMPLE_BOOKS = [
    ("점프 투 파이썬", "박응용", "총류", "005.13-박", 1, 1, "대출 가능"),
    ("클린 코드", "로버트 C. 마틴", "총류", "005.1-마", 1, 2, "대출 중"),
    ("미움받을 용기", "기시미 이치로", "철학", "181.7-기", 2, 1, "대출 가능"),
    ("정의란 무엇인가", "마이클 샌델", "철학", "190-샌", 2, 2, "대출 가능"),
    ("숫타니파타", "법정 옮김", "종교", "223.1-법", 3, 1, "대출 가능"),
    ("국부론", "애덤 스미스", "사회과학", "320.9-스", 4, 1, "대출 가능"),
    ("21세기 자본", "토마 피케티", "사회과학", "320.1-피", 4, 2, "대출 중"),
    ("경제학 콘서트", "팀 하포드", "사회과학", "320-하", 4, 3, "대출 가능"),
    ("공정하다는 착각", "마이클 샌델", "사회과학", "340-샌", 5, 1, "대출 가능"),
    ("페다고지", "파울로 프레이리", "사회과학", "370-프", 6, 1, "대출 가능"),
    ("수학의 정석", "홍성대", "자연과학", "410-홍", 7, 1, "대출 가능"),
    ("시간의 역사", "스티븐 호킹", "자연과학", "429-호", 7, 2, "대출 가능"),
    ("이기적 유전자", "리처드 도킨스", "자연과학", "470-도", 8, 1, "대출 가능"),
    ("종의 기원", "찰스 다윈", "자연과학", "470-다", 8, 2, "대출 중"),
    ("코스모스", "칼 세이건", "자연과학", "440-세", 9, 1, "대출 가능"),
    ("내 몸 사용설명서", "마이클 로이젠", "기술과학", "510-로", 10, 1, "대출 가능"),
    ("전자회로 입문 (예시)", "예시 저자", "기술과학", "560-예", 11, 1, "대출 가능"),
    ("집밥 레시피 100선 (예시)", "예시 저자", "기술과학", "594-예", 12, 1, "대출 가능"),
    ("서양미술사", "에른스트 곰브리치", "예술", "609-곰", 13, 1, "대출 가능"),
    ("음악의 즐거움 (예시)", "예시 저자", "예술", "670-예", 13, 2, "대출 가능"),
    ("스포츠 과학 입문 (예시)", "예시 저자", "예술", "690-예", 14, 1, "대출 가능"),
    ("한국어 맞춤법 길라잡이 (예시)", "예시 저자", "언어", "710-예", 15, 1, "대출 가능"),
    ("영어 회화 필수 표현 (예시)", "예시 저자", "언어", "740-예", 16, 1, "대출 가능"),
    ("채식주의자", "한강", "문학", "813.7-한", 17, 1, "대출 가능"),
    ("소년이 온다", "한강", "문학", "813.7-한", 17, 2, "대출 중"),
    ("아몬드", "손원평", "문학", "813.7-손", 18, 1, "대출 가능"),
    ("불편한 편의점", "김호연", "문학", "813.7-김", 18, 2, "대출 가능"),
    ("82년생 김지영", "조남주", "문학", "813.7-조", 18, 3, "대출 중"),
    ("무소유", "법정", "문학", "818-법", 19, 1, "대출 가능"),
    ("하늘과 바람과 별과 시", "윤동주", "문학", "811.6-윤", 19, 2, "대출 가능"),
    ("상실의 시대", "무라카미 하루키", "문학", "833.6-무", 20, 1, "대출 가능"),
    ("인간 실격", "다자이 오사무", "문학", "833.6-다", 20, 2, "대출 가능"),
    ("해리 포터와 마법사의 돌", "J.K. 롤링", "문학", "843-롤", 21, 1, "대출 가능"),
    ("1984", "조지 오웰", "문학", "843-오", 21, 2, "대출 가능"),
    ("위대한 개츠비", "F. 스콧 피츠제럴드", "문학", "843-피", 21, 3, "대출 중"),
    ("어린 왕자", "생텍쥐페리", "문학", "863-생", 22, 1, "대출 가능"),
    ("데미안", "헤르만 헤세", "문학", "853-헤", 22, 2, "대출 가능"),
    ("사피엔스", "유발 하라리", "역사", "909-하", 23, 1, "대출 가능"),
    ("총, 균, 쇠", "재레드 다이아몬드", "역사", "909-다", 23, 2, "대출 중"),
    ("먼나라 이웃나라", "이원복", "역사", "909-이", 23, 3, "대출 가능"),
    ("난중일기", "이순신", "역사", "911-이", 24, 1, "대출 가능"),
    ("한국사 편지", "박은봉", "역사", "911-박", 24, 2, "대출 가능"),
]


# ------------------------------------------------------------
# 데이터 처리 함수
# ------------------------------------------------------------
def clean_df(df):
    """CSV/예시 데이터를 앱에서 쓸 수 있는 형태로 정리합니다."""
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError("필요한 열이 없어요: " + ", ".join(missing))

    df = df[REQUIRED_COLS].copy()
    df = df.dropna(subset=["제목", "책장"])
    df["책장"] = pd.to_numeric(df["책장"], errors="coerce")
    df["칸"] = pd.to_numeric(df["칸"], errors="coerce").fillna(1)
    df = df.dropna(subset=["책장"])
    df = df[(df["책장"] >= 1) & (df["책장"] <= TOTAL_SHELVES)]
    df["책장"] = df["책장"].astype(int)
    df["칸"] = df["칸"].astype(int)

    for col in ["제목", "저자", "분류", "청구기호", "대출상태"]:
        df[col] = df[col].fillna("").astype(str).str.strip()
    df["대출상태"] = df["대출상태"].replace("", "대출 가능")

    df = df.reset_index(drop=True)
    if df.empty:
        raise ValueError("사용할 수 있는 책 정보가 없어요. (책장은 1~24 숫자여야 해요)")
    return df


def read_uploaded_csv(file):
    """업로드된 CSV를 읽습니다. (UTF-8, 엑셀 CP949 모두 지원)"""
    raw = file.getvalue()
    for enc in ("utf-8-sig", "cp949"):
        try:
            return pd.read_csv(io.BytesIO(raw), encoding=enc)
        except UnicodeDecodeError:
            continue
    raise ValueError("파일 인코딩을 읽을 수 없어요. CSV를 UTF-8로 저장해 주세요.")


def normalize(text):
    return str(text).lower().replace(" ", "")


def esc(text):
    """마크다운에서 달러 기호가 수식으로 바뀌는 것을 방지합니다."""
    return str(text).replace("$", "\\$")


def search_books(df, query, category, only_available):
    result = df
    if category != "전체":
        result = result[result["분류"] == category]
    if only_available:
        result = result[result["대출상태"] == "대출 가능"]

    tokens = [normalize(t) for t in query.split() if t.strip()]
    if tokens and not result.empty:
        blob = (
            result["제목"] + " " + result["저자"] + " "
            + result["분류"] + " " + result["청구기호"]
        ).map(normalize)
        mask = pd.Series(True, index=result.index)
        for t in tokens:
            mask &= blob.str.contains(t, regex=False)
        result = result[mask]
    return result


# ------------------------------------------------------------
# 지도 그리기 (HTML/CSS)
# ------------------------------------------------------------
MAP_CSS = (
    "<style>"
    ".lib-door{background:#37474F;color:#fff;text-align:center;padding:8px;"
    "border-radius:8px;margin-bottom:10px;font-weight:600;}"
    ".lib-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:8px;}"
    ".lib-shelf{position:relative;border-radius:10px;padding:12px 2px;"
    "text-align:center;color:#222;border:3px solid transparent;min-height:72px;}"
    ".lib-num{font-size:1.25rem;font-weight:800;}"
    ".lib-zn{font-size:.72rem;}"
    ".lib-hit{border:3px solid #E53935;animation:libpulse 1.4s infinite;}"
    ".lib-badge{position:absolute;top:-10px;right:-6px;background:#E53935;"
    "color:#fff;border-radius:50%;min-width:24px;height:24px;line-height:24px;"
    "font-size:.8rem;font-weight:700;}"
    ".lib-legend{display:flex;flex-wrap:wrap;gap:6px;margin-top:12px;}"
    ".lib-chip{padding:3px 10px;border-radius:12px;color:#222;font-size:.78rem;}"
    "@keyframes libpulse{0%{box-shadow:0 0 0 0 rgba(229,57,53,.7);}"
    "70%{box-shadow:0 0 0 12px rgba(229,57,53,0);}"
    "100%{box-shadow:0 0 0 0 rgba(229,57,53,0);}}"
    "</style>"
)


def render_map(highlight=None):
    """highlight: {책장번호: 표시할 글자}"""
    highlight = highlight or {}
    cells = []
    for n in range(1, TOTAL_SHELVES + 1):
        zone = SHELF_ZONE.get(n, "")
        color = ZONE_COLORS.get(zone, "#EEEEEE")
        css_class = "lib-shelf lib-hit" if n in highlight else "lib-shelf"
        badge = ""
        if n in highlight:
            badge = '<div class="lib-badge">' + str(highlight[n]) + "</div>"
        cells.append(
            '<div class="' + css_class + '" style="background:' + color + '">'
            '<div class="lib-num">' + str(n) + "</div>"
            '<div class="lib-zn">' + zone + "</div>" + badge + "</div>"
        )
    legend = "".join(
        '<span class="lib-chip" style="background:' + ZONE_COLORS[z] + '">'
        + z + " (" + str(v[0]) + "~" + str(v[-1]) + "번)</span>"
        for z, v in ZONES.items()
    )
    return (
        MAP_CSS
        + '<div class="lib-door">🚪 출입구 · 대출 데스크</div>'
        + '<div class="lib-grid">' + "".join(cells) + "</div>"
        + '<div class="lib-legend">' + legend + "</div>"
    )


def location_text(shelf, kan):
    row = (shelf - 1) // COLS_PER_ROW + 1
    col = (shelf - 1) % COLS_PER_ROW + 1
    zone = SHELF_ZONE.get(shelf, "")
    return (
        f"📍 **{shelf}번 책장** ({zone} 구역) · 위에서 **{kan}번째 칸**  \n"
        f"🚶 출입구에서 들어가 **{row}번째 줄, 왼쪽에서 {col}번째** 책장이에요."
    )


# ------------------------------------------------------------
# 상태 관리 (session_state)
# ------------------------------------------------------------
if "books" not in st.session_state:
    st.session_state.books = clean_df(pd.DataFrame(SAMPLE_BOOKS, columns=REQUIRED_COLS))
if "cart" not in st.session_state:
    st.session_state.cart = []


def add_to_cart(book_id):
    if book_id not in st.session_state.cart:
        st.session_state.cart.append(book_id)


def remove_from_cart(book_id):
    if book_id in st.session_state.cart:
        st.session_state.cart.remove(book_id)


def clear_cart():
    st.session_state.cart = []


def show_book_card(book_id, row, key_prefix):
    shelf = int(row["책장"])
    kan = int(row["칸"])
    available = row["대출상태"] == "대출 가능"
    with st.container(border=True):
        c1, c2, c3 = st.columns([4, 2, 2])
        with c1:
            st.markdown(f"**📖 {esc(row['제목'])}**")
            st.caption(f"{esc(row['저자'])} · {esc(row['분류'])} · 청구기호 {esc(row['청구기호'])}")
        with c2:
            st.metric("책장 번호", f"{shelf}번")
        with c3:
            if available:
                st.success("✅ 대출 가능")
            else:
                st.error("❌ 대출 중")
        st.markdown(location_text(shelf, kan))
        in_cart = book_id in st.session_state.cart
        st.button(
            "✔ 내 동선에 담김" if in_cart else "➕ 내 동선에 담기",
            key=f"{key_prefix}_{book_id}",
            disabled=in_cart,
            on_click=add_to_cart,
            args=(book_id,),
        )


# ------------------------------------------------------------
# 화면
# ------------------------------------------------------------
st.title("📚 책 어디 있지?")
st.caption("도서관에서 헤매지 마세요! 책 이름만 입력하면 책장 번호를 알려드려요.")

df = st.session_state.books

tab_search, tab_map, tab_route, tab_data = st.tabs(
    ["🔎 책 찾기", "🗺️ 도서관 지도", "🧭 내 동선", "⚙️ 데이터 관리"]
)

# ---------------- 1) 책 찾기 ----------------
with tab_search:
    query = st.text_input(
        "찾고 싶은 책을 입력하세요",
        placeholder="예) 해리 포터 / 한강 / 사피엔스 / 813.7",
    )
    f1, f2 = st.columns(2)
    with f1:
        categories = ["전체"] + sorted(df["분류"].unique().tolist())
        category = st.selectbox("분류 선택", categories)
    with f2:
        only_available = st.checkbox("대출 가능한 책만 보기", value=False)

    if not query.strip() and category == "전체" and not only_available:
        st.info("👆 책 제목, 저자, 청구기호 중 하나를 입력해 보세요. 분류만 골라서 둘러볼 수도 있어요.")
    else:
        try:
            result = search_books(df, query, category, only_available)
        except Exception as e:
            result = df.iloc[0:0]
            st.error(f"검색 중 문제가 생겼어요: {e}")

        if result.empty:
            st.warning("검색 결과가 없어요 😢")
            if query.strip():
                titles = df["제목"].tolist()
                similar = difflib.get_close_matches(query.strip(), titles, n=3, cutoff=0.3)
                if similar:
                    st.write("혹시 이 책을 찾으셨나요? → " + " / ".join(similar))
                st.caption("팁: 띄어쓰기를 줄이거나 저자 이름으로 검색해 보세요.")
        else:
            shown = result.head(20)
            st.success(f"총 {len(result)}권을 찾았어요!" + (" (상위 20권만 표시)" if len(result) > 20 else ""))
            highlight = {}
            for book_id, row in shown.iterrows():
                show_book_card(book_id, row, "s")
                highlight[int(row["책장"])] = "📍"
            st.subheader("🗺️ 지도에서 위치 보기")
            st.markdown(render_map(highlight), unsafe_allow_html=True)

# ---------------- 2) 도서관 지도 ----------------
with tab_map:
    st.subheader("도서관 전체 배치도")
    shelf_no = st.selectbox(
        "책장 번호를 고르면 꽂혀 있는 책을 볼 수 있어요",
        list(range(1, TOTAL_SHELVES + 1)),
        format_func=lambda n: f"{n}번 책장 ({SHELF_ZONE.get(n, '')})",
    )
    st.markdown(render_map({shelf_no: "📍"}), unsafe_allow_html=True)
    on_shelf = df[df["책장"] == shelf_no].sort_values("칸")
    st.markdown(f"#### {shelf_no}번 책장에 있는 책 ({len(on_shelf)}권)")
    if on_shelf.empty:
        st.info("이 책장에 등록된 책이 없어요.")
    else:
        st.dataframe(
            on_shelf[["칸", "제목", "저자", "청구기호", "대출상태"]],
            hide_index=True,
        )

# ---------------- 3) 내 동선 ----------------
with tab_route:
    st.subheader("내 대출 동선")
    st.caption("'책 찾기'에서 담은 책들을 책장 번호 순서로 정리해, 가장 덜 걷는 순서를 알려드려요.")
    cart_ids = [i for i in st.session_state.cart if i in df.index]
    if not cart_ids:
        st.info("아직 담은 책이 없어요. '책 찾기'에서 ➕ 버튼을 눌러 담아보세요.")
    else:
        cart_df = df.loc[cart_ids].sort_values(["책장", "칸"])
        shelf_order = {}
        for s in cart_df["책장"].tolist():
            if s not in shelf_order:
                shelf_order[s] = len(shelf_order) + 1

        route_text = "🚪 출입구 → " + " → ".join(f"{s}번 책장" for s in shelf_order)
        st.markdown(f"### {route_text}")

        for book_id, row in cart_df.iterrows():
            with st.container(border=True):
                a, b = st.columns([5, 1])
                with a:
                    status = "✅" if row["대출상태"] == "대출 가능" else "❌ 대출 중"
                    st.markdown(
                        f"**{shelf_order[int(row['책장'])]}번째 방문** · {int(row['책장'])}번 책장 "
                        f"{int(row['칸'])}번째 칸 · 📖 {esc(row['제목'])} {status}"
                    )
                with b:
                    st.button(
                        "삭제",
                        key=f"rm_{book_id}",
                        on_click=remove_from_cart,
                        args=(book_id,),
                    )

        st.markdown(render_map(shelf_order), unsafe_allow_html=True)
        st.caption("지도의 빨간 숫자는 방문 순서예요.")
        st.button("🗑️ 모두 비우기", on_click=clear_cart)

# ---------------- 4) 데이터 관리 ----------------
with tab_data:
    st.subheader("우리 도서관 데이터로 바꾸기")
    st.write(
        "CSV 파일에 아래 7개 열이 있어야 해요: **제목, 저자, 분류, 청구기호, 책장(1~24), 칸, 대출상태**"
    )
    template = pd.DataFrame(SAMPLE_BOOKS, columns=REQUIRED_COLS).to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 CSV 양식(예시 데이터) 내려받기",
        data=template,
        file_name="books_template.csv",
        mime="text/csv",
    )

    uploaded = st.file_uploader("CSV 파일 올리기", type=["csv"])
    if uploaded is not None:
        if st.button("✅ 이 파일로 적용하기"):
            try:
                new_df = clean_df(read_uploaded_csv(uploaded))
                st.session_state.books = new_df
                st.session_state.cart = []
                st.success(f"{len(new_df)}권의 책 정보를 불러왔어요!")
                st.rerun()
            except Exception as e:
                st.error(f"파일을 적용할 수 없어요: {e}")

    if st.button("↩️ 예시 데이터로 되돌리기"):
        st.session_state.books = clean_df(pd.DataFrame(SAMPLE_BOOKS, columns=REQUIRED_COLS))
        st.session_state.cart = []
        st.rerun()

    st.markdown(f"#### 현재 등록된 책 ({len(df)}권)")
    st.dataframe(df, hide_index=True)
