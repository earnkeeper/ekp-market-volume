from app.utils.page_title import page_title
from ekp_sdk.ui import (Chart, Col, Column, Container, Datatable, Image, Link,
                        Row, Span, collection, commify, documents, ekp_map,
                        format_currency, format_mask_address, format_template,
                        Div,
                        is_busy, json_array, sort_by)


def page(TABLE_COLLECTION_NAME, CHART_COLLECTION_NAME):
    return Container(
        children=[
            page_title('bar-chart', f'$.{CHART_COLLECTION_NAME}[0].name'),
            Link(
                href=format_template("https://bscscan.com/address/{{ address }}", {
                    "address": f"$.{CHART_COLLECTION_NAME}[0].address"
                }),
                external=True,
                externalIcon=True,
                content=f'$.{CHART_COLLECTION_NAME}[0].address'
            ),
            Div(class_name="d-block mb-2", children=[]),
            chart_row(CHART_COLLECTION_NAME),
        ]
    )


def chart_row(CHART_COLLECTION_NAME):
    return Chart(
        title="",
        height=200,
        type="line",
        data=documents(CHART_COLLECTION_NAME),
        options={
            "chart": {
                "zoom": {
                    "enabled": False,
                },
                "toolbar": {
                    "show": False,
                },
                "stacked": False,
                "type": "line"
            },
            "xaxis": {
                "type": "datetime",
            },
            "yaxis": [
                {
                    "labels": {
                        "show": False,
                        "formatter": commify("$")
                    },
                },
                {
                    "labels": {
                        "show": False,
                        "formatter": commify("$")
                    },
                    "opposite": True,
                },
            ],
            "labels": ekp_map(
                sort_by(
                    json_array(
                        documents(CHART_COLLECTION_NAME)
                    ),
                    "$.timestampMs"
                ), "$.timestampMs"
            ),
            "stroke": {
                "width": [4, 4],
                "curve": 'smooth',
            }
        },
        series=[
            {
                "name": "Sales",
                "type": "column",
                "data": ekp_map(
                    sort_by(
                        json_array(documents(CHART_COLLECTION_NAME)),
                        "$.timestampMs"),
                    "$.volume"
                )
            },
            {
                "name": "Volume",
                "type": "line",
                "data": ekp_map(
                    sort_by(
                        json_array(documents(CHART_COLLECTION_NAME)),
                        "$.timestampMs"
                    ),
                    "$.volumeFiat"
                ),
            },
        ],

    )
