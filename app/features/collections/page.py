from app.utils.page_title import page_title
from ekp_sdk.ui import (Chart, Col, Column, Container, Datatable, Image, Link,
                        Row, collection, commify, documents, ekp_map,
                        format_currency, format_mask_address, format_template,
                        is_busy, json_array, sort_by, navigate)


def page(TABLE_COLLECTION_NAME, CHART_COLLECTION_NAME):
    return Container(
        children=[
            page_title('bar-chart', 'Market Volumes'),
            chart_row(CHART_COLLECTION_NAME),
            table_row(TABLE_COLLECTION_NAME)
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
            # "dataLabels": {
            #     "enabled": False,
            # },
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
                    "$.timestamp_ms"
                ), "$.timestamp_ms"
            ),
            "stroke": {
                "width": [4, 4],
                "curve": 'smooth',
            }
        },
        series=[
            {
                "name": "Sales Count",
                "type": "column",
                "data": ekp_map(
                    sort_by(
                        json_array(documents(CHART_COLLECTION_NAME)),
                        "$.timestamp_ms"),
                    "$.volume"
                )
            },
            {
                "name": "Sales Value",
                "type": "line",
                "data": ekp_map(
                    sort_by(
                        json_array(documents(CHART_COLLECTION_NAME)),
                        "$.timestamp_ms"
                    ),
                    "$.volume_fiat"
                ),
            },
        ],

    )


def table_row(TABLE_COLLECTION_NAME):
    return Datatable(
        class_name="mt-1",
        data=documents(TABLE_COLLECTION_NAME),
        busy_when=is_busy(collection(TABLE_COLLECTION_NAME)),
        default_sort_field_id="volume24h",
        default_sort_asc=False,
        on_row_clicked=navigate(
            location=format_template(
                "collection/{{ address }}",
                {"address": "$.collectionAddress"}
            ),
            new_tab=True
        ),
        columns=[
            Column(
                id="collectionAddress",
                title="Address",
                width="180px",
                sortable=True,
                searchable=True,
                cell=Row(
                    children=[
                        Col(
                            class_name="col-auto pr-0",
                            children=[
                                Image(
                                    src="https://cryptologos.cc/logos/history/bnb-bnb-logo.svg?v=001",
                                    style={"width": "16px"}
                                )
                            ]
                        ),
                        Col(
                            class_name="col-auto",
                            children=[
                                Link(
                                    href=format_template("https://bscscan.com/address/{{ address }}", {
                                        "address": "$.collectionAddress"
                                    }),
                                    external=True,
                                    externalIcon=True,
                                    content=format_mask_address(
                                        "$.collectionAddress")
                                )
                            ]
                        )
                    ]
                )
            ),
            Column(
                id="collectionName",
                sortable=True,
                searchable=True,
                title="Collection Name"
            ),
            Column(
                id="volume24h",
                title="24h Sales",
                right=True,
                sortable=True,
                format={
                    "method": "commify",
                    "params": ["$.volume24h"]
                },
                width="120px"
            ),
            Column(
                id="volume24hUsd",
                title="24h Value",
                sortable=True,
                right=True,
                format=format_currency("$.volume24hUsd", "$.fiatSymbol"),
                width="140px"
            ),
            Column(
                id="volume7d",
                title="7d Sales",
                right=True,
                sortable=True,
                format={
                    "method": "commify",
                    "params": ["$.volume7d"]
                },
                width="100px"
            ),
            Column(
                id="volume7dUsd",
                title="7d Value",
                sortable=True,
                right=True,
                format=format_currency("$.volume7dUsd", "$.fiatSymbol"),
                width="140px"
            ),
            Column(
                id="chart7d",
                title="",
                width="180px",
                cell=chart_cell('$.chart7d.*')
            ),
        ]
    )


def chart_cell(path):
    return Chart(
        title="",
        card=False,
        type='line',
        height=90,
        series=[
            {
                "name": 'All',
                "data": ekp_map(
                    sort_by(
                        json_array(path),
                        '$.timestamp',
                    ),
                    ['$.timestamp_ms', '$.volume'],
                ),
            },
        ],
        data=path,
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
            "markers": {
                "size": 0
            },
            "stroke": {
                "width": 3,
                "curve": "smooth"
            },
            "grid": {
                "show": False,
            },
            "dataLabels": {
                "enabled": False,
            },
            "xaxis": {
                "axisBorder": {"show": False},
                "axisTicks": {"show": False},
                "type": "datetime",
                "labels": {
                    "show": False
                },
            },
            "yaxis": {
                "labels": {
                    "show": False
                },
            },
        }
    )
