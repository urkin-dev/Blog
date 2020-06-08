from django.urls import path

from . import views

app_name = 'main_app'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('loadArticles/', views.loadArticles, name = 'loadArticles'),
    path('loadComments/', views.loadComments, name = 'loadComments'),
    path('category/', views.category, name = 'category'),
    path('article/', views.article, name = 'article'),
    path('article/<int:article_id>/leave_comment/', views.leave_comment, name = 'leave_comment')
]