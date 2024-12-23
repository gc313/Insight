import streamlit as st
import layout.chart as chart
import database as db
import constants.db_constants as db_con

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
        db_con.TABLE_SEMESTER: db.fetch_select_data_from_table(db_con.TABLE_SEMESTER),
        db_con.TABLE_UNIT: db.fetch_select_data_from_table(db_con.TABLE_UNIT),
        db_con.TABLE_LESSON: db.fetch_select_data_from_table(db_con.TABLE_LESSON),
        db_con.TABLE_QUESTION_TYPE: db.fetch_select_data_from_table(db_con.TABLE_QUESTION_TYPE),
        db_con.TABLE_KNOWLEDGE_POINT: db.fetch_select_data_from_table(db_con.TABLE_KNOWLEDGE_POINT),
        db_con.TABLE_ERROR_REASON: db.fetch_select_data_from_table(db_con.TABLE_ERROR_REASON)
    }
    return options

# 输入数据对话框
@st.dialog("添加数据")
def input_data_dialog():
    options = load_selectbox_options()
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    with st.form(key="input_data_form"):
        semester_id = st.selectbox("学期", [row[1] for row in options[db_con.TABLE_SEMESTER]], format_func=lambda x: next(row[1] for row in options[db_con.TABLE_SEMESTER] if row[1] == x))
        unit_id = st.selectbox("单元", [row[1] for row in options[db_con.TABLE_UNIT]], format_func=lambda x: next(row[1] for row in options[db_con.TABLE_UNIT] if row[1] == x))
        lesson_id = st.selectbox("课时", [row[1] for row in options[db_con.TABLE_LESSON]], format_func=lambda x: next(row[1] for row in options[db_con.TABLE_LESSON] if row[1] == x))
        question_type_id = st.selectbox("题型", [row[1] for row in options[db_con.TABLE_QUESTION_TYPE]], format_func=lambda x: next(row[1] for row in options[db_con.TABLE_QUESTION_TYPE] if row[1] == x))
        knowledge_point_id = st.selectbox("知识点", [row[1] for row in options[db_con.TABLE_KNOWLEDGE_POINT]], format_func=lambda x: next(row[1] for row in options[db_con.TABLE_KNOWLEDGE_POINT] if row[1] == x))
        reason_id = st.selectbox("错误原因", [row[1] for row in options[db_con.TABLE_ERROR_REASON]], format_func=lambda x: next(row[1] for row in options[db_con.TABLE_ERROR_REASON] if row[1] == x))
        
        submitted = st.form_submit_button("提交")
        if submitted:
            # 将数据插入到 err_insight 表中
            cursor.execute(f"""
                INSERT INTO {db_con.TABLE_ERR_INSIGHT} ({db_con.COLUMN_SEMESTER_ID}, {db_con.COLUMN_UNIT_ID}, {db_con.COLUMN_LESSON_ID}, {db_con.COLUMN_QUESTION_TYPE_ID}, {db_con.COLUMN_KNOWLEDGE_POINT_ID}, {db_con.COLUMN_ERROR_REASON_ID})
                VALUES (?, ?, ?, ?, ?, ?)
            """, (get_option_id(options[db_con.TABLE_SEMESTER], semester_id), 
                  get_option_id(options[db_con.TABLE_UNIT], unit_id), 
                  get_option_id(options[db_con.TABLE_LESSON], lesson_id), 
                  get_option_id(options[db_con.TABLE_QUESTION_TYPE], question_type_id), 
                  get_option_id(options[db_con.TABLE_KNOWLEDGE_POINT], knowledge_point_id), 
                  get_option_id(options[db_con.TABLE_ERROR_REASON], reason_id)))
            
            conn.commit()
            st.success("数据已成功添加！")
    
    conn.close()

# 获取选项的 ID
def get_option_id(options, selected_value):
    for option in options:
        if option[1] == selected_value:
            return option[0]
    return None