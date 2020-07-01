# TODO: Make like button
# TODO: Customizate admin panel
# TODO: Make ability to create, update and delete articles

import json

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from django.utils import timezone

from .models import Category, Article, Comment, UserProfile

from .forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django import forms

def index(req):

    categories          = Category.objects.all()
    main_articles       = Article.objects.filter(is_main_in_homepage=True).order_by('likes') # Get three main articles and order by likes
    main_articles_array = main_articles[1:]

    popular_articles = Article.objects.order_by('-likes')[:10]

    context = {
        'categories': categories,
        'main_article': main_articles[0],
        'articles': popular_articles, 
        'main_articles': main_articles_array
    }

    if req.user.is_authenticated:
        profile = UserProfile.objects.get(user = req.user)
        context['profile'] = profile

    return render(req, 'pages/index.html', context)

def category(req):

    categories   = Category.objects.all()
    id           = req.GET.get('id')
    current_cat  = Category.objects.get(category_no = id)
    articles     = Article.objects.filter(category_id = id).order_by('-likes')[:9]
    
    try:
        main_article = Article.objects.get(category_id = id, is_main_in_category = True)    
    except Article.DoesNotExist:
        main_article = None
    
    context = {
        'categories': categories, 
        'articles': articles, 
        'main_article': main_article, 
        'current_cat': current_cat, 
        'category_id': int(id)
    }

    if req.user.is_authenticated:
        profile = UserProfile.objects.get(user = req.user)
        context['profile'] = profile

    return render(req, 'pages/category.html', context)

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
        article["author_name"] = a.author.user.username
        article["author_id"]   = a.author.id
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
        article        = Article.objects.get(id = id)
        profile        = UserProfile.objects.get(id = article.author.id)
    except:
        raise Http404('Статья не найдена')

    latest_comments_list = article.comment_set.order_by('-id')[:10]
    comment_count        = article.comment_set.count()
    
    article.article_text = parseArticleText(article.article_text)

    context = {
        'article': article, 
        'categories': categories, 
        'category_id': article.category_id, 
        'comments': latest_comments_list, 
        'author_profile': profile,
        'comment_count': comment_count
    }

    if req.user.is_authenticated:
        currentProfile = UserProfile.objects.get(user = req.user)
        context['profile'] = currentProfile

    return render(req, 'pages/article.html', context)


def profile(req):

    id      = req.GET.get('id')
    profile = UserProfile.objects.get(user = req.user)

    try:
        user_profile = UserProfile.objects.get(id = id)
    except:
        raise Http404('Пользователь не найден')

    last_articles = Article.objects.filter(author = user_profile).order_by('-pub_date')
    last_comments = Comment.objects.filter(author = user_profile).order_by('-pub_date')

    if (last_articles):
        last_articles = last_articles[0:8]

    if (last_comments):
        last_comments = last_comments[0:4]

    return render(req, 'user/profile.html', {'lastArticles': last_articles, 'lastComments': last_comments, 'profile': profile, 'load_profile': user_profile})

@login_required
def edit_profile(req):

    profile = UserProfile.objects.get(user = req.user)

    if req.method == 'POST':

        u_form = UserUpdateForm(req.POST, instance = req.user)
        p_form = ProfileUpdateForm(req.POST, req.FILES, instance = profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(req, 'Ваш аккаунт обновлен')
            return redirect('/profile/edit')

    else:
        u_form = UserUpdateForm(instance = req.user)
        p_form = ProfileUpdateForm(instance = profile)

    context = {'u_form': u_form, 'p_form': p_form, 'profile': profile}

    return render(req, 'user/edit.html', context)


def leave_comment(req, article_id):

    if req.user.is_authenticated:

        try:
            a = Article.objects.get(id = article_id)
        except:
            raise Http404("Статья не найдена")

        data = json.loads(req.body)
        profile = UserProfile.objects.get(user = req.user)
        
        c = a.comment_set.create(author = profile, comment_text = data['text'], pub_date = timezone.now())

        comment                = {}
        comment["id"]          = c.id
        comment["image"]       = c.author.avatar.url
        comment["author_name"] = c.author.user.username
        comment["author_id"]   = c.author.user.id
        comment["show-delete"] = True
        comment["pub_date"]    = c.pub_date.strftime("%d %B %Y %H:%M")
        comment["text"]        = c.comment_text

        context = json.dumps(comment)

        return HttpResponse(context, content_type="application/json")

    else:
        jsonr = json.dumps({ 'authenticated': False })
        return HttpResponse(jsonr, content_type="application/json")

def loadComments(req):

    count = req.GET.get('count', 10)
    count = int(count)

    latest_comments = Comment.objects.order_by('-id')[count:count+10]

    response_data = []

    for c in latest_comments:
        comment                = {}
        comment["id"]          = c.id
        comment["image"]       = c.author.avatar.url
        comment["author_name"] = c.author.user.username
        comment["author_id"]   = c.author.user.id
        comment["pub_date"]    = c.pub_date.strftime("%d %B %Y %H:%M")
        comment["text"]        = c.comment_text

        if c.author.user == req.user:
            comment["show-delete"] = True
        else:
            comment["show-delete"] = False

        response_data.append(comment)

    context = json.dumps(response_data)

    return HttpResponse(context, content_type="application/json")

def deleteComment(req):

    id = req.GET.get('id')

    Comment.objects.filter(id = id).delete()

    jsonr = json.dumps({ 'deleted': True })
    return HttpResponse(jsonr, content_type="application/json")


def login(req):

    if req.user.is_authenticated:
        return redirect('/')
    else:
        context = {}

        if req.method == 'POST':
            username = req.POST["username"]
            password = req.POST["password"]

            user = authenticate(req, username=username, password=password) # Get user from db

            if user is not None:
                auth_login(req, user)
                return redirect('/')
            else:
                messages.info(req, 'Имя пользователя или пароль неправильные')
                return render(req, 'pages/login.html', context)

        return render(req, 'pages/login.html', context)

def logoutUser(req):
    logout(req)
    return redirect('/')

def register(req):
    if req.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm(use_required_attribute=False)

        if req.method == 'POST':
            form = CreateUserForm(req.POST) # Create new form to check validation
            if form.is_valid():
                user = form.save() # Create new User
                UserProfile.objects.create(id = user.id, user = user) # Create Profile for new User
                username = form.cleaned_data.get('username')
                auth_login(req, user)
                return redirect('/profile/edit')

        context = {'form': form}
        return render(req, 'pages/register.html', context)

# TODO: Move to another .py file
def parseArticleText(text):

    lines = text.splitlines()

    return "\n".join('<p>'+i+'</p>' for i in lines)