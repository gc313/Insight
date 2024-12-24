import pandas as pd
import streamlit as st
import database as db
import constants.db_constants as db_con
import layout.chart_style as cs

def draw_chart(data):
    data_frame = pd.DataFrame(data, columns=['name', 'error_count'])
    
    # 按 error_count 降序排序
    data_frame = data_frame.sort_values(by='error_count', ascending=False)
    
    # 计算累计百分比
    data_frame['cumulative_percentage'] = data_frame['error_count'].cumsum() / data_frame['error_count'].sum()
    
    chart_spec = cs.Get_Chart_Style(data_frame)
    st.vega_lite_chart(chart_spec, use_container_width=True)

def sort_data_by_semester():
    return db.fetch_sorted_data(db_con.TABLE_SEMESTER, db_con.COLUMN_SEMESTER_ID, db_con.COLUMN_NAME)

def sort_data_by_unit():
    return db.fetch_sorted_data(db_con.TABLE_UNIT, db_con.COLUMN_UNIT_ID, db_con.COLUMN_NAME)

def sort_data_by_lesson():
    return db.fetch_sorted_data(db_con.TABLE_LESSON, db_con.COLUMN_LESSON_ID, db_con.COLUMN_NAME)

def sort_data_by_question_type():
    return db.fetch_sorted_data(db_con.TABLE_QUESTION_TYPE, db_con.COLUMN_QUESTION_TYPE_ID, db_con.COLUMN_NAME)

def sort_data_by_knowledge_point():
    return db.fetch_sorted_data(db_con.TABLE_KNOWLEDGE_POINT, db_con.COLUMN_KNOWLEDGE_POINT_ID, db_con.COLUMN_NAME)

def sort_data_by_error_reason():
    return db.fetch_sorted_data(db_con.TABLE_ERROR_REASON, db_con.COLUMN_ERROR_REASON_ID, db_con.COLUMN_NAME)