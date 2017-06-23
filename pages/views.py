from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseNotFound, HttpResponseServerError

# Create your views here.
"""
    Renders the required html page
    Input: s: request object
    output: Redirect object returned by render() and Httpresponse() functions.    
"""

def index(req):
    return render(req, "pages/index.html")

def about(req):
    return render(req, "pages/about.html")

def contact(req):
    return render(req, "pages/contact.html")

def info(req):
    return render(req, "pages/info.html")

def downloads(req):
    return render(req, "pages/downloads.html")

def theory(req):
    return render(req, "pages/theory.html")

def procedure(req):
    return render(req, "pages/procedure.html")

def experiments(req):
    return render(req, "pages/experiments.html")

def feedback(req):
    return render(req, "pages/feedback.html") 

def quiz(req):
    return render(req, "pages/quiz.html")   

def e404(req):
    return HttpResponseNotFound(render_to_string('pages/e404.html'))

def e500(req):
    return HttpResponseServerError(render_to_string('pages/e500.html'))
