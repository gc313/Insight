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

# 路径
DATABASE_PATH = './data'

# 数据库名
DATABASE_NAME = 'insight_data.db'

# 表名
TABLE_ERR_INSIGHT = 'err_insight'
TABLE_SEMESTER = 'semester'
TABLE_UNIT = 'unit'
TABLE_LESSON = 'lesson'
TABLE_QUESTION_TYPE = 'question_type'
TABLE_KNOWLEDGE_POINT = 'knowledge_point'
TABLE_ERROR_REASON = 'error_reason'

# 列名
COLUMN_ID = 'id'
COLUMN_NAME = 'name'
COLUMN_SEMESTER_ID = 'semester_id'
COLUMN_UNIT_ID = 'unit_id'
COLUMN_LESSON_ID = 'lesson_id'
COLUMN_QUESTION_TYPE_ID = 'question_type_id'
COLUMN_ERROR_REASON_ID = 'error_reason_id'
COLUMN_KNOWLEDGE_POINT_ID = 'knowledge_point_id'
COLUMN_IS_SELECTED = 'is_selected'
COLUMN_CREATED_AT = 'created_at'

# 其他常量
FOREIGN_KEY_SEMESTER = f'FOREIGN KEY ({COLUMN_SEMESTER_ID}) REFERENCES {TABLE_SEMESTER}({COLUMN_ID})'
FOREIGN_KEY_UNIT = f'FOREIGN KEY ({COLUMN_UNIT_ID}) REFERENCES {TABLE_UNIT}({COLUMN_ID})'
FOREIGN_KEY_LESSON = f'FOREIGN KEY ({COLUMN_LESSON_ID}) REFERENCES {TABLE_LESSON}({COLUMN_ID})'
FOREIGN_KEY_QUESTION_TYPE = f'FOREIGN KEY ({COLUMN_QUESTION_TYPE_ID}) REFERENCES {TABLE_QUESTION_TYPE}({COLUMN_ID})'
FOREIGN_KEY_ERROR_REASON = f'FOREIGN KEY ({COLUMN_ERROR_REASON_ID}) REFERENCES {TABLE_ERROR_REASON}({COLUMN_ID})'
FOREIGN_KEY_KNOWLEDGE_POINT = f'FOREIGN KEY ({COLUMN_KNOWLEDGE_POINT_ID}) REFERENCES {TABLE_KNOWLEDGE_POINT}({COLUMN_ID})'