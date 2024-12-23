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
    
    with tab1:
        with st.expander("学期"):
            semester_list = fetch_table_data("semester")
            semester_df = pd.DataFrame(semester_list, columns=["id", "name"])
            semester_df = semester_df.drop(columns=["id"])  # 去掉id列
            st.data_editor(semester_df, hide_index=True, num_rows="dynamic", key="semester_editor")
        
        with st.expander("单元"):
            unit_list = fetch_table_data("unit")
            unit_df = pd.DataFrame(unit_list, columns=["id", "name"])
            unit_df = unit_df.drop(columns=["id"])  # 去掉id列
            st.data_editor(unit_df, hide_index=True, num_rows="dynamic", key="unit_editor")
        
        with st.expander("课时"):
            lesson_list = fetch_table_data("lesson")
            lesson_df = pd.DataFrame(lesson_list, columns=["id", "name"])
            lesson_df = lesson_df.drop(columns=["id"])  # 去掉id列
            st.data_editor(lesson_df, hide_index=True, num_rows="dynamic", key="lesson_editor")
        
        with st.expander("题型"):
            question_type_list = fetch_table_data("question_type")
            question_type_df = pd.DataFrame(question_type_list, columns=["id", "name"])
            question_type_df = question_type_df.drop(columns=["id"])  # 去掉id列
            st.data_editor(question_type_df, hide_index=True, num_rows="dynamic", key="question_type_editor")
        
        with st.expander("知识点"):
            knowledge_point_list = fetch_table_data("knowledge_point")
            knowledge_point_df = pd.DataFrame(knowledge_point_list, columns=["id", "name"])
            knowledge_point_df = knowledge_point_df.drop(columns=["id"])  # 去掉id列
            st.data_editor(knowledge_point_df, hide_index=True, num_rows="dynamic", key="knowledge_point_editor")
        
        with st.expander("错误原因"):
            error_reason_list = fetch_table_data("error_reason")
            error_reason_df = pd.DataFrame(error_reason_list, columns=["id", "name"])
            error_reason_df = error_reason_df.drop(columns=["id"])  # 去掉id列
            st.data_editor(error_reason_df, hide_index=True, num_rows="dynamic", key="error_reason_editor")
        
    with tab2:
        st.empty()