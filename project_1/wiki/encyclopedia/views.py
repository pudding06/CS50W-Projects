from django.shortcuts import render
import markdown

from . import util

def convert_md_html(title):
    # get markdown data
    md = util.get_entry(title)
    # Check if the file exist
    if md == None:
        return None
    # Returns hmtl code
    markdowner = markdown.Markdown()
    return markdowner.convert(md)

def get_all_entries():
    '''
    Returns a list of dict with keys "title" and "url"
    '''
    titles = util.list_entries()
    urls = []
    for title in titles:
        urls.append("http://127.0.0.1:8000/wiki/" + title)
    data = []
    for i in range(len(titles)):
        d = dict()
        d["title"] = titles[i]
        d["url"] = urls[i]
        data.append(d)
    return data


def index(request):
    data = get_all_entries()
    return render(request, "encyclopedia/index.html", {
        "data": data
    })

def wiki(request, title):
    html_content = convert_md_html(title)
    if html_content == None:
        return render(request, "encyclopedia/error.html", {"message": f"Error {title} does not exist"})
    else:
        return render(request, "encyclopedia/markdown.html",
                      {"title": title, "html_content": html_content})
    
def search(request):
    if request.method == "POST":
        user_search = request.POST.get('q')
        html_content = convert_md_html(user_search)
        if html_content is not None:
            return render(request, "encyclopedia/markdown.html",
                {"title": user_search, "html_content": html_content})
        else:
            recommended = []
            entries = util.list_entries()
            for entry in entries:
                if user_search.lower() in entry.lower():
                    recommended.append(entry)
            print(recommended)
            urls = []
            for entry in recommended:
                urls.append("http://127.0.0.1:8000/wiki/" + entry)
            data = []
            for i in range(len(recommended)):
                d = dict()
                d["title"] = recommended[i]
                d["url"] = urls[i]
                data.append(d)
            return render(request, "encyclopedia/search.html", {"data": data})
        
def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        text = request.POST.get("text")
        entries = util.list_entries()
        if title in entries:
            return render(request, "encyclopedia/error.html",{
                "message": f"Entry {title} already exists"
            })
        else:
            util.save_entry(title, text)
            return render(request, "encyclopedia/markdown.html",
                {"title": title, "html_content": convert_md_html(title)})
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")