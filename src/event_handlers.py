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
from src.constants import db_constants as db_con

# 定义一个回调函数，当setting界面数据被修改时触发
def on_data_change(editor_key, original_df, data_changed_key):
    # 获取编辑器的状态
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