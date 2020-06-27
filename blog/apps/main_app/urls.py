from django.urls import path

from . import views

app_name = 'main_app'
urlpatterns = [
    path('', views.index, name = 'index'),

    path('profile/', views.profile, name = 'profile'),
    path('profile/edit', views.edit_profile, name = 'edit_profile'),
    path('profile/save', views.update_profile, name = 'update_profile'),

    path('login/', views.login, name = 'login'),
    path('logout/', views.logoutUser, name = 'logoutUser'),
    path('register/', views.register, name = 'register'),

    path('category/', views.category, name = 'category'),
    path('article/', views.article, name = 'article'),
    path('loadArticles/', views.loadArticles, name = 'loadArticles'),

    path('article/<int:article_id>/leave_comment/', views.leave_comment, name = 'leave_comment'),
    path('loadComments/', views.loadComments, name = 'loadComments'),
    path('deleteComment/', views.deleteComment, name = 'deleteComment')
]