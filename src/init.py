import sqlite3

def init_database():
    conn = sqlite3.connect('./data/insight_data.db')
    cursor = conn.cursor()

    # 检查是否存在 err_insight 主表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS err_insight (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            semester_id INT,
            unit_id INT,
            lesson_id INT,
            question_type_id INT,
            error_reason_id INT,
            knowledge_point_id INT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (semester_id) REFERENCES semester(id),
            FOREIGN KEY (unit_id) REFERENCES unit(id),
            FOREIGN KEY (lesson_id) REFERENCES lesson(id),
            FOREIGN KEY (question_type_id) REFERENCES question_type(id),
            FOREIGN KEY (error_reason_id) REFERENCES error_reason(id),
            FOREIGN KEY (knowledge_point_id) REFERENCES knowledge_point(id)
        )
    """)

    # 创建 学期 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS semester (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)

    # 创建 单元 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)

    # 创建 课时 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lesson (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)

    # 创建 题型 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS question_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)
    
    # 创建 知识点 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_point (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)
    
    # 创建 错误原因 表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS error_reason (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)

    conn.commit()
    conn.close()
    
# 测试数据
list_semester = ["四年级上期", "四年级下期", "五年级上期"]
list_unit = ["一单元", "二单元", "三单元"]
list_lesson = ["第一课", "第二课", "第三课"]
list_question_type = ["选择题", "填空题", "应用题"]
list_knowledge_point = ["加法结合律", "乘法分配律", "商不变"]
list_reason = ["计算错误", "概念不懂", "不理解题意"]

def init_debug_data():
    conn = sqlite3.connect('./data/insight_data.db')
    cursor = conn.cursor()

    # 插入 学期 数据
    for semester_name in list_semester:
        cursor.execute("INSERT INTO semester (name) VALUES (?)", (semester_name,))

    # 插入 单元 数据
    for unit_name in list_unit:
        cursor.execute("INSERT INTO unit (name) VALUES (?)", (unit_name,))

    # 插入 课时 数据
    for lesson_name in list_lesson:
        cursor.execute("INSERT INTO lesson (name) VALUES (?)", (lesson_name,))

    # 插入 题型 数据
    for question_type_name in list_question_type:
        cursor.execute("INSERT INTO question_type (name) VALUES (?)", (question_type_name,))

    # 插入 知识点 数据
    for knowledge_point_name in list_knowledge_point:
        cursor.execute("INSERT INTO knowledge_point (name) VALUES (?)", (knowledge_point_name,))

    # 插入 错误原因 数据
    for reason_description in list_reason:
        cursor.execute("INSERT INTO error_reason (name) VALUES (?)", (reason_description,))

    conn.commit()
    conn.close()
        