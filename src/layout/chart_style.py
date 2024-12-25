# Copyright (C) 2024  ThisWaySir

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Additionally, we encourage all users to review the full license agreement to fully understand their rights and obligations. For more information about the GNU General Public License, please visit:
# - Chinese: [GNU Official Website - GNU GPLv3 Chinese](https://www.gnu.org/licenses/quick-guide-gplv3.zh-cn.html)
# - English: [GNU Official Website - GNU GPLv3 English](https://www.gnu.org/licenses/gpl-3.0.en.html)

# Thank you for supporting the open source community and the free software movement!

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
                        "sort": {"field": "error_count", "order": "descending"}
                    },
                    "y": {
                        "field": "error_count",
                        "type": "quantitative",
                        "axis": {"title": "错误数", "orient": "left"}
                    },
                    "color": {"value": "#6BAED6"}
                }
            },
            {
                "mark": "text",
                "encoding": {
                    "x": {
                        "field": "name",
                        "type": "nominal",
                        "sort": {"field": "error_count", "order": "descending"}
                    },
                    "y": {
                        "field": "error_count",
                        "type": "quantitative",
                        "axis": None
                    },
                    "yOffset": {"value": 20},
                    "color": {"value": "#08306B"},
                    "size": {"value": 20},
                    "text": {"field": "error_count"}
                }
            },
            {
                "mark": {"type": "line", "point": {"filled": True}},
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
                        "axis": {"title": "累计百分比, ×100%", "orient": "right"}
                    },
                    "color": {"value": "#D95319"}
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
                        "format": ".1%" 
                    },
                    "yOffset": {"value": -10},
                    "size": {"value": 16},
                    "color": {"value": "#D95319"}
                }
            }
        ],
        "resolve": {"scale": {"y": "independent"}}
    }
    return chart_style