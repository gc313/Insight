import streamlit as st
import pandas as pd
import database as db
import constants.db_constants as db_con

def save_table_data(table_name, original_df, edited_df):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    # 移除 edited_df 中没有 'name' 值的行
    edited_df = edited_df.dropna(subset=[db_con.COLUMN_NAME])
    
    # 创建一个字典来存储原始数据的 id 和 name 对应关系
    original_dict = {row[db_con.COLUMN_NAME]: row[db_con.COLUMN_ID] for _, row in original_df.iterrows()}
    edited_dict = {row[db_con.COLUMN_NAME]: row[db_con.COLUMN_ID] if db_con.COLUMN_ID in row else None for _, row in edited_df.iterrows()}
    
    # 找出需要删除的记录
    to_delete = [name for name in original_dict if name not in edited_dict]
    for name in to_delete:
        cursor.execute(f"DELETE FROM {table_name} WHERE {db_con.COLUMN_NAME} = ?", (name,))
    
    # 找出需要插入的记录
    to_insert = [row for _, row in edited_df.iterrows() if row[db_con.COLUMN_NAME] not in original_dict]
    for row in to_insert:
        cursor.execute(f"INSERT INTO {table_name} ({db_con.COLUMN_NAME}) VALUES (?)", (row[db_con.COLUMN_NAME],))
    
    # 找出需要更新的记录
    to_update = [row for _, row in edited_df.iterrows() if row[db_con.COLUMN_NAME] in original_dict and row[db_con.COLUMN_NAME] in edited_dict]
    for row in to_update:
        cursor.execute(f"UPDATE {table_name} SET {db_con.COLUMN_NAME} = ? WHERE {db_con.COLUMN_ID} = ?", (row[db_con.COLUMN_NAME], original_dict[row[db_con.COLUMN_NAME]]))
    
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
            "学期": db_con.TABLE_SEMESTER,
            "单元": db_con.TABLE_UNIT,
            "课时": db_con.TABLE_LESSON,
            "题型": db_con.TABLE_QUESTION_TYPE,
            "知识点": db_con.TABLE_KNOWLEDGE_POINT,
            "错误原因": db_con.TABLE_ERROR_REASON
        }
        
        for label, table_name in tables.items():
            with st.expander(label):
                data_list = db.fetch_table_data(table_name)
                original_df = pd.DataFrame(data_list, columns=[db_con.COLUMN_ID, db_con.COLUMN_NAME])
                editor = st.data_editor(original_df.drop(columns=[db_con.COLUMN_ID]), num_rows="dynamic", key=f"{table_name}_editor")
                
                col1 = st.columns(1)
                with col1[0]:
                    if st.button("保存", key=f"save_{table_name}"):
                        save_table_data(table_name, original_df, editor)
                        st.success(f"{label} 数据已保存！")
        
    with tab2:
        st.empty()