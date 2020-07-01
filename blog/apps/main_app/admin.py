from django.contrib import admin

from .models import Article, Category, Comment, UserProfile

class ProfileAdmin(admin.ModelAdmin):
    fields = ['id', 'user', 'bio', 'avatar']
    readonly_fields = ['id', 'user', 'bio', 'avatar']

class ArticleAdmin(admin.ModelAdmin):
    fields = ['article_image', 'article_title', 'article_description', 'article_text', 'pub_date', 'is_main_in_category', 'is_main_in_homepage', 'author', 'category', 'likes']

    readonly_fields = ['likes']

class CommentAdmin(admin.ModelAdmin):
    fields = ['article', 'author', 'comment_text', 'pub_date']

    readonly_fields = ['article', 'author', 'comment_text', 'pub_date']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserProfile, ProfileAdmin)