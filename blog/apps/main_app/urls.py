from django.urls import path

from . import views

app_name = 'main_app'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('profile/', views.profile, name = 'loadArticles'),
    path('loadArticles/', views.loadArticles, name = 'loadArticles'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logoutUser, name = 'logoutUser'),
    path('register/', views.register, name = 'register'),
    path('loadComments/', views.loadComments, name = 'loadComments'),
    path('category/', views.category, name = 'category'),
    path('article/', views.article, name = 'article'),
    path('article/<int:article_id>/leave_comment/', views.leave_comment, name = 'leave_comment')
]