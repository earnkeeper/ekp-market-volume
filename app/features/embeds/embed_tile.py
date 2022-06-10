from ekp_sdk.ui import (Chart, Col, Div, Image, Link, Row, Span, commify,
                        ekp_map, format_currency, format_template, sort_by, json_array)


def embed_tile():
    return Div(
        context="$.data[0]",
        children=[
            Row(
                [
                    chart_row,
                    Col(
                        "col-12 px-2",
                        [
                            Div(
                                style={"marginTop": "-12px"},
                                children=[
                                    Row(
                                        [
                                            name_row,
                                            details_row,
                                            source_row
                                        ]
                                    )

                                ]
                            ),

                        ]
                    )
                ],
                "p-0"
            )
        ]
    )


name_row = Col(
    "col-12",
    [
        Span(
            format_template("{{ rank }}. {{ name }}", {
                "rank": "$.rank",
                "name": "$.name"
            }),
            "text-primary"
        )
    ]
)

details_row = Col(
    "col-12",
    [
        Row(
            class_name="mt-1",
            children=[
                Col(
                    "col-5",
                    [
                        Span("24 Hr Sales", "d-block font-small-3"),
                        Span("$.sales24h", "d-block font-small-2"),
                    ]
                ),
                Col(
                    "col-5",
                    [
                        Span("24 Hr Volume", "d-block font-small-3"),
                        Span(
                            format_currency("$.volume24h", "$.fiatSymbol"),
                            "d-block font-small-2"
                        ),
                    ]
                ),
                Col(
                    "col-2 my-auto",
                    [
                        Image(
                            src="https://cryptologos.cc/logos/history/bnb-bnb-logo.svg?v=001",
                            style={"height": "24px"}
                        )
                    ]
                ),


            ]
        )
    ]
)

source_row = Col(
    "col-12",
    [
        Div([], style={"height": "4px"}),
        Row([
            Col(
                "col-auto pr-0",
                [
                    Image(
                        src="https://market-volume.ekp.earnkeeper.io/static/tofu.png",
                        style={"height": "12px"}
                    )
                ]
            ),
            Col(
                "col-auto px-0",
                [
                    Div([], style={"width": "8px"})
                ]
            ),
            Col(
                "col-auto pl-0 my-auto",
                [
                    Span("Source Tofu NFT", "font-small-1")
                ]
            )
        ])
    ]
)

chart_row = Col(
    "col-12 px-0",
    [
        Div(
            style={"marginRight": "-13px"},
            children=[
                Chart(
                    title="",
                    height=174,
                    type="line",
                    data="$.chart30d.*",
                    card=False,
                    options={
                        "legend": {
                            "show": False
                        },
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
                            "labels": {"show": False}
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
                                    "$.chart30d.*"
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
                            "name": "Sales",
                            "type": "column",
                            "data": ekp_map(
                                    sort_by(
                                        json_array("$.chart30d.*"),
                                        "$.timestamp_ms"),
                                    "$.sales"
                            )
                        },
                        {
                            "name": "Volume",
                            "type": "line",
                            "data": ekp_map(
                                    sort_by(
                                        json_array("$.chart30d.*"),
                                        "$.timestamp_ms"
                                    ),
                                "$.volume"
                            ),
                        },
                    ],
                )
            ]),

    ]
)
