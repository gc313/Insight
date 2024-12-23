import streamlit as st
import pandas as pd
import database as db

def save_table_data(table_name, original_df, edited_df):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # 移除 edited_df 中没有 'name' 值的行
    edited_df = edited_df.dropna(subset=['name'])
    
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
        tables = {
            "学期": "semester",
            "单元": "unit",
            "课时": "lesson",
            "题型": "question_type",
            "知识点": "knowledge_point",
            "错误原因": "error_reason"
        }
        
        for label, table_name in tables.items():
            with st.expander(label):
                data_list = db.fetch_table_data(table_name)
                original_df = pd.DataFrame(data_list, columns=["id", "name"])
                editor = st.data_editor(original_df.drop(columns=["id"]), num_rows="dynamic", key=f"{table_name}_editor")
                
                col1 = st.columns(1)
                with col1[0]:
                    if st.button("保存", key=f"save_{table_name}"):
                        save_table_data(table_name, original_df, editor)
                        st.success(f"{label} 数据已保存！")
        
    with tab2:
        st.empty()