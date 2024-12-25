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
import layout.chart as chart
import database as db

# 显示数据筛选列表
def data_filter_selectbox():
    # 创建一个下拉框供用户选择统计条件
    selected_option = st.selectbox("统计条件: ", ["学期", "单元", "课时", "题型", "知识点", "错误原因"], key="data_filter_selectbox", index=1)
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
    
# 显示添加数据按钮
def data_input_button():
    # 创建一个按钮供用户点击以添加数据
    if st.button("添加数据", use_container_width=True, icon="➕"):
        input_data_dialog()

# 输入数据对话框
@st.dialog("添加数据")
def input_data_dialog():
    db.save_error_info()