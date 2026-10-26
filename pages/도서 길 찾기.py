
import heapq
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="도서 길찾기 맵",
    page_icon="📚",
    layout="wide"
)

# ---------------------------------------
# 예시 도서 데이터
# 실제 도서관에 맞게 수정할 수 있습니다.
# ---------------------------------------
BOOKS = [
    {"title": "불편한 편의점", "author": "김호연", "category": "문학", "shelf": "A-03", "available": True},
    {"title": "아몬드", "author": "손원평", "category": "문학", "shelf": "A-03", "available": True},
    {"title": "작별하지 않는다", "author": "한강", "category": "문학", "shelf": "A-04", "available": False},
    {"title": "사피엔스", "author": "유발 하라리", "category": "사회과학", "shelf": "B-02", "available": True},
    {"title": "총, 균, 쇠", "author": "재레드 다이아몬드", "category": "사회과학", "shelf": "B-03", "available": True},
    {"title": "코스모스", "author": "칼 세이건", "category": "자연과학", "shelf": "C-01", "available": True},
    {"title": "이기적 유전자", "author": "리처드 도킨스", "category": "자연과학", "shelf": "C-02", "available": False},
    {"title": "어린 왕자", "author": "생텍쥐페리", "category": "문학", "shelf": "A-02", "available": True},
    {"title": "파이썬 프로그래밍", "author": "윤인성", "category": "디지털자료실", "shelf": "D-01", "available": True},
    {"title": "달러구트 꿈 백화점", "author": "이미예", "category": "문학", "shelf": "A-05", "available": True},
    {"title": "미움받을 용기", "author": "기시미 이치로", "category": "사회과학", "shelf": "B-04", "available": True},
    {"title": "새로 들어온 책", "author": "도서관 자료실", "category": "신간도서", "shelf": "N-01", "available": True},
]

# ---------------------------------------
# 도서관 지도 노드와 통로
# 각 노드는 지도 위의 위치를 나타냅니다.
# ---------------------------------------
NODES = {
    "정문": (0, 4),
    "중앙통로": (3, 4),
    "중앙교차로": (6, 4),
    "오른쪽통로": (9, 4),
    "문학": (3, 7),
    "사회과학": (6, 7),
    "자연과학": (9, 7),
    "신간도서": (1, 6),
    "디지털자료실": (9, 1),
    "아래통로": (6, 1),
    "안내데스크": (3, 1),
    "어린이자료실": (11, 7),
}

EDGES = [
    ("정문", "중앙통로"),
    ("중앙통로", "중앙교차로"),
    ("중앙교차로", "오른쪽통로"),
    ("중앙통로", "문학"),
    ("중앙교차로", "사회과학"),
    ("오른쪽통로", "자연과학"),
    ("문학", "사회과학"),
    ("사회과학", "자연과학"),
    ("중앙통로", "안내데스크"),
    ("안내데스크", "아래통로"),
    ("아래통로", "중앙교차로"),
    ("아래통로", "디지털자료실"),
    ("자연과학", "어린이자료실"),
    ("중앙통로", "신간도서"),
]

# 서가별 지도 위치와 연결된 통로
SHELVES = {
    "A-02": ("문학", (2, 7)),
    "A-03": ("문학", (3, 6)),
    "A-04": ("문학", (4, 7)),
    "A-05": ("문학", (4, 6)),
    "B-02": ("사회과학", (6, 6)),
    "B-03": ("사회과학", (7, 7)),
    "B-04": ("사회과학", (7, 6)),
    "C-01": ("자연과학", (9, 6)),
    "C-02": ("자연과학", (10, 6)),
    "D-01": ("디지털자료실", (9, 2)),
    "N-01": ("신간도서", (1, 6)),
}

STARTS = {
    "정문(입구)": "정문",
    "안내데스크": "안내데스크",
    "중앙통로": "중앙통로",
}

GRAPH = {name: [] for name in NODES}

def add_edge(a, b):
    """양방향 통로를 그래프에 추가합니다."""
    x1, y1 = NODES[a]
    x2, y2 = NODES[b]
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    GRAPH[a].append((b, distance))
    GRAPH[b].append((a, distance))

for a, b in EDGES:
    add_edge(a, b)

# 서가 위치를 통로 네트워크에 연결
for shelf, (aisle, coords) in SHELVES.items():
    node = f"서가 {shelf}"
    NODES[node] = coords
    GRAPH[node] = []
    add_edge(aisle, node)

def shortest_path(start, end):
    """다익스트라 알고리즘으로 최단 경로를 찾습니다."""
    distances = {node: float("inf") for node in GRAPH}
    previous = {}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        distance, node = heapq.heappop(queue)

        if distance > distances[node]:
            continue

        if node == end:
            break

        for neighbor, weight in GRAPH[node]:
            new_distance = distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = node
                heapq.heappush(queue, (new_distance, neighbor))

    if distances[end] == float("inf"):
        return [], 0

    path = [end]
    while path[-1] != start:
        path.append(previous[path[-1]])

    path.reverse()
    return path, distances[end]

def draw_map(path, destination, start):
    """도서관의 개략적인 평면도와 이동 경로를 그립니다."""
    fig = go.Figure()

    # 통로
    for a, b in EDGES:
        x1, y1 = NODES[a]
        x2, y2 = NODES[b]

        fig.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode="lines",
            line=dict(color="#CBD5E1", width=10),
            hoverinfo="skip",
            showlegend=False,
        ))

    # 서가
    for shelf, (_, coords) in SHELVES.items():
        x, y = coords
        is_target = shelf == destination

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode="markers+text",
            marker=dict(
                size=24 if is_target else 17,
                color="#F97316" if is_target else "#64748B",
                symbol="square",
                line=dict(color="white", width=2),
            ),
            text=[shelf],
            textposition="top center",
            textfont=dict(color="#1E293B", size=11),
            showlegend=False,
            hovertemplate=f"서가 {shelf}<extra></extra>",
        ))

    # 경로
    if path:
        px = [NODES[node][0] for node in path]
        py = [NODES[node][1] for node in path]

        fig.add_trace(go.Scatter(
            x=px,
            y=py,
            mode="lines+markers",
            line=dict(color="#EF4444", width=5, dash="dash"),
            marker=dict(size=9, color="#EF4444"),
            name="이동 경로",
            hovertemplate="추천 경로<extra></extra>",
        ))

    # 출발 위치
    sx, sy = NODES[start]
    fig.add_trace(go.Scatter(
        x=[sx],
        y=[sy],
        mode="markers+text",
        marker=dict(size=19, color="#16A34A", symbol="star"),
        text=["현재 위치"],
        textposition="bottom center",
        showlegend=False,
    ))

    fig.update_layout(
        height=480,
        margin=dict(l=10, r=10, t=20, b=10),
        plot_bgcolor="#F8FAFC",
        paper_bgcolor="white",
        xaxis=dict(visible=False, range=[-1, 12]),
        yaxis=dict(visible=False, range=[0, 9], scaleanchor="x"),
        showlegend=False,
    )
    return fig

# ---------------------------------------
# 화면 디자인
# ---------------------------------------
st.markdown("""
<style>
.main .block-container {max-width: 1400px; padding-top: 1.5rem;}
.hero {
    background: linear-gradient(120deg, #153E68, #2877A8);
    padding: 25px;
    border-radius: 18px;
    color: white;
}
.hero h1 {color:white; margin:0;}
.hero p {color:#E0F2FE; margin:8px 0 0 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>📚 도서 길찾기 맵</h1>
<p>찾고 싶은 책을 선택하세요. 현재 위치에서 서가까지 가는 길을 안내합니다.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("🔍 책 검색")
    query = st.text_input("책 제목 또는 저자", placeholder="예: 아몬드")

    categories = ["전체"] + sorted(
        {book["category"] for book in BOOKS}
    )
    category = st.selectbox("자료 분류", categories)
    available_only = st.checkbox("대출 가능한 책만 보기")

    st.divider()
    st.header("📍 현재 위치")
    start_label = st.selectbox("출발 위치", list(STARTS.keys()))
    st.caption(
        "실내 GPS 위치는 자동으로 감지하지 않습니다. "
        "현재 위치와 가장 가까운 지점을 선택하세요."
    )

filtered = []

for book in BOOKS:
    text = (
        book["title"] + " " + book["author"] + " "
        + book["category"] + " " + book["shelf"]
    ).lower()

    if query.strip().lower() not in text:
        continue
    if category != "전체" and book["category"] != category:
        continue
    if available_only and not book["available"]:
        continue

    filtered.append(book)

m1, m2, m3 = st.columns(3)
m1.metric("등록 도서", f"{len(BOOKS)}권")
m2.metric("검색 결과", f"{len(filtered)}권")
m3.metric("대출 가능(예시)", f"{sum(b['available'] for b in BOOKS)}권")

left, right = st.columns([0.9, 1.3], gap="large")

with left:
    st.subheader("📖 검색 결과")

    selected = None

    if not filtered:
        st.warning("검색 결과가 없습니다. 다른 검색어를 입력해 보세요.")
    else:
        labels = [
            f"{b['title']} — {b['author']} "
            f"({'대출 가능' if b['available'] else '대출 중'})"
            for b in filtered
        ]

        label = st.selectbox("안내받을 책 선택", labels)
        selected = filtered[labels.index(label)]

        st.markdown(f"### {selected['title']}")
        st.write(f"**저자:** {selected['author']}")
        st.write(f"**분류:** {selected['category']}")
        st.write(f"**서가 번호:** `{selected['shelf']}`")

        if selected["available"]:
            st.success("🟢 대출 가능 (예시 데이터)")
        else:
            st.warning("🟠 대출 중 (예시 데이터)")

        st.info(
            f"목적지: {selected['category']} / "
            f"서가 {selected['shelf']}"
        )

with right:
    st.subheader("🗺️ 서가까지 이동 경로")

    if selected:
        shelf = selected["shelf"]

        if shelf not in SHELVES:
            st.error("이 책의 서가 위치가 지도에 등록되어 있지 않습니다.")
        else:
            start_node = STARTS[start_label]
            target_node = f"서가 {shelf}"

            path, distance = shortest_path(start_node, target_node)

            if path:
                st.plotly_chart(
                    draw_map(path, shelf, start_node),
                    use_container_width=True,
                    config={"displayModeBar": False},
                )

                c1, c2 = st.columns(2)
                c1.metric("이동 구간", f"{len(path) - 1}개")
                c2.metric("예상 거리", f"{distance * 4:.0f}m")

                st.markdown("#### 🚶 이동 순서")

                for i, node in enumerate(path, start=1):
                    if node == start_node:
                        description = f"출발: {start_label}"
                    elif node.startswith("서가 "):
                        description = f"도착: {node}"
                    else:
                        description = f"{node} 방향으로 이동"

                    st.write(f"**{i}.** {description}")

                st.caption(
                    "지도와 거리는 시연용 예시입니다. "
                    "실제 도서관 통로와 위치를 반영해 수정해야 합니다."
                )
            else:
                st.error("경로를 찾을 수 없습니다. 지도 연결 정보를 확인하세요.")
    else:
        st.info("왼쪽에서 책을 선택하면 이동 경로가 표시됩니다.")

st.divider()
st.subheader("📚 자료실 안내")

room_cols = st.columns(3)

rooms = [
    ("📕 문학", "소설, 시, 에세이"),
    ("🌐 사회과학", "역사, 사회, 경제"),
    ("🌿 자연과학", "과학, 수학"),
    ("🆕 신간도서", "새로 들어온 책"),
    ("💻 디지털자료실", "컴퓨터, 프로그래밍"),
]

for i, (name, description) in enumerate(rooms):
    with room_cols[i % 3]:
        st.markdown(f"**{name}**")
        st.caption(description)

st.caption(
    "학생용 도서관 길찾기 시연 앱입니다. "
    "도서 목록, 대출 상태, 서가 위치는 실제 도서관 데이터가 아닙니다."
)

