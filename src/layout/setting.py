import streamlit as st
import pandas as pd
import database as db
import constants.db_constants as db_con
from functools import partial
import time
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO)

def save_table_data(table_name, original_df, edited_df):
    conn = db.get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 移除 edited_df 中没有 'name' 值的行
        edited_df = edited_df.dropna(subset=[db_con.COLUMN_NAME])
        
        # 创建一个字典来存储原始数据的 id 和 name 对应关系
        original_dict = {row[db_con.COLUMN_NAME]: row[db_con.COLUMN_ID] for _, row in original_df.iterrows()}
        edited_dict = {row[db_con.COLUMN_NAME]: row.get(db_con.COLUMN_ID) for _, row in edited_df.iterrows()}
        
        # 找出需要删除的记录
        to_delete = [name for name in original_dict if name not in edited_dict]
        if to_delete:
            cursor.executemany(
                f"DELETE FROM {table_name} WHERE {db_con.COLUMN_NAME} = ?",
                [(name,) for name in to_delete]
            )
        
        # 找出需要插入的记录
        to_insert = [
            (row[db_con.COLUMN_NAME], row.get(db_con.COLUMN_IS_SELECTED, 1))
            for _, row in edited_df.iterrows() 
            if row[db_con.COLUMN_NAME] not in original_dict
        ]
        if to_insert:
            cursor.executemany(
                f"INSERT INTO {table_name} ({db_con.COLUMN_NAME}, {db_con.COLUMN_IS_SELECTED}) VALUES (?, ?)",
                to_insert
            )
        
        # 找出需要更新的记录
        to_update = [
            (row[db_con.COLUMN_NAME], row.get(db_con.COLUMN_IS_SELECTED, 1), original_dict[row[db_con.COLUMN_NAME]])
            for _, row in edited_df.iterrows() 
            if row[db_con.COLUMN_NAME] in original_dict and row[db_con.COLUMN_NAME] in edited_dict
        ]
        if to_update:
            cursor.executemany(
                f"UPDATE {table_name} SET {db_con.COLUMN_NAME} = ?, {db_con.COLUMN_IS_SELECTED} = ? WHERE {db_con.COLUMN_ID} = ?",
                to_update
            )
        
        conn.commit()
        logging.info(f"Data saved successfully for table: {table_name}")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error saving data for table {table_name}: {e}")
    finally:
        conn.close()

def setting_button():
    if st.button("设置", use_container_width=True, icon="⚙️"):
        setting_dialog()

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
                data_list = db.fetch_all_table_data(table_name)
                original_df = pd.DataFrame(data_list, columns=[db_con.COLUMN_ID, db_con.COLUMN_NAME, db_con.COLUMN_IS_SELECTED])
                editor_key = f"{table_name}_editor"
                data_changed_key = f"data_changed_{table_name}"
                
                # 初始化数据变化标志
                if data_changed_key not in st.session_state:
                    st.session_state[data_changed_key] = False
                
                editor = st.data_editor(
                    original_df.drop(columns=[db_con.COLUMN_ID]), 
                    num_rows="dynamic", 
                    key=editor_key, 
                    use_container_width=True,
                    column_config={
                        db_con.COLUMN_NAME: st.column_config.TextColumn("项目名称"),
                        db_con.COLUMN_IS_SELECTED: st.column_config.CheckboxColumn("是否选用")
                    },
                    on_change=partial(on_data_change, editor_key, original_df, data_changed_key)
                )
                
                # 确保 is_selected 列没有 NaN 值，使用默认值 1
                editor[db_con.COLUMN_IS_SELECTED] = editor[db_con.COLUMN_IS_SELECTED].fillna(1)
                
                # 保存按钮容器
                button_container = st.container()
                with button_container:
                    save_button_key = f"save_{table_name}"
                    if st.session_state[data_changed_key]:
                        if st.button("保存", key=save_button_key, type="primary", use_container_width=True):
                            save_table_data(table_name, original_df, editor)
                            st.session_state[data_changed_key] = False
                            st.success(f"{label} 数据已保存！")
                            time.sleep(0.8)
                            st.rerun(scope="fragment")
                            
    with tab2:
        st.empty()

def on_data_change(editor_key, original_df, data_changed_key):
    editor_state = st.session_state[editor_key]
    
    # 获取编辑过的行和新增的行
    edited_rows = editor_state.get('edited_rows', {})
    added_rows = editor_state.get('added_rows', [])
    deleted_indices = editor_state.get('deleted_rows', [])
    
    # 构建编辑过的 DataFrame
    edited_df = pd.DataFrame(list(edited_rows.values()), columns=[db_con.COLUMN_NAME, db_con.COLUMN_IS_SELECTED])
    
    # 构建新增的 DataFrame
    added_df = pd.DataFrame(added_rows, columns=[db_con.COLUMN_NAME, db_con.COLUMN_IS_SELECTED])
    
    # 构建删除的 DataFrame
    deleted_df = original_df.iloc[deleted_indices].reset_index(drop=True)
    
    # 合并编辑过的 DataFrame 和新增的 DataFrame
    combined_df = pd.concat([edited_df, added_df], ignore_index=True) if not edited_df.empty or not added_df.empty else pd.DataFrame(columns=[db_con.COLUMN_NAME, db_con.COLUMN_IS_SELECTED])

    # 确保 is_selected 列没有 NaN 值，使用默认值 1
    combined_df[db_con.COLUMN_IS_SELECTED] = combined_df[db_con.COLUMN_IS_SELECTED].fillna(1)

    # 检查是否有变化
    if not combined_df.equals(original_df.drop(columns=[db_con.COLUMN_ID])) or not deleted_df.empty:
        st.session_state[data_changed_key] = True
    else:
        st.session_state[data_changed_key] = False