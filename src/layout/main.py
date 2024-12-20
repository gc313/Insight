import streamlit as st
import layout.chart as chart
import layout.input as input

def main_container():
    chart.draw_chart()
    
def bottom_container():
    input.data_input_button()
    
