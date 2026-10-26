import streamlit as st
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="스마트 도서관 길잡이", page_icon="📚", layout="wide")

# 2. 오류가 발생했던 CSS 스타일 코드를 100% 안전하게 수정
st.markdown("""
<style>
    .cover-1 { 
        background: linear-gradient(135deg, #A7C7E7 0%, #7DA0C4 100%); 
        padding: 8px 12px; 
        border-radius: 5px; 
        color: white; 
        font-weight: bold; 
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)
