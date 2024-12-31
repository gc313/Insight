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

import sqlite3
import time
import streamlit as st
from core.constants import db_constants as db_con

# 获取数据库连接
def get_db_connection():
    return sqlite3.connect(db_con.DATABASE_PATH + '/' + db_con.DATABASE_NAME)

# 从指定表中获取所有数据
def fetch_all_table_data(table_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
    return data

# 从指定表中获取特定列的数据，并按名称排序
def fetch_select_data_from_table(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {db_con.COLUMN_ID}, {db_con.COLUMN_NAME} FROM {table_name} ORDER BY {db_con.COLUMN_NAME}")
    rows = cursor.fetchall()
    conn.close()
    return rows

# 通用的数据库查询函数，用于获取分组后的错误计数，并按计数降序排序
def fetch_sorted_data(join_table, join_field, group_field):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 判断 join_table 是否为 semester 表
        if join_table == db_con.TABLE_SEMESTER:
            query = f"""
                SELECT {join_table}.{group_field} AS group_field, COUNT({db_con.TABLE_ERR_INSIGHT}.{db_con.COLUMN_ID}) AS error_count
                FROM {db_con.TABLE_ERR_INSIGHT}
                JOIN {join_table} ON {db_con.TABLE_ERR_INSIGHT}.{join_field} = {join_table}.{db_con.COLUMN_ID}
                WHERE {join_table}.{db_con.COLUMN_IS_SELECTED} = 1
                GROUP BY {join_table}.{group_field}
                ORDER BY error_count DESC
            """
        else:
            query = f"""
                SELECT {join_table}.{group_field} AS group_field, COUNT({db_con.TABLE_ERR_INSIGHT}.{db_con.COLUMN_ID}) AS error_count
                FROM {db_con.TABLE_ERR_INSIGHT}
                JOIN {join_table} ON {db_con.TABLE_ERR_INSIGHT}.{join_field} = {join_table}.{db_con.COLUMN_ID}
                JOIN {db_con.TABLE_SEMESTER} ON {db_con.TABLE_ERR_INSIGHT}.{db_con.COLUMN_SEMESTER_ID} = {db_con.TABLE_SEMESTER}.{db_con.COLUMN_ID}
                WHERE {join_table}.{db_con.COLUMN_IS_SELECTED} = 1
                AND {db_con.TABLE_SEMESTER}.{db_con.COLUMN_IS_SELECTED} = 1
                GROUP BY {join_table}.{group_field}
                ORDER BY error_count DESC
            """
        
        cursor.execute(query)
        data = cursor.fetchall()
    return data

# 保存setting数据到数据库，包括删除、插入和更新操作
def save_setting_table_data(table_name, original_df, edited_df):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 移除 edited_df 中没有 'name' 值的行
        edited_df = edited_df.dropna(subset=[db_con.COLUMN_NAME])

        # 创建字典存储原始数据和编辑后数据的 id 和 name 对应关系
        original_dict = {row[db_con.COLUMN_NAME]: row[db_con.COLUMN_ID] for _, row in original_df.iterrows()}
        edited_dict = {row[db_con.COLUMN_NAME]: row.get(db_con.COLUMN_ID) for _, row in edited_df.iterrows()}

        # 找出需要删除的记录并执行删除操作
        to_delete = [name for name in original_dict if name not in edited_dict]
        if to_delete:
            cursor.executemany(
                f"DELETE FROM {table_name} WHERE {db_con.COLUMN_NAME} = ?",
                [(name,) for name in to_delete]
            )

        # 找出需要插入的记录并执行插入操作
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

        # 找出需要更新的记录并执行更新操作
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
    except Exception as e:
        st.error(f"数据保存失败: {e}", icon="🚨")
        conn.rollback()
    finally:
        conn.close()

# 缓存下拉框选项
@st.cache_resource()
def load_selectbox_options():
    # 从数据库中加载各个表的数据选项，并缓存结果
    options = {
        db_con.TABLE_SEMESTER: fetch_select_data_from_table(db_con.TABLE_SEMESTER),
        db_con.TABLE_UNIT: fetch_select_data_from_table(db_con.TABLE_UNIT),
        db_con.TABLE_LESSON: fetch_select_data_from_table(db_con.TABLE_LESSON),
        db_con.TABLE_QUESTION_TYPE: fetch_select_data_from_table(db_con.TABLE_QUESTION_TYPE),
        db_con.TABLE_KNOWLEDGE_POINT: fetch_select_data_from_table(db_con.TABLE_KNOWLEDGE_POINT),
        db_con.TABLE_ERROR_REASON: fetch_select_data_from_table(db_con.TABLE_ERROR_REASON)
    }
    return options

# 保存错误信息到数据库
def save_error_info():
    # 获取数据库连接
    conn = get_db_connection()
    cursor = conn.cursor()
    # 加载下拉框选项
    options = load_selectbox_options()

    with st.form(key="input_data_form"):
        # 创建各个字段的下拉框供用户选择
        semester_id = st.selectbox("学期", [row[1] for row in options[db_con.TABLE_SEMESTER]], format_func=lambda x: next(row[1] for row in options[db_con.TABLE_SEMESTER] if row[1] == x))
        unit_id = st.selectbox("单元", [row[1] for row in options[db_con.TABLE_UNIT]], format_func=lambda x: next(row[1] for row in options[db_con.TABLE_UNIT] if row[1] == x))
        lesson_id = st.selectbox("课时", [row[1] for row in options[db_con.TABLE_LESSON]], format_func=lambda x: next(row[1] for row in options[db_con.TABLE_LESSON] if row[1] == x))
        question_type_id = st.selectbox("题型", [row[1] for row in options[db_con.TABLE_QUESTION_TYPE]], format_func=lambda x: next(row[1] for row in options[db_con.TABLE_QUESTION_TYPE] if row[1] == x))
        knowledge_point_id = st.selectbox("知识点", [row[1] for row in options[db_con.TABLE_KNOWLEDGE_POINT]], format_func=lambda x: next(row[1] for row in options[db_con.TABLE_KNOWLEDGE_POINT] if row[1] == x))
        reason_id = st.selectbox("错误原因", [row[1] for row in options[db_con.TABLE_ERROR_REASON]], format_func=lambda x: next(row[1] for row in options[db_con.TABLE_ERROR_REASON] if row[1] == x))

        # 创建提交按钮
        submitted = st.form_submit_button("提交", type="primary", use_container_width=True)
        if submitted:
            # 验证所有 selectbox 的值是否为空
            if not semester_id or not unit_id or not lesson_id or not question_type_id or not knowledge_point_id or not reason_id:
                st.error("请选择所有字段！", icon="⚠️")
            else:
                try:
                    # 将用户选择的数据插入到 err_insight 表中
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
                    st.success("数据已添加！", icon="✔️")
                except Exception as e:
                    st.error(f"数据保存失败: {e}", icon="🚨")
                    conn.rollback()
                finally:
                    # 确保在任何情况下都关闭数据库连接
                    conn.close()
                    time.sleep(0.8)
                    st.rerun(scope="fragment")

# 获取选项的 ID
def get_option_id(options, selected_value):
    # 根据用户选择的值查找对应的ID
    for option in options:
        if option[1] == selected_value:
            return option[0]
    return None