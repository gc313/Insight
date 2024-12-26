# Copyright (C) 2024  ThisWaySir

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Additionally, we encourage all users to review the full license agreement to fully understand their rights and obligations. For more information about the GNU General Public License, please visit:
# - Chinese: [GNU Official Website - GNU GPLv3 Chinese](https://www.gnu.org/licenses/quick-guide-gplv3.zh-cn.html)
# - English: [GNU Official Website - GNU GPLv3 English](https://www.gnu.org/licenses/gpl-3.0.en.html)

# Thank you for supporting the open source community and the free software movement!

import streamlit as st
import pandas as pd
import time
import logging
from src import database as db
from src.constants import db_constants as db_con
from src import event_handlers as eh
from src.layout import about as abt
from functools import partial

# 设置日志记录，日志级别为 INFO
logging.basicConfig(level=logging.INFO)

def setting_button():
    # 创建一个设置按钮，当用户点击按钮时，调用 setting_dialog 函数显示设置对话框
    if st.button("设置", use_container_width=True, icon="⚙️"):
        setting_dialog()

@st.dialog("⚙️ 设置")
def setting_dialog():
    # 显示设置对话框
    tab1, tab2 = st.tabs(["统计分类", "关于"])

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
                            # 检查 name 列是否有空值
                            if editor[db_con.COLUMN_NAME].isnull().any():
                                st.error(f"{label} 数据中的“项目名称”列不能为空！", icon="⚠️")
                            else:
                                db.load_selectbox_options.clear()
                                # 调用 save_table_data 函数保存数据，并重置数据变化标志
                                db.save_setting_table_data(table_name, original_df, editor)
                                st.session_state[data_changed_key] = False
                                st.success(f"{label} 数据已保存！", icon="✔️")
                                time.sleep(0.5)
                                st.rerun(scope="fragment")
    with tab2:
        abt.about_info()