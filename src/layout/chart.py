import pandas as pd
import streamlit as st
import database as db

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
    st.vega_lite_chart(chart_spec, use_container_width=True)

def sort_data_by_semester():
    return db.fetch_sorted_data('semester', 'semester', 'semester_id', 'name')

def sort_data_by_unit():
    return db.fetch_sorted_data('unit', 'unit', 'unit_id', 'name')

def sort_data_by_lesson():
    return db.fetch_sorted_data('lesson', 'lesson', 'lesson_id', 'name')

def sort_data_by_question_type():
    return db.fetch_sorted_data('question_type', 'question_type', 'question_type_id', 'name')

def sort_data_by_knowledge_point():
    return db.fetch_sorted_data('knowledge_point', 'knowledge_point', 'knowledge_point_id', 'name')

def sort_data_by_error_reason():
    return db.fetch_sorted_data('error_reason', 'error_reason', 'error_reason_id', 'name')