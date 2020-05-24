import datetime
from django.db import models
from django.utils import timezone

class Category(models.Model):
    category_no   = models.IntegerField('Номер категории', primary_key=True)
    name          = models.CharField('Название категории', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Article(models.Model):
    article_image       = models.ImageField(upload_to='img/articles', max_length=100, default='img/default/default.jpg')
    article_title       = models.CharField('Название статьи', max_length = 30)
    article_description = models.CharField('Краткое описание статьи', max_length = 45)
    article_text        = models.TextField('Текст статьи')
    pub_date            = models.DateTimeField('Дата публикации')
    is_main_article     = models.BooleanField('Главная статья(всего 3 места)', default=False)
    author_name         = models.CharField('Логин автора', max_length=50, default="No name")
    category            = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, db_column='category_no', default=0)
    likes               = models.IntegerField(default=0)

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days = 7))

    # For russian lang
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'