# TODO Create new pages for other categories
from django.shortcuts import render

from .models import Category

def index(req):
    categories = Category.objects.all()
    return render(req, 'pages/index.html', { 'categories': categories })