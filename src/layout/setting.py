import streamlit as st
import pandas as pd
import time
import logging
import database as db
import constants.db_constants as db_con
import event_handlers as eh
from functools import partial

# 设置日志记录，日志级别为 INFO
logging.basicConfig(level=logging.INFO)

def setting_button():
    # 创建一个设置按钮，当用户点击按钮时，调用 setting_dialog 函数显示设置对话框
    if st.button("设置", use_container_width=True, icon="⚙️"):
        setting_dialog()

@st.dialog("设置")
def setting_dialog():
    # 显示设置对话框，包含两个标签页：“统计分类”和“空”。目前“空”标签页留白
    tab1, tab2 = st.tabs(["统计分类", "空"]) # 创建两个标签页，另一个暂时留空
    
    with tab1:
        # 在“统计分类”标签页中，定义了多个表格及其对应的数据库表名
        tables = {
            "学期": db_con.TABLE_SEMESTER,
            "单元": db_con.TABLE_UNIT,
            "课时": db_con.TABLE_LESSON,
            "题型": db_con.TABLE_QUESTION_TYPE,
            "知识点": db_con.TABLE_KNOWLEDGE_POINT,
            "错误原因": db_con.TABLE_ERROR_REASON
        }
        
        for label, table_name in tables.items():
            # 遍历每个表格，创建一个可展开的区域（expander），显示表格数据
            with st.expander(label):
                # 从数据库中获取表格数据，并转换为 DataFrame
                data_list = db.fetch_all_table_data(table_name)
                original_df = pd.DataFrame(data_list, columns=[db_con.COLUMN_ID, db_con.COLUMN_NAME, db_con.COLUMN_IS_SELECTED])
                
                # 生成唯一的编辑器键和数据变化标志键
                editor_key = f"{table_name}_editor"
                data_changed_key = f"data_changed_{table_name}"
                
                # 初始化数据变化标志
                if data_changed_key not in st.session_state:
                    st.session_state[data_changed_key] = False
                
                # 使用 Streamlit 的 data_editor 组件显示和编辑数据
                editor = st.data_editor(
                    original_df.drop(columns=[db_con.COLUMN_ID]), 
                    num_rows="dynamic", 
                    key=editor_key, 
                    use_container_width=True,
                    column_config={
                        db_con.COLUMN_NAME: st.column_config.TextColumn("项目名称"),
                        db_con.COLUMN_IS_SELECTED: st.column_config.CheckboxColumn("是否选用")
                    },
                    on_change=partial(eh.on_data_change, editor_key, original_df, data_changed_key)
                )
                
                # 确保 is_selected 列没有 NaN 值，使用默认值 1
                editor[db_con.COLUMN_IS_SELECTED] = editor[db_con.COLUMN_IS_SELECTED].fillna(1)
                
                # 创建一个容器用于保存按钮
                button_container = st.container()
                with button_container:
                    save_button_key = f"save_{table_name}"
                    if st.session_state[data_changed_key]:
                        # 如果数据发生变化，显示保存按钮
                        if st.button("保存", key=save_button_key, type="primary", use_container_width=True):
                            # 调用 save_table_data 函数保存数据，并重置数据变化标志
                            db.save_setting_table_data(table_name, original_df, editor)
                            st.session_state[data_changed_key] = False
                            st.success(f"{label} 数据已保存！")
                            time.sleep(0.8)
                            st.rerun(scope="fragment")
                            logging.info(f"{label} 数据已保存！")
    # with tab2:
    #     st.empty() # 留白