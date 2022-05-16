# https://betterprogramming.pub/how-to-remove-null-none-values-from-a-dictionary-in-python-1bedf1aab5e4
def cleanNullTerms(d):
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = cleanNullTerms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean


def Paragraphs(children, class_name=None):
    return {
        "_type": "Paragraphs",
        "props": cleanNullTerms({
            "class_name": class_name,
            "children": children,
        })
    }


def Fragment(children, class_name=None):
    return {
        "_type": "Fragment",
        "props": cleanNullTerms({
            "className": class_name,
            "children": children,
        })
    }


def Span(content, class_name=None):
    return {
        "_type": "Span",
        "props": cleanNullTerms({
            "className": class_name,
            "content": content,
        })
    }


def Chart(
        title,
        type,
        series,
        data=None,
        height=400,
        busy_when=None,
        options=None,
        class_name=None
):
    return {
        "_type": "Chart",
        "props": cleanNullTerms({
            "className": class_name,
            "title": title,
            "type": type,
            "height": height,
            "busyWhen": busy_when,
            "data": data,
            "series": series,
            "options": options,
        })
    }


def Container(children, class_name=None):
    return {
        "_type": "Container",
        "props": cleanNullTerms({
            "className": class_name,
            "children": children
        })
    }


def Row(children, class_name=None):
    return {
        "_type": "Row",
        "props": cleanNullTerms({
            "className": class_name,
            "children": children
        })
    }


def Div(children, class_name=None, style=None):
    return {
        "_type": "Div",
        "props": cleanNullTerms({
            "className": class_name,
            "children": children,
            "style": style,
        })
    }


def Col(children, class_name=None):
    return {
        "_type": "Col",
        "props": cleanNullTerms({
            "className": class_name,
            "children": children
        })
    }


def Icon(name, class_name=None, size=None):
    return {
        "_type": "Icon",
        "props": cleanNullTerms({
            "className": class_name,
            "name": name,
            "size": size
        })
    }


def Datatable(
    data,
    columns,
    class_name=None,
    busy_when=None,
    show_export=None,
    pagination=None,
    pagination_per_page=None,
    grid_view=None,
    disable_list_view=None,
    default_view=None,
    filters=None,
    default_sort_field_id=None,
    default_sort_asc=None
):
    return {
        "_type": "Datatable",
        "props": cleanNullTerms({
            "busyWhen": busy_when,
            "className": class_name,
            "columns": columns,
            "data": data,
            "defaultSortAsc": default_sort_asc,
            "defaultSortFieldId": default_sort_field_id,
            "defaultView": default_view,
            "disableListView": disable_list_view,
            "filters": filters,
            "gridView": grid_view,
            "pagination": pagination,
            "paginationPerPage": pagination_per_page,
            "showExport": show_export,
        })
    }


def Hr():
    return {
        "_type": "Hr",
        "props": {}
    }


def Badge(color, children, class_name=None):
    return {
        "_type": "Badge",
        "props": cleanNullTerms({
            "children": children,
            "className": class_name,
            "color": color,
        })
    }


def Column(
    id,
    cell=None,
    format=None,
    grow=None,
    omit=None,
    min_width=None,
    right=None,
    searchable=None,
    sortable=None,
    title=None,
    value=None,
    width=None,
):
    return cleanNullTerms({
        "cell": cell,
        "format": format,
        "grow": grow,
        "id": id,
        "minWidth": min_width,
        "omit": omit,
        "right": right,
        "searchable": searchable,
        "sortable": sortable,
        "title": title,
        "value": value,
        "width": width,
    })


def Card(children=None, class_name=None):
    return {
        "_type": "Card",
        "props": cleanNullTerms({
            "children": children,
            "className": class_name
        })
    }


def Form(name, schema, children, class_name=None):
    return {
        "_type": "Form",
        "props": cleanNullTerms({
            "children": children,
            "className": class_name,
            "name": name,
            "schema": schema,
        })
    }


def Select(label, name, options, min_width=None, class_name=None):
    return {
        "_type": "Select",
        "props": cleanNullTerms({
            "className": class_name,
            "label": label,
            "name": name,
            "options": options,
            "minWidth": min_width,
        })
    }


def Button(label, is_submit=None, class_name=None, busyWhen=None):
    return {
        "_type": "Button",
        "props": cleanNullTerms({
            "className": class_name,
            "label": label,
            "isSubmit": is_submit,
            "busyWhen": busyWhen,
        })
    }


def collection(collectionName):
    return collectionName


def documents(collectionName):
    return f'$["{collection(collectionName)}"].*'


def is_busy(collection):
    return f'$..busy[?(@.id=="{collection}")]'


def format_currency(rpc, symbol):
    return {
        "method": "formatCurrency",
        "params": [rpc, symbol]
    }


def selected_currency(event):
    if (event is None):
        return None

    if ("state" not in event.keys()):
        return None

    if ("client" not in event["state"].keys()):
        return None

    if ("selectedCurrency" not in event["state"]["client"].keys()):
        return None

    return event["state"]["client"]["selectedCurrency"]


def form_value(event, form_name, property_name):
    if (event is None):
        return None

    if ("state" not in event.keys()):
        return None

    if ("forms" not in event["state"].keys()):
        return None

    if (form_name not in event["state"]["forms"].keys()):
        return None

    if (property_name not in event["state"]["forms"][form_name].keys()):
        return None

    return event["state"]["forms"][form_name][property_name]


def format_template(template, values):
    return {
        "method": "formatTemplate",
        "params": [template, values]
    }


def switch_case(on, cases):
    return {
        "method": "switchCase",
        "params": [on, cases]
    }


def commify(value):
    return {
        "method": "commify",
        "params": [value]
    }


def json_array(values):
    return {
        "method": "jsonArray",
        "params": [values]
    }


def ekp_map(source, projection):
    return {
        "method": "map",
        "params": [source, projection]
    }


def sort_by(source, comparator):
    return {
        "method": "sortBy",
        "params": [source, comparator]
    }


def format_percent(value):
    return {
        "method": "formatPercent",
        "params": [value]
    }


def Image(src, style=None, class_name=None):
    return {
        "_type": "Image",
        "props": cleanNullTerms({
            "src": src,
            "style": style,
            "className": class_name
        })
    }
