# TODO Create new pages for other categories
from django.shortcuts import render

from .models import Category, Article

def index(req):
    categories          = Category.objects.all()
    main_articles       = Article.objects.filter(is_main_in_homepage=True).order_by('likes') # Get three main articles and order by likes
    main_articles_array = main_articles[1:]

    popular_articles = Article.objects.order_by('-likes')[:10]
    return render(req, 'pages/index.html', { 'categories': categories, 'main_article': main_articles[0], 'articles': popular_articles, 'main_articles': main_articles_array })