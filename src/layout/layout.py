# Copyright (C) 2024  ThisWaySir

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Additionally, we encourage all users to review the full license agreement to fully understand their rights and obligations. For more information about the GNU General Public License, please visit:
# - Chinese: [GNU Official Website - GNU GPLv3 Chinese](https://www.gnu.org/licenses/quick-guide-gplv3.zh-cn.html)
# - English: [GNU Official Website - GNU GPLv3 English](https://www.gnu.org/licenses/gpl-3.0.en.html)

# Thank you for supporting the open source community and the free software movement!

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


def left_with_columns(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 添加自定义 CSS 样式
        st.markdown(
            """
            <style>
            .left-container {
                display: flex;
                justify-content: left;
                width: 100%;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        
        # 使用st.columns创建5列
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # 调用被装饰的函数
            func(*args, **kwargs)
        
        # 其他列可以留空或添加其他内容
        with col2:
            st.empty()
        with col3:
            st.empty()
    
    return wrapper