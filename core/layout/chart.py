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

import pandas as pd
import streamlit as st
from core import database as db
from core.constants import db_constants as db_con
from core.layout import chart_style as cs

def draw_chart(data):
    data_frame = pd.DataFrame(data, columns=['name', 'error_count'])

    # 按 error_count 降序排序
    data_frame = data_frame.sort_values(by='error_count', ascending=False)

    # 计算累计百分比
    data_frame['cumulative_percentage'] = data_frame['error_count'].cumsum() / data_frame['error_count'].sum()

    chart_spec = cs.Get_Chart_Style(data_frame)
    st.vega_lite_chart(chart_spec, use_container_width=True)

def sort_data_by_semester():
    return db.fetch_sorted_data(db_con.TABLE_SEMESTER, db_con.COLUMN_SEMESTER_ID, db_con.COLUMN_NAME)

def sort_data_by_unit():
    return db.fetch_sorted_data(db_con.TABLE_UNIT, db_con.COLUMN_UNIT_ID, db_con.COLUMN_NAME)

def sort_data_by_lesson():
    return db.fetch_sorted_data(db_con.TABLE_LESSON, db_con.COLUMN_LESSON_ID, db_con.COLUMN_NAME)

def sort_data_by_question_type():
    return db.fetch_sorted_data(db_con.TABLE_QUESTION_TYPE, db_con.COLUMN_QUESTION_TYPE_ID, db_con.COLUMN_NAME)

def sort_data_by_knowledge_point():
    return db.fetch_sorted_data(db_con.TABLE_KNOWLEDGE_POINT, db_con.COLUMN_KNOWLEDGE_POINT_ID, db_con.COLUMN_NAME)

def sort_data_by_error_reason():
    return db.fetch_sorted_data(db_con.TABLE_ERROR_REASON, db_con.COLUMN_ERROR_REASON_ID, db_con.COLUMN_NAME)