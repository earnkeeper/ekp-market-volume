from ekp_sdk.ui import Col, Icon, Row, Span


def page_title(icon, title):
    return Row(
        children=[
            Col(
                class_name='col-auto pr-0 my-auto',
                children=[
                    Icon(
                        size="lg",
                        name=icon
                    )
                ],
            ),
            Col(
                class_name="my-auto",
                children=[
                    Span(title, "font-large-1")
                ]
            ),
        ],
        class_name="mb-2"
    )
