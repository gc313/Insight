import streamlit as st
from functools import wraps

def center_with_columns(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 添加自定义 CSS 样式
        st.markdown(
            """
            <style>
            .center-container {
                display: flex;
                justify-content: center;
                width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        # 使用 st.container 创建一个容器
        with st.container():
            # 使用 st.columns 创建三列布局，中间一列用于放置内容
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown('<div class="center-container">', unsafe_allow_html=True)
                result = func(*args, **kwargs)
                st.markdown('</div>', unsafe_allow_html=True)
        return result
    return wrapper