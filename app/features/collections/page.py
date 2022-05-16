from app.utils.page_title import page_title
from sdk.components.components import Container


def page(COLLECTION_NAME):
    return Container(
        children=[
            page_title('bar-chart', 'Collections'),
        ]
    )
