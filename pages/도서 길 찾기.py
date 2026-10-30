
import streamlit as st
import plotly.graph_objects as go
import heapq
import math

st.set_page_config(page_title="도서관 길찾기", page_icon="📚", layout="wide")

# 도서 데이터
books = [
    ["불편한 편의점", "김호연", "문학", "A-01", True],
    ["아몬드", "손원평", "문학", "A-01", True],
    ["작별하지 않는다", "한강", "문학", "A-02", False],
    ["어린 왕자", "생텍쥐페리", "문학", "A-02", True],
    ["사피엔스", "유발 하라리", "사회과학", "B-01", True],
    ["총, 균, 쇠", "재레드 다이아몬드", "사회과학", "B-02", True],
    ["미움받을 용기", "기시미 이치로", "사회과학", "B-02", True],
    ["코스모스", "칼 세이건", "자연과학", "C-01", True],
    ["이기적 유전자", "리처드 도킨스", "자연과학", "C-02", False],
    ["파이썬 프로그래밍", "윤인성", "컴퓨터", "D-01", True],
    ["혼자 공부하는 머신러닝", "박해선", "컴퓨터", "D-02", True],
    ["달러구트 꿈 백화점", "이미예", "문학", "A-03", True],
    ["새로 들어온 책", "도서관 자료실", "신간", "N-01", True],
]

# 지도 위치
nodes = {
    "정문": (0, 2),
    "중앙통로": (3, 2),
    "왼쪽통로": (3, 5),
    "위쪽통로": (6, 5),
    "오른쪽통로": (9, 5),
    "오른쪽중앙": (9, 2),
    "아래통로": (6, 0),
    "안내데스크": (3, 0),
    "문학": (3, 6),
    "사회과학": (6, 6),
    "자연과학": (9, 6),
    "컴퓨터": (9, 0),
    "신간": (0, 5),
}

# 서가 좌표
shelves = {
    "A-01": ("문학", (2, 6)),
    "A-02": ("문학", (4, 6)),
    "A-03": ("문학", (3, 7)),
    "B-01": ("사회과학", (5, 6)),
    "B-02": ("사회과학", (7, 6)),
    "C-01": ("자연과학", (8, 7)),
    "C-02": ("자연과학", (10, 6)),
    "D-01": ("컴퓨터", (8, 0)),
    "D-02": ("컴퓨터", (10, 0)),
    "N-01": ("신간", (0, 6)),
}

# 서가 노드를 지도에 추가
for shelf, (room, position) in shelves.items():
    nodes["서가 " + shelf] = position

# 모든 통로 연결
edges = [
    ("정문", "중앙통로"),
    ("중앙통로", "왼쪽통로"),
    ("왼쪽통로", "위쪽통로"),
    ("위쪽통로", "오른쪽통로"),
    ("오른쪽통로", "오른쪽중앙"),
    ("중앙통로", "안내데스크"),
    ("안내데스크", "아래통로"),
    ("아래통로", "오른쪽중앙"),
    ("중앙통로", "위쪽통로"),
    ("위쪽통로", "아래통로"),
    ("왼쪽통로", "문학"),
    ("위쪽통로", "사회과학"),
    ("오른쪽통로", "자연과학"),
    ("오른쪽중앙", "컴퓨터"),
    ("왼쪽통로", "신간"),
]

for shelf, (room, position) in shelves.items():
    edges.append((room, "서가 " + shelf))

# 그래프 만들기
graph = {name: [] for name in nodes}

for a, b in edges:
    x1, y1 = nodes[a]
    x2, y2 = nodes[b]
    distance = math.hypot(x2 - x1, y2 - y1)
    graph[a].append((b, distance))
    graph[b].append((a, distance))

# 최단 경로 찾기
def find_path(start, end):
    distances = {n: float("inf") for n in graph}
    previous = {}
    distances[start] = 0
    queue = [(0, start)]

    while queue:
        dist, current = heapq.heappop(queue)

        if dist > distances[current]:
            continue

        if current == end:
            break

        for neighbor, weight in graph[current]:
            new_dist = dist + weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current
                heapq.heappush(queue, (new_dist, neighbor))

    if distances[end] == float("inf"):
        return None, 0

    path = [end]
    while path[-1] != start:
        path.append(previous[path[-1]])

    path.reverse()
    return path, distances[end]

# 지도 그리기
def draw_map(path, target, start):
    fig = go.Figure()

    # 통로
    for a, b in edges:
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]

        fig.add_trace(go.Scatter(
            x=[x1, x2],
            y=[y1, y2],
            mode="lines",
            line=dict(color="#CBD5E1", width=10),
            hoverinfo="skip",
            showlegend=False
        ))

    # 서가
    for shelf in shelves:
        x, y = nodes["서가 " + shelf]
        color = "#F97316" if shelf == target else "#64748B"

        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode="markers+text",
            marker=dict(
                size=22,
                color=color,
                symbol="square"
            ),
            text=[shelf],
            textposition="top center",
            showlegend=False
        ))

    # 이동 경로
    if path:
        xs = [nodes[n][0] for n in path]
        ys = [nodes[n][1] for n in path]

        fig.add_trace(go.Scatter(
            x=xs,
            y=ys,
            mode="lines+markers",
            line=dict(color="red", width=5, dash="dash"),
            marker=dict(size=9, color="red"),
            showlegend=False
        ))

    # 출발 위치
    x, y = nodes[start]

    fig.add_trace(go.Scatter(
        x=[x],
        y=[y],
        mode="markers+text",
        marker=dict(size=20, color="green", symbol="star"),
        text=["현재 위치"],
        textposition="bottom center",
        showlegend=False
    ))

    fig.update_layout(
        height=480,
        margin=dict(l=10, r=10, t=20, b=10),
        plot_bgcolor="#F8FAFC",
        xaxis=dict(visible=False, range=[-1, 12]),
        yaxis=dict(visible=False, range=[-1, 9], scaleanchor="x"),
        showlegend=False
    )

    return fig

# 화면
st.title("📚 학생 도서관 길찾기")
st.write("찾고 싶은 책을 검색하면 서가까지 이동 경로를 안내합니다.")

with st.sidebar:
    st.header("🔎 도서 검색")

    keyword = st.text_input("책 제목 또는 저자")

    categories = ["전체"] + sorted(set(b[2] for b in books))
    category = st.selectbox("도서 분류", categories)

    only_available = st.checkbox("대출 가능한 책만 보기")

    st.divider()
    st.header("📍 현재 위치")

    start = st.selectbox(
        "출발 장소",
        ["정문", "안내데스크", "중앙통로", "왼쪽통로", "오른쪽중앙"]
    )

# 검색
results = []

for book in books:
    title, author, group, shelf, available = book

    text = (title + author + group + shelf).lower()

    if keyword.lower().strip() not in text:
        continue

    if category != "전체" and group != category:
        continue

    if only_available and not available:
        continue

    results.append(book)

# 통계
c1, c2, c3 = st.columns(3)
c1.metric("전체 도서", str(len(books)) + "권")
c2.metric("검색 결과", str(len(results)) + "권")
c3.metric("대출 가능", str(sum(1 for b in books if b[4])) + "권")

left, right = st.columns([1, 1.5])

with left:
    st.subheader("📖 검색 결과")

    selected = None

    if results:
        labels = [
            b[0] + " - " + b[1]
            for b in results
        ]

        choice = st.selectbox("책 선택", labels)
        selected = results[labels.index(choice)]

        st.markdown("### " + selected[0])
        st.write("저자:", selected[1])
        st.write("분류:", selected[2])
        st.write("서가 번호:", selected[3])

        if selected[4]:
            st.success("대출 가능 (예시 데이터)")
        else:
            st.warning("대출 중 (예시 데이터)")
    else:
        st.info("검색 결과가 없습니다.")

with right:
    st.subheader("🗺️ 이동 경로 안내")

    if selected:
        shelf = selected[3]
        target = "서가 " + shelf

        path, distance = find_path(start, target)

        if path:
            st.plotly_chart(
                draw_map(path, shelf, start),
                use_container_width=True,
                config={"displayModeBar": False}
            )

            st.metric("예상 이동 거리", f"{distance:.1f} 지도 단위")

            st.markdown("#### 🚶 이동 순서")

            for i, place in enumerate(path, 1):
                if i == 1:
                    st.write(f"{i}. 출발: {place}")
                elif i == len(path):
                    st.write(f"{i}. 도착: {place}")
                else:
                    st.write(f"{i}. {place} 방향으로 이동")

        else:
            st.error("경로를 찾을 수 없습니다.")
    else:
        st.info("왼쪽에서 책을 선택해 주세요.")

st.divider()
st.caption(
    "※ 도서와 서가 위치는 시연용 예시입니다. "
    "실제 도서관의 지도 및 도서 정보와 다를 수 있습니다."
)
