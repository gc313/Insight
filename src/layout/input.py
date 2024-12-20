import streamlit as st
import sqlite3
import layout.chart as chart

# 获取数据库连接
def get_db_connection():
    return sqlite3.connect('./data/insight_data.db')

# 获取表格数据
def fetch_table_data(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, name FROM {table_name} ORDER BY name")
    rows = cursor.fetchall()
    conn.close()
    return rows

# 显示数据筛选列表
def data_filter_selectbox():
    selected_option = st.selectbox("统计条件: ", ["学期", "单元", "课时", "题型", "知识点", "错误原因"], key="data_filter_selectbox", index=1)
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
    if st.button("添加数据"):
        input_data_dialog()

# 缓存下拉框选项
@st.cache_resource
def load_selectbox_options():
    options = {
        "semester": fetch_table_data("semester"),
        "unit": fetch_table_data("unit"),
        "lesson": fetch_table_data("lesson"),
        "question_type": fetch_table_data("question_type"),
        "knowledge_point": fetch_table_data("knowledge_point"),
        "reason": fetch_table_data("error_reason")
    }
    return options

# 输入数据对话框
@st.dialog("添加数据")
def input_data_dialog():
    options = load_selectbox_options()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    with st.form(key="input_data_form"):
        semester_id = st.selectbox("学期", [row[1] for row in options["semester"]], format_func=lambda x: next(row[1] for row in options["semester"] if row[1] == x))
        unit_id = st.selectbox("单元", [row[1] for row in options["unit"]], format_func=lambda x: next(row[1] for row in options["unit"] if row[1] == x))
        lesson_id = st.selectbox("课时", [row[1] for row in options["lesson"]], format_func=lambda x: next(row[1] for row in options["lesson"] if row[1] == x))
        question_type_id = st.selectbox("题型", [row[1] for row in options["question_type"]], format_func=lambda x: next(row[1] for row in options["question_type"] if row[1] == x))
        knowledge_point_id = st.selectbox("知识点", [row[1] for row in options["knowledge_point"]], format_func=lambda x: next(row[1] for row in options["knowledge_point"] if row[1] == x))
        reason_id = st.selectbox("错误原因", [row[1] for row in options["reason"]], format_func=lambda x: next(row[1] for row in options["reason"] if row[1] == x))
        
        submitted = st.form_submit_button("提交")
        if submitted:
            st.write(f"学期: {semester_id}")
            st.write(f"单元: {unit_id}")
            st.write(f"课时: {lesson_id}")
            st.write(f"题型: {question_type_id}")
            st.write(f"知识点: {knowledge_point_id}")
            st.write(f"错误原因: {reason_id}")

            # 将数据插入到 err_insight 表中
            cursor.execute("""
                INSERT INTO err_insight (semester_id, unit_id, lesson_id, question_type_id, knowledge_point_id, error_reason_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (get_option_id(options["semester"], semester_id), 
                  get_option_id(options["unit"], unit_id), 
                  get_option_id(options["lesson"], lesson_id), 
                  get_option_id(options["question_type"], question_type_id), 
                  get_option_id(options["knowledge_point"], knowledge_point_id), 
                  get_option_id(options["reason"], reason_id)))
            
            conn.commit()
            st.success("数据已成功添加！")
    
    conn.close()

# 获取选项的 ID
def get_option_id(options, selected_value):
    for option in options:
        if option[1] == selected_value:
            return option[0]
    return None