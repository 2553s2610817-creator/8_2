import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 & CSS 스타일링
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="희망 도서 책장 번호 찾기",
    page_icon="📚",
    layout="wide"
)

# 커스텀 스타일
st.markdown("""
<style>
    .main-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .shelf-badge {
        background-color: #EF4444;
        color: white;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 1.4rem;
        font-weight: bold;
        display: inline-block;
        margin-top: 5px;
        margin-bottom: 5px;
    }
    .info-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 기초 도서 데이터베이스 (샘플 데이터)
# -----------------------------------------------------------------------------
if 'book_db' not in st.session_state:
    st.session_state.book_db = pd.DataFrame([
        {"id": "BK001", "title": "Do it! 점프 투 파이썬", "author": "박응용", "call_number": "005.133 박68ㄷ2", "floor": "2층", "shelf_no": 3, "shelf_side": "A면", "shelf_row": "2단", "status": "대출가능"},
        {"id": "BK002", "title": "클린 코드 (Clean Code)", "author": "로버트 C. 마틴", "call_number": "005.133 마892ㅋ", "floor": "2층", "shelf_no": 3, "shelf_side": "B면", "shelf_row": "1단", "status": "대출가능"},
        {"id": "BK003", "title": "공정하다는 착각", "author": "마이클 샌델", "call_number": "301.1 샌32ㄱ", "floor": "3층", "shelf_no": 5, "shelf_side": "B면", "shelf_row": "3단", "status": "대출가능"},
        {"id": "BK004", "title": "트렌드 코리아 2026", "author": "김난도 외", "call_number": "322.09 김295트", "floor": "3층", "shelf_no": 6, "shelf_side": "A면", "shelf_row": "1단", "status": "대출가능"},
        {"id": "BK005", "title": "아몬드", "author": "손원평", "call_number": "813.7 손67아", "floor": "1층", "shelf_no": 1, "shelf_side": "B면", "shelf_row": "2단", "status": "대출가능"},
        {"id": "BK006", "title": "불편한 편의점", "author": "김호연", "call_number": "813.7 김75부", "floor": "1층", "shelf_no": 1, "shelf_side": "A면", "shelf_row": "3단", "status": "대출중"},
        {"id": "BK007", "title": "코스모스", "author": "칼 세이건", "call_number": "504 세67ㅋ", "floor": "2층", "shelf_no": 4, "shelf_side": "A면", "shelf_row": "5단", "status": "대출가능"},
        {"id": "BK008", "title": "사피엔스", "author": "유발 하라리", "call_number": "909 하94ㅅ", "floor": "3층", "shelf_no": 8, "shelf_side": "A면", "shelf_row": "2단", "status": "대출가능"},
    ])

# -----------------------------------------------------------------------------
# 3. 도서관 평면도 시각화 함수 (Plotly 사용)
# -----------------------------------------------------------------------------
def draw_shelf_map(floor_name, target_shelf_no):
    shelves = [
        {"no": 1, "x": 1, "y": 3}, {"no": 2, "x": 3, "y": 3},
        {"no": 3, "x": 5, "y": 3}, {"no": 4, "x": 7, "y": 3},
        {"no": 5, "x": 1, "y": 1}, {"no": 6, "x": 3, "y": 1},
        {"no": 7, "x": 5, "y": 1}, {"no": 8, "x": 7, "y": 1},
    ]

    fig = go.Figure()

    # 입구 표시
    fig.add_shape(type="rect", x0=0.2, y0=0.1, x1=1.8, y1=0.5, fillcolor="#E2E8F0", line=dict(color="#94A3B8"))
    fig.add_annotation(x=1, y=0.3, text="🚪 입구", showarrow=False, font=dict(size=11, color="#334155"))

    for s in shelves:
        is_target = (s["no"] == target_shelf_no)
        bg_color = "#EF4444" if is_target else "#CBD5E1"
        border_color = "#991B1B" if is_target else "#64748B"
        text_color = "#FFFFFF" if is_target else "#1E293B"

        fig.add_shape(
            type="rect",
            x0=s["x"] - 0.75, y0=s["y"] - 0.45,
            x1=s["x"] + 0.75, y1=s["y"] + 0.45,
            fillcolor=bg_color,
            line=dict(color=border_color, width=3 if is_target else 1)
        )

        label = f"<b>★ 책장 {s['no']:02d}번</b><br>(여기!)" if is_target else f"책장 {s['no']:02d}번"
        fig.add_annotation(
            x=s["x"], y=s["y"],
            text=label,
            showarrow=False,
            font=dict(size=13 if is_target else 11, color=text_color)
        )

    fig.update_xaxes(range=[0, 8.8], showgrid=False, zeroline=False, visible=False)
    fig.update_yaxes(range=[0, 3.8], showgrid=False, zeroline=False, visible=False)
    fig.update_layout(
        title=f"🏛️ [{floor_name}] 배치도 - 책장 {target_shelf_no:02d}번 위치 하이라이트",
        height=350,
        margin=dict(l=10, r=10, t=40, b=10),
        plot_bgcolor="#F8FAFC"
    )
    return fig

# -----------------------------------------------------------------------------
# 4. 앱 화면 구성을 위한 헤더 & 검색 기능
# -----------------------------------------------------------------------------
st.markdown('<div class="main-title">📚 도서관 희망 도서 위치 & 책장 번호 검색</div>', unsafe_allow_html=True)
st.write("도서관 내부에서 찾고자 하는 책을 검색하면 정확한 **위치(층)**와 **책장 번호**를 안내해 드립니다.")
st.markdown("---")

search_kw = st.text_input("🔍 도서명, 저자, 또는 청구기호를 입력하세요", placeholder="예: 파이썬, 사피엔스, 마이클 샌델")

if search_kw.strip():
    df = st.session_state.book_db
    filtered_df = df[
        df["title"].str.contains(search_kw, case=False, na=False) |
        df["author"].str.contains(search_kw, case=False, na=False) |
        df["call_number"].str.contains(search_kw, case=False, na=False)
    ]

    if not filtered_df.empty:
        st.success(f"총 {len(filtered_df)}건의 도서가 검색되었습니다.")
        
        selected_book_title = st.selectbox("목록에서 도서를 선택하세요:", filtered_df["title"].tolist())
        book = filtered_df[filtered_df["title"] == selected_book_title].iloc[0]

        st.markdown("<br>", unsafe_allow_html=True)
        col_info, col_map = st.columns([1, 1])

        with col_info:
            st.markdown("<div class='info-box'>", unsafe_allow_html=True)
            st.markdown(f"### 📖 {book['title']}")
            st.write(f"• **저자**: {book['author']}")
            st.write(f"• **청구기호**: `{book['call_number']}`")
            st.write(f"• **대출상태**: {'✅ 대출가능' if book['status'] == '대출가능' else '❌ 대출중'}")
            st.markdown("---")
            st.markdown("#### 📍 도서 위치 정보")
            st.write(f"• **위치 층**: **{book['floor']}**")
            st.markdown(f"• **책장 번호**: <div class='shelf-badge'>책장 {book['shelf_no']:02d}번</div>", unsafe_allow_html=True)
            st.write(f"• **세부 위치**: **{book['shelf_side']}** / **{book['shelf_row']}**")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_map:
            fig = draw_shelf_map(book['floor'], book['shelf_no'])
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("검색 결과가 없습니다. 다른 검색어로 다시 검색해 주세요.")
else:
    st.info("💡 위 검색창에 원하시는 책 이름을 입력해 보세요.")
