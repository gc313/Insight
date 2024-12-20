import streamlit as st
import sys
sys.path.append('./src')  # 添加 src 目录到系统路径
import init

st.text("Hello World")

if __name__ == "__main__":
    init.init_database()