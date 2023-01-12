from django.shortcuts import render
from django.http import Http404

import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, name):
    mkdown = util.get_entry(name)

    if not mkdown:
        raise Http404('The requested page was not found.')

    html = markdown2.markdown(mkdown)

    # return render(request, f'encyclopedia/{name}.html', {"name": name})
    return render(request, 'encyclopedia/entry.html', {"html": html})
