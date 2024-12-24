

def Get_Chart_Style(data_frame):
    chart_style = {
            "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
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
                        "sort": {"field": "error_count","order": "descending"}
                        },
                        "y": {
                        "field": "error_count",
                        "type": "quantitative",
                        "axis": {"title": "错误数","orient": "left"}
                        },
                        "color": {"value": "#172D44"}
                    }
                    },
                    {
                    "mark": "text",
                    "encoding": {
                        "x": {
                        "field": "name",
                        "type": "nominal",
                        "sort": {"field": "error_count","order": "descending"}
                        },
                        "y": {
                        "field": "error_count",
                        "type": "quantitative",
                        "axis": None
                        },
                        "yOffset": {"value": 20},
                        "color": {"value": "#F3E5BB"},
                        "size": {"value": 20},
                        "text": {"field": "error_count"}
                    }
                    },
                    {
                    "mark": {"type": "line","point": {"filled": True}},
                    "encoding": {
                        "x": {
                        "field": "name",
                        "type": "nominal",
                        "sort": {
                            "field": "cumulative_percentage",
                            "order": "ascending"
                        }
                        },
                        "y": {
                        "field": "cumulative_percentage",
                        "type": "quantitative",
                        "axis": {"title": "累计百分比,%","orient": "right"}
                        },
                        "color": {"value": "#CA443C"}
                    }
                    },
                    {
                    "mark": "text",
                    "encoding": {
                        "x": {
                        "field": "name",
                        "type": "nominal",
                        "sort": {
                            "field": "cumulative_percentage",
                            "order": "ascending"
                        }
                        },
                        "y": {
                        "field": "cumulative_percentage",
                        "type": "quantitative",
                        "axis": None
                        },
                        "text": {
                        "field": "cumulative_percentage",
                        "type": "quantitative",
                        "format": ".0%"
                        },
                        "yOffset": {"value": -10},
                        "size": {"value": 20},
                        "color": {"value": "#CA443C"}
                    }
                    }
                ],
                "resolve": {"scale": {"y": "independent"}}
                }
    return chart_style
