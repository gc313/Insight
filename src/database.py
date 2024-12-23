import sqlite3
import constants.db_constants as db_con

# 获取数据库连接
def get_db_connection():
    return sqlite3.connect(db_con.DATABASE_PATH + '/' + db_con.DATABASE_NAME)

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
            SELECT {join_table}.{group_field}, COUNT({db_con.TABLE_ERR_INSIGHT}.{db_con.COLUMN_ID}) AS error_count 
            FROM {db_con.TABLE_ERR_INSIGHT} 
            JOIN {join_table} ON {db_con.TABLE_ERR_INSIGHT}.{join_field} = {join_table}.{db_con.COLUMN_ID} 
            GROUP BY {join_table}.{group_field} 
            ORDER BY error_count DESC
        """
        cursor.execute(query)
        data = cursor.fetchall()
    return data