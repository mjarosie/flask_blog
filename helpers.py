from flask import render_template, request


def object_list(template_name, query, paginate_by=2, **context):
    """List the objects from query in given template, paginate by given number of entries.
    Shows the first page by default.

    :param template_name: Template for the query to be listed in.
    :param query: Items to be displayed.
    :param paginate_by: Number of items per page.
    :param context: Additional context of the template.
    :return: None
    """

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1
    object_list_paginated = query.paginate(page, paginate_by)
    return render_template(template_name, object_list=object_list_paginated, **context)
