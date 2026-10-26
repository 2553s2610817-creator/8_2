
import streamlit as st
import pandas as pd

# ==========================================
# 1. 페이지 기본 설정
# ==========================================
st.set_page_config(
    page_title="스마트 도서관 길잡이",
    page_icon="📚",
    layout="wide"
)

# ==========================================
# 2. CSS 스타일 설정
# ==========================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F8FAFD;
    }

    .cover-1 {
        background: linear-gradient(
            135deg,
            #A7C7E7 0%,
            #7DA0C4 100%
        );
        padding: 8px 12px;
        border-radius: 8px;
        color: white;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }

    .main-title {
        color: #4A6FA5;
        font-weight: bold;
    }

    .book-info {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# 3. 도서 데이터 생성
# ==========================================
@st.cache_data
def load_books():
    return pd.DataFrame([
        {
            "id": 1,
            "title": "파이썬 머신러닝 완벽 가이드",
            "author": "권철민",
            "location": "2층 자연과학실",
            "shelf": "B-04 서가 3번째 선반",
            "call_number": "005.133-권36파"
        },
        {
            "id": 2,
            "title": "클린 코드",
            "author": "로버트 C. 마틴",
            "location": "2층 자연과학실",
            "shelf": "B-02 서가 1번째 선반",
            "call_number": "005.11-마898클"
        },
        {
            "id": 3,
            "title": "돈의 속성",
            "author": "김승호",
            "location": "1층 인문사회실",
            "shelf": "A-08 서가 2번째 선반",
            "call_number": "320.1-김897돈"
        },
        {
            "id": 4,
            "title": "코스모스",
            "author": "칼 세이건",
            "location": "2층 자연과학실",
            "shelf": "C-01 서가 4번째 선반",
            "call_number": "440.1-세04코"
        },
        {
            "id": 5,
            "title": "불편한 편의점",
            "author": "김호연",
            "location": "1층 문학자료실",
            "shelf": "M-05 서가 2번째 선반",
            "call_number": "813.7-김96불"
        }
    ])


books_df = load_books()

# ==========================================
# 4. 세션 상태 초기화
# ==========================================
if "favorites" not in st.session_state:
    st.session_state["favorites"] = []

# ==========================================
# 5. 메인 화면
# ==========================================
st.markdown(
    '<h1 class="main-title">📚 스마트 도서관 길잡이</h1>',
    unsafe_allow_html=True
)

st.write(
    "원하는 책의 위치를 쉽게 찾고 "
    "즐겨찾기에 담아 동선을 관리하세요."
)

st.caption(
    "도서 제목이나 저자를 검색하여 "
    "도서 위치와 청구기호를 확인할 수 있습니다."
)

# ==========================================
# 6. 탭 설정
# ==========================================
tab1, tab2, tab3 = st.tabs([
    "🔍 도서 검색 및 위치",
    "⭐ 내 즐겨찾기 목록",
    "🤖 AI 도우미"
])

# ==========================================
# 첫 번째 탭 : 도서 검색
# ==========================================
with tab1:

    st.subheader("🔍 도서 검색")

    search_query = st.text_input(
        "책 제목이나 저자를 검색하세요",
        placeholder="예: 코스모스, 김호연",
        key="book_search"
    )

    # 검색 기능
    if search_query.strip():

        filtered_df = books_df[
            books_df["title"].str.contains(
                search_query,
                case=False,
                na=False,
                regex=False
            )
            |
            books_df["author"].str.contains(
                search_query,
                case=False,
                na=False,
                regex=False
            )
        ]

    else:
        filtered_df = books_df

    # 검색 결과가 없는 경우
    if filtered_df.empty:

        st.warning(
            "검색 결과가 없습니다. "
            "다른 검색어를 입력해 보세요."
        )

    # 검색 결과 출력
    for _, row in filtered_df.iterrows():

        st.markdown(
            f"""
            <div class="cover-1">
                구역: {row['shelf'][:4]}
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns([3, 1])

        with col1:

            st.markdown(f"### 📖 {row['title']}")

            st.write(f"✍️ 저자: {row['author']}")

            st.write(
                f"📍 **위치:** {row['location']}  \n"
                f"📌 **서가:** {row['shelf']}  \n"
                f"🏷️ **청구기호:** `{row['call_number']}`"
            )

        with col2:

            # 즐겨찾기 추가 및 제거
            if row["id"] in st.session_state["favorites"]:

                if st.button(
                    "❌ 담기 취소",
                    key=f"del_{row['id']}"
                ):

                    st.session_state["favorites"].remove(
                        row["id"]
                    )

                    st.rerun()

            else:

                if st.button(
                    "⭐ 위치 담기",
                    key=f"add_{row['id']}"
                ):

                    st.session_state["favorites"].append(
                        row["id"]
                    )

                    st.rerun()

        st.divider()


# ==========================================
# 두 번째 탭 : 즐겨찾기 목록
# ==========================================
with tab2:

    st.subheader("⭐ 내 서재")

    st.write(
        "관심 있는 책을 저장하고 "
        "나중에 책의 위치를 확인할 수 있습니다."
    )

    fav_books = books_df[
        books_df["id"].isin(
            st.session_state["favorites"]
        )
    ]

    if fav_books.empty:

        st.info(
            "아직 즐겨찾기에 담긴 책이 없습니다. "
            "도서 검색에서 책을 담아보세요."
        )

    else:

        st.dataframe(
            fav_books[
                [
                    "title",
                    "author",
                    "location",
                    "shelf",
                    "call_number"
                ]
            ],
            hide_index=True,
            use_container_width=True,
            column_config={
                "title": "도서명",
                "author": "저자",
                "location": "위치(층/실)",
                "shelf": "서가 번호",
                "call_number": "청구기호"
            }
        )

        st.write("")

        if st.button("🗑️ 전체 삭제"):

            st.session_state["favorites"] = []

            st.rerun()


# ==========================================
# 세 번째 탭 : AI 도우미
# ==========================================
with tab3:

    st.subheader("🤖 도서관 AI 사서")

    st.write(
        "청구기호의 의미나 도서관 이용 방법을 "
        "AI 사서에게 질문해 보세요."
    )

    # API 키 가져오기
    api_key = st.secrets.get(
        "GEMINI_API_KEY",
        ""
    )

    # 질문 입력
    q = st.text_input(
        "질문을 입력하세요.",
        placeholder="예: 청구기호는 무엇인가요?",
        key="ai_question"
    )

    # 질문하기 버튼
    if st.button("💬 질문하기"):

        if not q.strip():

            st.warning("질문을 입력해 주세요.")

        elif not api_key:

            st.error(
                "Streamlit Secrets에 "
                "GEMINI_API_KEY가 등록되지 않았습니다."
            )

        else:

            try:

                from google import genai

                # Gemini API 설정
                client = genai.Client(
                    api_key=api_key
                )

                # AI 답변 생성
                with st.spinner(
                    "AI 사서가 답변을 작성하고 있습니다..."
                ):

                    response = client.models.generate_content(
                        model="gemini-2.5-flash-lite",
                        contents=q
                    )

                    st.markdown(
                        "### 💡 AI 사서의 답변"
                    )

                    if response.text:

                        st.write(response.text)

                    else:

                        st.warning(
                            "답변을 생성하지 못했습니다. "
                            "다시 질문해 주세요."
                        )

            except Exception as e:

                st.error(
                    f"AI 답변 생성 중 오류가 발생했습니다: {e}"
                )

# ==========================================
# 7. 하단 안내
# ==========================================
st.divider()

st.caption(
    "📚 스마트 도서관 길잡이 | "
    "도서 위치 검색 및 즐겨찾기 서비스"
)
