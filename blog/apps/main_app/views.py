# TODO: Make like button
# TODO: Make article page
# TODO: Make commentaries
# TODO: Make authorization
import json

from django.shortcuts import render
from django.http import HttpResponse

from .models import Category, Article

def index(req):
    categories          = Category.objects.all()
    main_articles       = Article.objects.filter(is_main_in_homepage=True).order_by('likes') # Get three main articles and order by likes
    main_articles_array = main_articles[1:]

    popular_articles = Article.objects.order_by('-likes')[:10]
    return render(req, 'pages/index.html', { 'categories': categories, 'main_article': main_articles[0], 'articles': popular_articles, 'main_articles': main_articles_array })

def category(req):
    categories   = Category.objects.all()
    id           = req.GET.get('id')
    current_cat  = Category.objects.get(category_no = id)
    articles     = Article.objects.filter(category_id = id).order_by('-likes')[:10]
    main_article = Article.objects.get(category_id = id, is_main_in_category = True)
    
    return render(req, 'pages/category.html', { 'categories': categories, 'articles': articles, 'main_article': main_article, 'current_cat': current_cat })

def loadArticles(req):
    count = req.GET.get('count', 10)
    count = int(count)

    popular_articles = Article.objects.filter(is_main_in_homepage=False).order_by('-likes')[count:count+10]

    response_data = []

    for a in popular_articles:
        article                = {}
        article["id"]          = a.id
        article["img"]         = a.article_image.url
        article["title"]       = a.article_title
        article["desc"]        = a.article_description
        article["author_name"] = a.author_name
        article["date"]        = a.pub_date.strftime("%d %B %Y %H:%M")
        article["category"]    = a.category.name
        article["category_no"] = a.category.category_no
        article["likes"]       = a.likes

        response_data.append(article)

    context = json.dumps(response_data)

    return HttpResponse(context, content_type="application/json")