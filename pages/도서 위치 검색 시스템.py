import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정 (가장 먼저 와야 함)
st.set_page_config(
    page_title="도서 위치 검색",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 가상의 도서 데이터베이스 생성
@st.cache_data
def load_data():
    return pd.DataFrame({
        '도서명': ['불편한 편의점', '달러구트 꿈 백화점', '오늘 밤, 세계에서 이 사랑이 사라진다 해도', '지적 대화를 위한 넓고 얕은 지식', '역행자', '아몬드', '코스모스'],
        '저자': ['김호연', '이미예', '이치조 미사키', '채사장', '자청', '손원평', '칼 세이건'],
        '분류': ['소설', '소설', '소설', '인문', '자기계발', '소설', '과학'],
        '위치': ['A구역 3층-12', 'B구역 2층-05', 'A구역 3층-15', 'D구역 1층-02', 'C구역 2층-11', 'A구역 3층-08', 'E구역 4층-01'],
        '상태': ['대출가능', '대출중', '대출가능', '대출가능', '대출중', '대출가능', '대출가능']
    })

books_df = load_data()

# 3. 사이드바 구성 (새로 들어온 책)
with st.sidebar:
    st.header("✨ 새로 들어온 책")
    st.markdown("---")
    
    # 최근 도서 3개만 추출해서 보여주기
    new_books = books_df.head(3)
    for index, row in new_books.iterrows():
        st.markdown(f"### 📘 {row['도서명']}")
        st.caption(f"{row['저자']} | {row['분류']}")
        st.markdown(" ")

# 4. 메인 화면 구성
st.title("📖 도서 위치 검색")
st.markdown("#### 원하는 책을 더 빠르고, 더 쉽게 찾으세요!")
st.markdown("<br>", unsafe_allow_html=True)

# 검색 영역
search_query = st.text_input("🔍 찾고 싶은 책 제목이나 저자를 입력해보세요!", placeholder="예: 불편한 편의점, 김호연")

# 해시태그 버튼 (장식용)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("# 인기 도서", use_container_width=True)
with col2:
    st.button("# 신간 도서", use_container_width=True)
with col3:
    st.button("# 베스트셀러", use_container_width=True)
with col4:
    st.button("# 문학상 수상작", use_container_width=True)

st.markdown("---")

# 5. 검색 결과 및 주요 기능 안내 처리
if search_query:
    # 검색어가 있을 경우 데이터 필터링 (도서명 또는 저자에 포함되는지 확인)
    filtered_df = books_df[
        books_df['도서명'].str.contains(search_query, case=False, na=False) | 
        books_df['저자'].str.contains(search_query, case=False, na=False)
    ]
    
    st.subheader(f"'{search_query}' 검색 결과 ({len(filtered_df)}건)")
    
    if len(filtered_df) > 0:
        # 결과를 깔끔한 데이터프레임으로 출력
        st.dataframe(
            filtered_df,
            column_config={
                "도서명": st.column_config.TextColumn("도서명", width="large"),
                "상태": st.column_config.TextColumn("대출 상태")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.warning("찾으시는 도서가 없습니다. 철자나 띄어쓰기를 확인해 주세요.")

else:
    # 검색어가 없을 때 보여줄 4가지 특징 안내 (원본 디자인 반영)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.info("**🔍 간편한 검색**\n\n책 제목, 저자, 키워드로 쉽게 검색할 수 있어요.")
    with c2:
        st.success("**📍 도서 위치 확인**\n\n찾고 있는 책의 정확한 서가 위치를 알려드려요.")
    with c3:
        st.warning("**📖 신간 도서 확인**\n\n지금 가장 인기 있는 새로운 책들을 만나보세요.")
    with c4:
        st.error("**⚡ 빠르고 정확하게**\n\n원하는 책을 더 빠르고, 더 쉽게 찾아보세요.")
