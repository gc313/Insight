import streamlit as st
import layout.chart as chart
import layout.input as input
import layout.setting as setting

def main_container():
    chart.draw_chart(input.data_filter_selectbox())
    
def bottom_container():
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])  # 创建三列布局，中间列较宽
        with col2:
            col4, col5 = st.columns(2)  # 在中间列中创建两列布局
            with col4:
                input.data_input_button()
            with col5:
                setting.setting_button()
    
