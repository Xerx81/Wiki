from django.shortcuts import render
from markdown2 import Markdown
from random import choice

from . import util

# Function Convert md file content to html
def md_to_html(title):
    md_cont = util.get_entry(title)
    markdowner = Markdown()

    if md_cont:
        return markdowner.convert(md_cont)
    else: 
        return None

# Render index page with list of all entries title
def index(request):
    return render(request, "encyclopedia/index.html", {
        "header": "All Pages",
        "entries": util.list_entries()
    })

def entry(request, title):
    html_cont = md_to_html(title)

    # Show error if page doesn't exists
    if html_cont == None:
        return render(request, "encyclopedia/error.html", {
            "error": "<h1>404<h1> <h4>page not found<h4>"
        })
    
    # Render content if page exists
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "content": html_cont
    })
    

def search(request):
    if request.method == "POST":
        q = request.POST['q']
        html_cont = md_to_html(q)

        # Redirect to the content page if title exists
        if html_cont:
            return render(request, "encyclopedia/page.html", {
                "title": q,
                "content": html_cont
            })
        
        # Recommend entries based on characters typed by user
        else:
            entries = util.list_entries()
            new_list = []

            # Enter the entries to new_list if it matched the text typed by user
            for entry in entries:
                if q.lower() in entry.lower():
                    new_list.append(entry)

            # If no matches found show 'no results'
            if not new_list:
                return render(request, "encyclopedia/index.html", {
                "header": "Search Results",
                "error": "No results"
            })

            # If matches found then show user the matched results
            return render(request, "encyclopedia/index.html", {
                "header": "Search Results",
                "entries": new_list
            })
        
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        # Return error if title already exists
        check_title = util.get_entry(title)
        if check_title:
            return render(request, "encyclopedia/error.html", {
                "error": "<h1>400</h1> <p>Entry already exists<p>"
            })
        
        # Save entry and redirect to that entry page 
        else:
            util.save_entry(title, content)
            return entry(request, title)

    return render(request, "encyclopedia/create.html")

def edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    
def save(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        # Save entry and redirect to that entry page 
        util.save_entry(title, content)
        return entry(request, title)

    return render(request, "encyclopedia/edit.html")

def rand(request):
    entries = util.list_entries()
    rand_entry = choice(entries)

    return entry(request, rand_entry)