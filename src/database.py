import sqlite3

# 获取数据库连接
def get_db_connection():
    return sqlite3.connect('./data/insight_data.db')

def fetch_table_data(table_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
    return data

# 通用的数据库查询函数
def fetch_sorted_data(table_name, join_table, join_field, group_field):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = f"""
            SELECT {join_table}.name, COUNT(err_insight.id) AS error_count 
            FROM err_insight 
            JOIN {join_table} ON err_insight.{join_field} = {join_table}.id 
            GROUP BY {join_table}.name 
            ORDER BY error_count DESC
        """
        cursor.execute(query)
        data = cursor.fetchall()
    return data