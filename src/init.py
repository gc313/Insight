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
            description TEXT
        )
    """)

    conn.commit()
    conn.close()