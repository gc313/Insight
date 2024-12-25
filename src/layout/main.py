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
import layout.input as input
import layout.setting as setting
import layout.about as abt
from layout.layout import center_with_columns


def main_container():
    chart_placeholder = st.empty()
    data = input.data_filter_selectbox()
    with chart_placeholder:
        chart.draw_chart(data)
    
@center_with_columns
def bottom_container():
    with st.container():
            col1, col2 = st.columns(2)  # 在中间列中创建两列布局
            with col1:
                input.data_input_button()
            with col2:
                setting.setting_button()
                
@center_with_columns
def copyright():
    abt.show_copy_right()
    
