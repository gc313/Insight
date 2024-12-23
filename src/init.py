import os
import database as db
import constants.db_constants as db_con

# 定义表名和列名常量
TABLES = {
    db_con.TABLE_ERR_INSIGHT: [
        f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT',
        f'{db_con.COLUMN_SEMESTER_ID} INT',
        f'{db_con.COLUMN_UNIT_ID} INT',
        f'{db_con.COLUMN_LESSON_ID} INT',
        f'{db_con.COLUMN_QUESTION_TYPE_ID} INT',
        f'{db_con.COLUMN_ERROR_REASON_ID} INT',
        f'{db_con.COLUMN_KNOWLEDGE_POINT_ID} INT',
        f'{db_con.COLUMN_CREATED_AT} DATETIME DEFAULT CURRENT_TIMESTAMP',
        db_con.FOREIGN_KEY_SEMESTER,
        db_con.FOREIGN_KEY_UNIT,
        db_con.FOREIGN_KEY_LESSON,
        db_con.FOREIGN_KEY_QUESTION_TYPE,
        db_con.FOREIGN_KEY_ERROR_REASON,
        db_con.FOREIGN_KEY_KNOWLEDGE_POINT
    ],
    db_con.TABLE_SEMESTER: [f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT', f'{db_con.COLUMN_NAME} TEXT UNIQUE'],
    db_con.TABLE_UNIT: [f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT', f'{db_con.COLUMN_NAME} TEXT UNIQUE'],
    db_con.TABLE_LESSON: [f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT', f'{db_con.COLUMN_NAME} TEXT UNIQUE'],
    db_con.TABLE_QUESTION_TYPE: [f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT', f'{db_con.COLUMN_NAME} TEXT UNIQUE'],
    db_con.TABLE_KNOWLEDGE_POINT: [f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT', f'{db_con.COLUMN_NAME} TEXT UNIQUE'],
    db_con.TABLE_ERROR_REASON: [f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT', f'{db_con.COLUMN_NAME} TEXT UNIQUE']
}

# 测试数据
TEST_DATA = {
    db_con.TABLE_SEMESTER: ["四年级上期", "四年级下期", "五年级上期"],
    db_con.TABLE_UNIT: ["一单元", "二单元", "三单元"],
    db_con.TABLE_LESSON: ["第一课", "第二课", "第三课"],
    db_con.TABLE_QUESTION_TYPE: ["选择题", "填空题", "应用题"],
    db_con.TABLE_KNOWLEDGE_POINT: ["加法结合律", "乘法分配律", "商不变"],
    db_con.TABLE_ERROR_REASON: ["计算错误", "概念不懂", "不理解题意"]
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
            cursor.execute(f"INSERT OR IGNORE INTO {table_name} ({db_con.COLUMN_NAME}) VALUES (?)", (data,))

def init_debug_data():
    for table_name, data_list in TEST_DATA.items():
        insert_data(table_name, data_list)