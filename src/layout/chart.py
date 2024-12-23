import pandas as pd
import streamlit as st
import database as db
import constants.db_constants as db_con

def draw_chart(data):
    data_frame = pd.DataFrame(data, columns=['name', 'error_count'])
    
    # 按 error_count 降序排序
    data_frame = data_frame.sort_values(by='error_count', ascending=False)
    
    # 计算累计百分比
    data_frame['cumulative_percentage'] = data_frame['error_count'].cumsum() / data_frame['error_count'].sum() * 100
    
    chart_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "A simple bar chart with embedded data and a line chart for cumulative percentage.",
        "data": {
            "values": data_frame.to_dict(orient='records')
        },
        "layer": [
            {
                "mark": "bar",
                "encoding": {
                    "x": {
                        "field": "name",
                        "type": "nominal",
                        "axis": {"title": "排序条件"},
                        "sort": {"field": "error_count", "order": "descending"}
                    },
                    "y": {
                        "field": "error_count",
                        "type": "quantitative",
                        "axis": {"title": "错误数", "orient": "left"}
                    }
                }
            },
            {
                "mark": "text",
                "encoding": {
                    "x": {
                        "field": "name",
                        "type": "nominal",
                        "axis": {"title": "排序条件"},
                        "sort": {"field": "error_count", "order": "descending"}
                    },
                    "y": {
                        "field": "error_count",
                        "type": "quantitative",
                        "axis": {"title": "错误数", "orient": "left"},
                        "offset": 50  # 将数值标签往上移一点
                    },
                    "text": {"field": "error_count"}
                }
            },
            {
                "mark": {
                    "type": "line",
                    "point": {"filled": False}
                },
                "encoding": {
                    "x": {
                        "field": "name",
                        "type": "nominal",
                        "axis": {"title": "排序条件"},
                        "sort": {"field": "cumulative_percentage", "order": "ascending"}  # 确保 x 轴顺序与累计百分比一致
                    },
                    "y": {
                        "field": "cumulative_percentage",
                        "type": "quantitative",
                        "axis": {"title": "累计百分比", "orient": "right"}
                    },
                    "color": {"value": "firebrick"}
                }
            },
            {
                "mark": {
                    "type": "point",
                    "filled": False
                },
                "encoding": {
                    "x": {
                        "field": "name",
                        "type": "nominal",
                        "axis": {"title": "排序条件"},
                        "sort": {"field": "cumulative_percentage", "order": "ascending"}  # 确保 x 轴顺序与累计百分比一致
                    },
                    "y": {
                        "field": "cumulative_percentage",
                        "type": "quantitative",
                        "axis": {"title": "累计百分比", "orient": "right"}
                    },
                    "color": {"value": "firebrick"},
                    "text": {
                        "field": "cumulative_percentage",
                        "type": "quantitative",
                        "format": ".1f"
                    }
                },
                "layer": [
                    {
                        "mark": "text",
                        "encoding": {
                            "y": {
                                "field": "cumulative_percentage",
                                "type": "quantitative",
                                "axis": {"title": "累计百分比", "orient": "right"},
                                "offset": 50  # 将数值标签往上移一点
                            },
                            "text": {"field": "cumulative_percentage", "type": "quantitative", "format": ".1f"}
                        }
                    }
                ]
            }
        ],
        "resolve": {
            "scale": {
                "y": "independent"  # 独立的 y 轴
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