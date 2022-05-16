from app.utils.page_title import page_title
from sdk.ui.components import (Column, Container, Datatable, collection,
                               documents, format_currency, format_template,
                               is_busy)


def page(COLLECTION_NAME):
    return Container(
        children=[
            page_title('bar-chart', 'Collections'),
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
                grow=0,
                sortable=True,
                searchable=True,
                cell={
                    "_type": "Link",
                    "props": {
                        "href": format_template("https://bscscan.com/address/{{ address }}", {
                            "address": "$.collectionAddress"
                        }),
                        "external": True,
                        "content": {
                            "method": "formatMaskAddress",
                            "params": ["$.collectionAddress"]
                        },
                    }
                }
            ),
            Column(
                id="blockchain",
                title="Chain",
                grow=0
            ),
            Column(
                id="collectionName",
                sortable=True,
                searchable=True,
                title="Collection Name"
            ),
            Column(
                id="volume24h",
                title="Vol 24h",
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
                title="Value 24h",
                sortable=True,
                right=True,
                format=format_currency("$.volume24hUsd", "$.fiatSymbol"),
                grow=0,
                width="120px"
            ),
        ]
    )
