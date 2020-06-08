# TODO: Make like button
# TODO: Make authorization
# TODO: Customizate admin panel

import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from django.utils import timezone

from .models import Category, Article, Comment

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
    articles     = Article.objects.filter(category_id = id).order_by('-likes')[:9]
    
    try:
        main_article = Article.objects.get(category_id = id, is_main_in_category = True)    
    except Article.DoesNotExist:
        main_article = None
    
    return render(req, 'pages/category.html', { 'categories': categories, 'articles': articles, 'main_article': main_article, 'current_cat': current_cat, 'category_id': int(id) })

def loadArticles(req):
    count = req.GET.get('count', 10)
    id    = req.GET.get('id')
    count = int(count)

    if id is not None:
        id = int(id)
        popular_articles = Article.objects.filter(is_main_in_category=False, category_id = id).order_by('-likes')[count:count+9]
    else:
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

def article(req):
    id         = req.GET.get('id')
    categories = Category.objects.all()
   
    try:
        article = Article.objects.get(id = id)
    except:
        raise Http404('Статья не найдена')

    latest_comments_list = article.comment_set.order_by('-id')[:10]
    
    article.article_text = parseArticleText(article.article_text)
    return render(req, 'pages/article.html', { 'article': article, 'categories': categories, 'category_id': article.category_id, 'comments': latest_comments_list })

def leave_comment(req, article_id):
    try:
        a = Article.objects.get(id = article_id)
    except:
        raise Http404("Статья не найдена")

    data = json.loads(req.body)
    
    c = a.comment_set.create(author_name = 'No name', comment_text = data['text'], pub_date = timezone.now())

    comment                = {}
    comment["id"]          = c.id
    comment["author_name"] = c.author_name
    comment["pub_date"]    = c.pub_date.strftime("%d %B %Y %H:%M")
    comment["text"]        = c.comment_text

    context = json.dumps(comment)

    return HttpResponse(context, content_type="application/json")

def loadComments(req):

    count = req.GET.get('count', 10)
    count = int(count)

    latest_comments = Comment.objects.order_by('-id')[count:count+10]

    response_data = []

    for c in latest_comments:
        comment                = {}
        comment["id"]          = c.id
        comment["author_name"] = c.author_name
        comment["pub_date"]    = c.pub_date.strftime("%d %B %Y %H:%M")
        comment["text"]        = c.comment_text

        response_data.append(comment)

    context = json.dumps(response_data)

    return HttpResponse(context, content_type="application/json")

def parseArticleText(text):

    lines = text.splitlines()

    return "\n".join('<p>'+i+'</p>' for i in lines)