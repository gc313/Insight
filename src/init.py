import os
import database as db
import constants.db_constants as db_con

# 定义表名和列名常量
TABLES = {
    'err_insight': [
        'id INTEGER PRIMARY KEY AUTOINCREMENT',
        'semester_id INT',
        'unit_id INT',
        'lesson_id INT',
        'question_type_id INT',
        'error_reason_id INT',
        'knowledge_point_id INT',
        'created_at DATETIME DEFAULT CURRENT_TIMESTAMP',
        'FOREIGN KEY (semester_id) REFERENCES semester(id)',
        'FOREIGN KEY (unit_id) REFERENCES unit(id)',
        'FOREIGN KEY (lesson_id) REFERENCES lesson(id)',
        'FOREIGN KEY (question_type_id) REFERENCES question_type(id)',
        'FOREIGN KEY (error_reason_id) REFERENCES error_reason(id)',
        'FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_point(id)'
    ],
    'semester': ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'name TEXT UNIQUE'],
    'unit': ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'name TEXT UNIQUE'],
    'lesson': ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'name TEXT UNIQUE'],
    'question_type': ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'name TEXT UNIQUE'],
    'knowledge_point': ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'name TEXT UNIQUE'],
    'error_reason': ['id INTEGER PRIMARY KEY AUTOINCREMENT', 'name TEXT UNIQUE']
}

# 测试数据
TEST_DATA = {
    'semester': ["四年级上期", "四年级下期", "五年级上期"],
    'unit': ["一单元", "二单元", "三单元"],
    'lesson': ["第一课", "第二课", "第三课"],
    'question_type': ["选择题", "填空题", "应用题"],
    'knowledge_point': ["加法结合律", "乘法分配律", "商不变"],
    'error_reason': ["计算错误", "概念不懂", "不理解题意"]
}

def init_database():
    data_dir = db_con.DATABASE_PATH
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    with db.get_db_connection() as conn:
        cursor = conn.cursor()
        for table_name, columns in TABLES.items():
            columns_str = ', '.join(columns)
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")

def insert_data(table_name, data_list):
    with db.get_db_connection() as conn:
        cursor = conn.cursor()
        for data in data_list:
            placeholders = ', '.join(['?'] * len(data))
            cursor.execute(f"INSERT OR IGNORE INTO {table_name} (name) VALUES ({placeholders})", (data,))

def init_debug_data():
    for table_name, data_list in TEST_DATA.items():
        insert_data(table_name, data_list)