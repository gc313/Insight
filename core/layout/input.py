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

import time
import streamlit as st
from core.layout import chart
from core import database as db
from core.constants import db_constants as db_con
from core.layout.layout import center_with_columns


# 显示数据筛选列表
def data_filter_selectbox():
    # 创建一个下拉框供用户选择统计条件
    selected_option = data_selectbox()
    # 根据用户选择的统计条件调用相应的排序函数
    if selected_option == "学期":
        return chart.sort_data_by_semester()
    elif selected_option == "单元":
        return chart.sort_data_by_unit()
    elif selected_option == "课时":
        return chart.sort_data_by_lesson()
    elif selected_option == "题型":
        return chart.sort_data_by_question_type()
    elif selected_option == "知识点":
        return chart.sort_data_by_knowledge_point()
    elif selected_option == "错误原因":
        return chart.sort_data_by_error_reason()

@center_with_columns
def data_selectbox():
    return st.selectbox(
        "数据筛选",
        ["学期", "单元", "课时", "题型", "知识点", "错误原因"],
        key="data_filter_selectbox",
        index=1
    )

# 显示添加数据按钮
def data_input_button():
    # 创建一个按钮供用户点击以添加数据
    if st.button("添加数据", use_container_width=True, icon="✏️"):
        input_data_dialog()

# 输入数据对话框
@st.dialog("✏️ 添加数据")
def input_data_dialog():
    # 加载下拉框选项
    options = db.load_selectbox_options()

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
                db.recode_error_statistics(options, semester_id, unit_id, lesson_id, question_type_id, knowledge_point_id, reason_id)
                time.sleep(0.5)
                st.rerun(scope="fragment")
                