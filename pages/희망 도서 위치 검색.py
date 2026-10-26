import streamlit as st

st.set_page_config(page_title="도서관 길잡이", layout="wide")

# CSS 문법 오류가 났던 부분을 완벽하게 파이썬 문자열로 감쌌습니다.
st.markdown("""
<style>
    .cover-1 { background: linear-gradient(135deg, #A7C7E7 0%, #7DA0C4 100%); }
</style>
""", unsafe_allow_html=True)

st.title("📚 스마트 도서관 길잡이")
st.success
