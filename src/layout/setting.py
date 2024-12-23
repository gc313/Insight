import streamlit as st
import pandas as pd
import sqlite3

# 获取数据库连接
def get_db_connection():
    return sqlite3.connect('./data/insight_data.db')

def fetch_table_data(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    conn.close()
    return data

def setting_button():
    if st.button("设置"):
        setting_dialog()
        
        
# 设置对话框
@st.dialog("设置")
def setting_dialog():
    tab1, tab2 = st.tabs(["统计分类", "空"])
    conn = get_db_connection()
    cursor = conn.cursor()
    
    with tab1:
        with st.expander("学期"):
            semester_list = fetch_table_data("semester")
            df = pd.DataFrame(semester_list, columns=["id", "name"])
            edited_df = st.data_editor(df, hide_index=True)
        with st.expander("单元"):
            unit_list = fetch_table_data("unit")
            df = pd.DataFrame(unit_list, columns=["id", "name"])
            edited_df = st.data_editor(df, hide_index=True)
        with st.expander("课时"):
            lesson_list = fetch_table_data("lesson")
            df = pd.DataFrame(lesson_list, columns=["id", "name"])
            edited_df = st.data_editor(df, hide_index=True)
        with st.expander("题型"):
            question_type_list = fetch_table_data("question_type")
            df = pd.DataFrame(question_type_list, columns=["id", "name"])
            edited_df = st.data_editor(df, hide_index=True)
        with st.expander("知识点"):
            knowledge_point_list = fetch_table_data("knowledge_point")
            df = pd.DataFrame(knowledge_point_list, columns=["id", "name"])
            edited_df = st.data_editor(df, hide_index=True)
        with st.expander("错误原因"):
            error_reason_list = fetch_table_data("error_reason")
            df = pd.DataFrame(error_reason_list, columns=["id", "name"])
            edited_df = st.data_editor(df, hide_index=True)
        
        
    with tab2:
        st.empty()