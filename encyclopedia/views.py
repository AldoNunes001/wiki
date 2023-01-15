from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse

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
    return render(request, 'encyclopedia/entry.html', {"html": html, 'entry': name})


def search(request):
    query = util.get_entry(request.GET['q'])

    if query:
        html = markdown2.markdown(query)
        return render(request, 'encyclopedia/entry.html', {"html": html})

    entries = util.list_entries()
    # print(entries)
    results = []

    for entry in entries:
        if request.GET['q'].lower() in entry.lower():
            results.append(entry)

    return render(request, "encyclopedia/search.html", {'results': results, 'number': len(results), 'q': request.GET['q']})


def new_page(request):
    if request.method == 'POST':
        # print(request.POST)
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if not title or not content:
            error = "Error. Title and content are required fields."
            return render(request, "encyclopedia/new_page.html", {'error': error, 'title': title, 'content': content})

        if util.get_entry(title):
            error = "Error. This entry already exists."
            return render(request, "encyclopedia/new_page.html", {'error': error, 'title': title, 'content': content})

        util.save_entry(title, content)
        # entry = util.get_entry(title)
        # html = markdown2.markdown(entry)

        return HttpResponseRedirect(reverse('encyclopedia:entry_page', args=[title]))

    return render(request, "encyclopedia/new_page.html")


def edit_page(request, entry):
    if request.method == 'POST':
        # print(request.POST)
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if not title or not content:
            error = "Error. Title and content are required fields."
            return render(request, "encyclopedia/edit_page.html", {'error': error, 'title': title, 'content': content})

        util.save_entry(title, content)

        return HttpResponseRedirect(reverse('encyclopedia:entry_page', args=[title]))

    title = entry
    content = util.get_entry(title)

    return render(request, "encyclopedia/edit_page.html", {'title': title, 'content': content})
