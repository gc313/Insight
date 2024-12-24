import os
import database as db
import constants.db_constants as db_con

# 定义表名和列名常量
TABLES = {
    db_con.TABLE_ERR_INSIGHT: [
        f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT',  # 主键自增
        f'{db_con.COLUMN_SEMESTER_ID} INT',  # 学期ID
        f'{db_con.COLUMN_UNIT_ID} INT',  # 单元ID
        f'{db_con.COLUMN_LESSON_ID} INT',  # 课程ID
        f'{db_con.COLUMN_QUESTION_TYPE_ID} INT',  # 题目类型ID
        f'{db_con.COLUMN_ERROR_REASON_ID} INT',  # 错误原因ID
        f'{db_con.COLUMN_KNOWLEDGE_POINT_ID} INT',  # 知识点ID
        f'{db_con.COLUMN_CREATED_AT} DATETIME DEFAULT CURRENT_TIMESTAMP',  # 创建时间，默认当前时间
        db_con.FOREIGN_KEY_SEMESTER,  # 外键，关联学期表
        db_con.FOREIGN_KEY_UNIT,  # 外键，关联单元表
        db_con.FOREIGN_KEY_LESSON,  # 外键，关联课程表
        db_con.FOREIGN_KEY_QUESTION_TYPE,  # 外键，关联题目类型表
        db_con.FOREIGN_KEY_ERROR_REASON,  # 外键，关联错误原因表
        db_con.FOREIGN_KEY_KNOWLEDGE_POINT  # 外键，关联知识点表
    ],
    db_con.TABLE_SEMESTER: [f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT', f'{db_con.COLUMN_NAME} TEXT UNIQUE', f'{db_con.COLUMN_IS_SELECTED} BOOLEAN DEFAULT 1'],  # 学期表
    db_con.TABLE_UNIT: [f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT', f'{db_con.COLUMN_NAME} TEXT UNIQUE', f'{db_con.COLUMN_IS_SELECTED} BOOLEAN DEFAULT 1'],  # 单元表
    db_con.TABLE_LESSON: [f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT', f'{db_con.COLUMN_NAME} TEXT UNIQUE', f'{db_con.COLUMN_IS_SELECTED} BOOLEAN DEFAULT 1'],  # 课程表
    db_con.TABLE_QUESTION_TYPE: [f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT', f'{db_con.COLUMN_NAME} TEXT UNIQUE', f'{db_con.COLUMN_IS_SELECTED} BOOLEAN DEFAULT 1'],  # 题目类型表
    db_con.TABLE_KNOWLEDGE_POINT: [f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT', f'{db_con.COLUMN_NAME} TEXT UNIQUE', f'{db_con.COLUMN_IS_SELECTED} BOOLEAN DEFAULT 1'],  # 知识点表
    db_con.TABLE_ERROR_REASON: [f'{db_con.COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT', f'{db_con.COLUMN_NAME} TEXT UNIQUE', f'{db_con.COLUMN_IS_SELECTED} BOOLEAN DEFAULT 1']  # 错误原因表
}

# 测试数据
TEST_DATA = {
    db_con.TABLE_SEMESTER: ["四年级上期", "四年级下期", "五年级上期"],  # 学期测试数据
    db_con.TABLE_UNIT: ["一单元", "二单元", "三单元"],  # 单元测试数据
    db_con.TABLE_LESSON: ["第一课", "第二课", "第三课"],  # 课程测试数据
    db_con.TABLE_QUESTION_TYPE: ["选择题", "填空题", "应用题"],  # 题目类型测试数据
    db_con.TABLE_KNOWLEDGE_POINT: ["加法结合律", "乘法分配律", "商不变"],  # 知识点测试数据
    db_con.TABLE_ERROR_REASON: ["计算错误", "概念不懂", "不理解题意"]  # 错误原因测试数据
}

def init_database():
    data_dir = db_con.DATABASE_PATH  # 数据库路径
    if not os.path.exists(data_dir):  # 如果数据库路径不存在
        os.makedirs(data_dir)  # 创建数据库路径
        
    with db.get_db_connection() as conn:  # 获取数据库连接
        cursor = conn.cursor()  # 创建游标
        for table_name, columns in TABLES.items():  # 遍历表名和列定义
            columns_str = ', '.join(columns)  # 将列定义拼接成字符串
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})")  # 创建表，如果表不存在

def insert_data(table_name, data_list):
    with db.get_db_connection() as conn:  # 获取数据库连接
        cursor = conn.cursor()  # 创建游标
        for data in data_list:  # 遍历数据列表
            cursor.execute(f"INSERT OR IGNORE INTO {table_name} ({db_con.COLUMN_NAME}) VALUES (?)", (data,))  # 插入数据，如果已存在则忽略

def init_debug_data():
    for table_name, data_list in TEST_DATA.items():  # 遍历测试数据
        insert_data(table_name, data_list)  # 插入测试数据