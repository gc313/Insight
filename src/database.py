import sqlite3
import constants.db_constants as db_con

# 获取数据库连接
def get_db_connection():
    return sqlite3.connect(db_con.DATABASE_PATH + '/' + db_con.DATABASE_NAME)

def fetch_all_table_data(table_name):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
    return data


def fetch_select_data_from_table(table_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT {db_con.COLUMN_ID}, {db_con.COLUMN_NAME} FROM {table_name} ORDER BY {db_con.COLUMN_NAME}")
    rows = cursor.fetchall()
    conn.close()
    return rows


# 通用的数据库查询函数
def fetch_sorted_data(join_table, join_field, group_field):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = f"""
            SELECT {join_table}.{group_field}, COUNT({db_con.TABLE_ERR_INSIGHT}.{db_con.COLUMN_ID}) AS error_count 
            FROM {db_con.TABLE_ERR_INSIGHT} 
            JOIN {join_table} ON {db_con.TABLE_ERR_INSIGHT}.{join_field} = {join_table}.{db_con.COLUMN_ID} 
            WHERE {join_table}.{db_con.COLUMN_IS_SELECTED} = 1
            GROUP BY {join_table}.{group_field} 
            ORDER BY error_count DESC
        """
        cursor.execute(query)
        data = cursor.fetchall()
    return data