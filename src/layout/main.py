import streamlit as st
import layout.chart as chart
import layout.input as input
import layout.setting as setting
import layout.about as abt
from layout.layout import center_with_columns


def main_container():
    chart.draw_chart(input.data_filter_selectbox())
    
@center_with_columns
def bottom_container():
    with st.container():
            col1, col2 = st.columns(2)  # 在中间列中创建两列布局
            with col1:
                input.data_input_button()
            with col2:
                setting.setting_button()
                
@center_with_columns
def copyright():
    abt.show_copy_right()
    
