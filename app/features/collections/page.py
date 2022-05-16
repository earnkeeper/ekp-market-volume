from app.utils.page_title import page_title
from ekp_sdk.ui import (Chart, Col, Column, Container, Datatable, Image, Link,
                        Row, collection, documents, ekp_map, format_currency,
                        format_mask_address, format_template, is_busy,
                        json_array, sort_by)


def page(COLLECTION_NAME):
    return Container(
        children=[
            page_title('bar-chart', 'Market Volumes'),
            tableRow(COLLECTION_NAME)
        ]
    )


def tableRow(COLLECTION_NAME):
    return Datatable(
        class_name="mt-1",
        data=documents(COLLECTION_NAME),
        busy_when=is_busy(collection(COLLECTION_NAME)),
        default_sort_field_id="volume24hUsd",
        default_sort_asc=False,
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
                title="24h Volume",
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
                title="7d Volume",
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
                    ['$.timestamp_ms', '$.volume_usd'],
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
