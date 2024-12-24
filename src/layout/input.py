import streamlit as st
import layout.chart as chart
import database as db
import constants.db_constants as db_con

# 显示数据筛选列表
def data_filter_selectbox():
    # 创建一个下拉框供用户选择统计条件
    selected_option = st.selectbox("统计条件: ", ["学期", "单元", "课时", "题型", "知识点", "错误原因"], key="data_filter_selectbox", index=1)
    # 根据用户选择的统计条件调用相应的排序函数
    if selected_option == "学期":
        return chart.sort_data_by_semester()
    elif selected_option == "单元":
        return chart.sort_data_by_unit()
    elif selected_option == "课时":
        return chart.sort_data_by_lesson()
    elif selected_option == "题型":
        return chart.sort_data_by_question_type()
    elif selected_option == "知识点":
        return chart.sort_data_by_knowledge_point()
    elif selected_option == "错误原因":
        return chart.sort_data_by_error_reason()
    
# 显示添加数据按钮
def data_input_button():
    # 创建一个按钮供用户点击以添加数据
    if st.button("添加数据", use_container_width=True, icon="➕"):
        input_data_dialog()

# 输入数据对话框
@st.dialog("添加数据")
def input_data_dialog():
    db.save_error_info()