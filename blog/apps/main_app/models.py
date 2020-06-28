import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings

from django.contrib.auth.models import User

from PIL import Image

import os
from django.db.models.signals import pre_save
from django.dispatch.dispatcher import receiver

class UserProfile(models.Model):

    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    bio    = models.CharField('Описание пользователя', max_length=170)
    avatar = models.ImageField(upload_to='img/users', max_length=100, default='img/default_images/defaultUser.png')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img  = Image.open(self.avatar.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)  
            img.save(self.avatar.path)

class Category(models.Model):
    category_no   = models.IntegerField('Номер категории', primary_key=True)
    name          = models.CharField('Название категории', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Article(models.Model):
    article_image       = models.ImageField(upload_to='img/articles', max_length=100, default='img/default_images/default.jpg')
    article_title       = models.CharField('Название статьи', max_length = 30)
    article_description = models.CharField('Краткое описание статьи', max_length = 150)
    article_text        = models.TextField('Текст статьи')
    pub_date            = models.DateTimeField('Дата публикации')
    is_main_in_category = models.BooleanField('Главная статья в своей категории(можно поставить только 1)', default=False)
    is_main_in_homepage = models.BooleanField('Главная статья на домашней страницу(всего 3)', default=False)
    author              = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, default = '1')
    category            = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, db_column='category_no', default=14)
    likes               = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.is_main_in_category:
            try:
                temp = Article.objects.get(is_main_in_category=True, category=self.category)
                if self != temp:
                    temp.is_main_in_category = False
                    temp.save()
            except Article.DoesNotExist:
                pass

        if self.is_main_in_homepage:
            try:
                main_count = len(Article.objects.filter(is_main_in_homepage=True))
                if main_count >= 3:
                    self.is_main_in_homepage = False
            except Article.DoesNotExist:
                pass
            
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days = 7))

    # For russian lang
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

class Comment(models.Model):
    article      = models.ForeignKey(Article, on_delete = models.CASCADE)
    
    author       = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    comment_text = models.CharField('Текст комментария', max_length = 200)
    pub_date     = models.DateTimeField('Дата публикации')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

# Delete images from media folder when they uploaded
@receiver(pre_save, sender=UserProfile)
def delete_avatar(sender, instance, *args, **kwargs):
    try:
        old_instance = UserProfile.objects.get(id=instance.id)
        old_avatar = os.path.basename(old_instance.avatar.name)
        new_avatar = os.path.basename(instance.avatar.name)

        if (old_avatar != new_avatar):
            if (old_avatar != 'defaultUser.png'):
                os.remove(old_instance.avatar.path)
            
    except UserProfile.DoesNotExist:
        return None

@receiver(pre_save, sender=Article)
def delete_img(sender, instance, *args, **kwargs):
    try:
        old_instance = Article.objects.get(id=instance.id)
        old_image = os.path.basename(old_instance.article_image.name)
        new_image = os.path.basename(instance.article_image.name)

        if (new_image != old_image):
            if (old_image != 'default.jpg'):
                os.remove(old_instance.article_image.path)
            
    except Article.DoesNotExist:
        return None