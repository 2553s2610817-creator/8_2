
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="공주님의 책장",
    page_icon="🎀",
    layout="centered"
)

# -------------------------
# 파스텔 핑크 디자인
# -------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fff2f8, #f9f3ff);
    color: #80516c;
}

header[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3 {
    color: #d96da0 !important;
    font-family: sans-serif;
}

p, label, div {
    font-family: sans-serif;
}

.princess-banner {
    background: linear-gradient(135deg, #ffcce3, #e8d8ff);
    padding: 30px 15px;
    border-radius: 25px;
    text-align: center;
    border: 2px solid #ffffff;
    box-shadow: 0 5px 15px #e8b8d433;
    margin-bottom: 22px;
}

.princess-banner h1 {
    color: #b94d85 !important;
    font-size: 30px;
    margin-bottom: 8px;
}

.princess-banner p {
    color: #9d668b;
    font-size: 15px;
}

.book-card {
    background: #ffffff;
    border: 2px solid #f8d5e7;
    border-radius: 18px;
    padding: 17px;
    margin: 10px 0;
    box-shadow: 0 4px 12px #e8b8d422;
}

div.stButton > button {
    background: #f5b8d4;
    color: #7f4264;
    border: 1px solid #f2a5ca;
    border-radius: 15px;
    font-weight: bold;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: #e9cfff;
    color: #804c9b;
    border-color: #d8b5f3;
}

div[data-testid="stTextInput"] input {
    border: 2px solid #f5c8df;
    border-radius: 14px;
    background: #fffafd;
}

div[data-testid="stAlert"] {
    border-radius: 15px;
}

hr {
    border-color: #f5d6e8;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 책 데이터
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
# 즐겨찾기 상태 저장
# -------------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

# -------------------------
# 상단 배너
# -------------------------
st.markdown("""
<div class="princess-banner">
    <div style="font-size:42px;">👑 🎀 🐰</div>
    <h1>공주님의 책장</h1>
    <p>♡ 마음에 드는 책을 소중하게 모아 보세요 ♡</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🌷 책 둘러보기", "💗 나의 즐겨찾기"])

# -------------------------
# 책 둘러보기
# -------------------------
with tab1:
    st.subheader("🎀 마음에 드는 책 고르기")
    st.caption("책을 둘러보고 하트 버튼을 눌러 즐겨찾기에 담아 보세요!")

    for i, book in enumerate(books):
        with st.container(border=True):
            st.markdown(f"### 📖 {book['제목']}")
            st.write(f"✍️ 저자: {book['저자']}")
            st.write(f"🏰 위치: {book['위치']}")
            st.write(f"🌸 서가: {book['서가']}")
            st.caption(f"청구기호: {book['청구기호']}")

            if book in st.session_state.favorites:
                st.button(
                    "💗 즐겨찾기 추가됨",
                    key=f"added_{i}",
                    disabled=True,
                    use_container_width=True
                )
                if st.button("💔 즐겨찾기에서 빼기", key=f"remove_{i}",
                             use_container_width=True):
                    st.session_state.favorites.remove(book)
                    st.rerun()
            else:
                if st.button("♡ 즐겨찾기에 담기 ♡", key=f"add_{i}",
                             use_container_width=True):
                    st.session_state.favorites.append(book)
                    st.rerun()

# -------------------------
# 나의 즐겨찾기
# -------------------------
with tab2:
    st.subheader("💖 나만의 소중한 책")
    st.caption("즐겨찾기에 담은 책을 여기에서 확인할 수 있어요!")

    favorites = st.session_state.favorites

    if favorites:
        st.success(f"🎀 현재 {len(favorites)}권의 책을 모았어요!")

        for i, book in enumerate(favorites):
            with st.container(border=True):
                st.markdown(f"### 💕 {book['제목']}")
                st.write(f"✍️ 저자: {book['저자']}")
                st.write(f"🏰 위치: {book['위치']}")
                st.write(f"🌸 서가: {book['서가']}")
                st.caption(f"청구기호: {book['청구기호']}")

                if st.button(
                    "💔 즐겨찾기 삭제",
                    key=f"delete_fav_{i}",
                    use_container_width=True
                ):
                    st.session_state.favorites.remove(book)
                    st.rerun()

        st.divider()

        if st.button("🧺 즐겨찾기 전체 비우기", use_container_width=True):
            st.session_state.favorites = []
            st.rerun()

    else:
        st.markdown("""
        <div class="book-card" style="text-align:center;">
            <div style="font-size:45px;">🧸</div>
            <h3>아직 담긴 책이 없어요!</h3>
            <p>책 둘러보기에서 마음에 드는 책을 골라 보세요 💗</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<hr>
<p style="text-align:center; color:#c28baa;">
    ♡ 나만의 작은 도서관 ♡
</p>
""", unsafe_allow_html=True)
