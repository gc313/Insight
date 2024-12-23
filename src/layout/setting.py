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

def save_table_data(table_name, original_df, edited_df):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建一个字典来存储原始数据的 id 和 name 对应关系
    original_dict = {row['name']: row['id'] for _, row in original_df.iterrows()}
    edited_dict = {row['name']: row['id'] if 'id' in row else None for _, row in edited_df.iterrows()}
    
    # 找出需要删除的记录
    to_delete = [name for name in original_dict if name not in edited_dict]
    for name in to_delete:
        cursor.execute(f"DELETE FROM {table_name} WHERE name = ?", (name,))
    
    # 找出需要插入的记录
    to_insert = [row for _, row in edited_df.iterrows() if row['name'] not in original_dict]
    for row in to_insert:
        cursor.execute(f"INSERT INTO {table_name} (name) VALUES (?)", (row['name'],))
    
    # 找出需要更新的记录
    to_update = [row for _, row in edited_df.iterrows() if row['name'] in original_dict and row['name'] in edited_dict]
    for row in to_update:
        cursor.execute(f"UPDATE {table_name} SET name = ? WHERE id = ?", (row['name'], original_dict[row['name']]))
    
    conn.commit()
    conn.close()

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
            original_semester_df = pd.DataFrame(semester_list, columns=["id", "name"])
            semester_editor = st.data_editor(original_semester_df.drop(columns=["id"]), num_rows="dynamic", key="semester_editor")
            
            col1 = st.columns(1)
            with col1[0]:
                if st.button("保存", key="save_semester"):
                    save_table_data("semester", original_semester_df, semester_editor)
                    st.success("学期数据已保存！")
        
        with st.expander("单元"):
            unit_list = fetch_table_data("unit")
            original_unit_df = pd.DataFrame(unit_list, columns=["id", "name"])
            unit_editor = st.data_editor(original_unit_df.drop(columns=["id"]), num_rows="dynamic", key="unit_editor")
            
            col1 = st.columns(1)
            with col1[0]:
                if st.button("保存", key="save_unit"):
                    save_table_data("unit", original_unit_df, unit_editor)
                    st.success("单元数据已保存！")
        
        with st.expander("课时"):
            lesson_list = fetch_table_data("lesson")
            original_lesson_df = pd.DataFrame(lesson_list, columns=["id", "name"])
            lesson_editor = st.data_editor(original_lesson_df.drop(columns=["id"]), num_rows="dynamic", key="lesson_editor")
            
            col1 = st.columns(1)
            with col1[0]:
                if st.button("保存", key="save_lesson"):
                    save_table_data("lesson", original_lesson_df, lesson_editor)
                    st.success("课时数据已保存！")
        
        with st.expander("题型"):
            question_type_list = fetch_table_data("question_type")
            original_question_type_df = pd.DataFrame(question_type_list, columns=["id", "name"])
            question_type_editor = st.data_editor(original_question_type_df.drop(columns=["id"]), num_rows="dynamic", key="question_type_editor")
            
            col1 = st.columns(1)
            with col1[0]:
                if st.button("保存", key="save_question_type"):
                    save_table_data("question_type", original_question_type_df, question_type_editor)
                    st.success("题型数据已保存！")
        
        with st.expander("知识点"):
            knowledge_point_list = fetch_table_data("knowledge_point")
            original_knowledge_point_df = pd.DataFrame(knowledge_point_list, columns=["id", "name"])
            knowledge_point_editor = st.data_editor(original_knowledge_point_df.drop(columns=["id"]), num_rows="dynamic", key="knowledge_point_editor")
            
            col1 = st.columns(1)
            with col1[0]:
                if st.button("保存", key="save_knowledge_point"):
                    save_table_data("knowledge_point", original_knowledge_point_df, knowledge_point_editor)
                    st.success("知识点数据已保存！")
        
        with st.expander("错误原因"):
            error_reason_list = fetch_table_data("error_reason")
            original_error_reason_df = pd.DataFrame(error_reason_list, columns=["id", "name"])
            error_reason_editor = st.data_editor(original_error_reason_df.drop(columns=["id"]), num_rows="dynamic", key="error_reason_editor")
            
            col1 = st.columns(1)
            with col1[0]:
                if st.button("保存", key="save_error_reason"):
                    save_table_data("error_reason", original_error_reason_df, error_reason_editor)
                    st.success("错误原因数据已保存！")
        
    with tab2:
        st.empty()