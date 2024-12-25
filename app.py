import sys
sys.path.append('./src')
import init as init
import streamlit as st
import layout.main as main

st.set_page_config(
    page_title="Insight",
    page_icon="🧊",
    layout="wide"
)
    
if __name__ == "__main__":
    init.init_database()
    #init.init_debug_data() # 初始化调试数据
    main.main_container()
    main.bottom_container()
    main.copyright()