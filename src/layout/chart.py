import streamlit as st
import sqlite3
import pandas as pd

# 获取数据库连接
def get_db_connection():
    return sqlite3.connect('./data/insight_data.db')

def draw_chart(data):
    data_frame = pd.DataFrame(data, columns=['name', 'error_count'])
    
    chart_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "A simple bar chart with embedded data.",
        "data": {
            "values": data_frame.to_dict(orient='records')
        },
        "mark": "bar",
        "encoding": {
            "x": {
                "field": "name",
                "type": "nominal",
                "axis": {"title": "排序条件"},
                "sort": {"field": "error_count", "order": "descending"}
            },
            "y": {
                "aggregate": "sum",
                "field": "error_count",
                "type": "quantitative",
                "axis": {"title": "错误数"}
            }
        },
        "config": {
            "mark": {
                "color": "steelblue"
            }
        }
    }
    st.vega_lite_chart(chart_spec, use_container_width = True)


def sort_data_by_semester():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 以错题数量最多的学期排序
    cursor.execute("""
        SELECT semester.name, COUNT(err_insight.id) AS error_count 
        FROM err_insight 
        JOIN semester ON err_insight.semester_id = semester.id 
        GROUP BY semester.name 
        ORDER BY error_count DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def sort_data_by_unit():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 以错题数量最多的单元排序
    cursor.execute("""
        SELECT unit.name, COUNT(err_insight.id) AS error_count 
        FROM err_insight 
        JOIN unit ON err_insight.unit_id = unit.id 
        GROUP BY unit.name 
        ORDER BY error_count DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def sort_data_by_lesson():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 以错题数量最多的课时排序
    cursor.execute("""
        SELECT lesson.name, COUNT(err_insight.id) AS error_count 
        FROM err_insight 
        JOIN lesson ON err_insight.lesson_id = lesson.id 
        GROUP BY lesson.name 
        ORDER BY error_count DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def sort_data_by_question_type():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 以错题数量最多的题目类型排序
    cursor.execute("""
        SELECT question_type.name, COUNT(err_insight.id) AS error_count 
        FROM err_insight 
        JOIN question_type ON err_insight.question_type_id = question_type.id 
        GROUP BY question_type.name 
        ORDER BY error_count DESC
    """)

def sort_data_by_knowledge_point():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 以错题数量最多的知识点排序
    cursor.execute("""
        SELECT knowledge_point.name, COUNT(err_insight.id) AS error_count 
        FROM err_insight 
        JOIN knowledge_point ON err_insight.knowledge_point_id = knowledge_point.id 
        GROUP BY knowledge_point.name 
        ORDER BY error_count DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data

def sort_data_by_error_reason():
    conn = get_db_connection()
    cursor = conn.cursor()
    # 以错题数量最多的错误原因排序
    cursor.execute("""
        SELECT error_reason.name, COUNT(err_insight.id) AS error_count 
        FROM err_insight 
        JOIN error_reason ON err_insight.error_reason_id = error_reason.id 
        GROUP BY error_reason.name 
        ORDER BY error_count DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return data