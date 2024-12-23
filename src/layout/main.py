import streamlit as st
import layout.chart as chart
import layout.input as input
import layout.setting as setting

def main_container():
    chart.draw_chart(input.data_filter_selectbox())
    
def bottom_container():
    input.data_input_button()
    setting.setting_button()
    
