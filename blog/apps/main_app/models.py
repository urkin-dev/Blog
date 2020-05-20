import datetime
from django.db import models
from django.utils import timezone

class Article(models.Model):
    article_image       = models.ImageField(upload_to='img', max_length=100, default='img/default/default.jpg')
    article_title       = models.CharField('Название статьи', max_length = 200)
    article_description = models.CharField('Описание статьи', max_length = 450)
    article_text        = models.TextField('Текст статьи')
    pub_date            = models.DateTimeField('Дата публикации')
    is_main_article     = models.BooleanField(default=False)

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days = 7))

    # For russian lang
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'