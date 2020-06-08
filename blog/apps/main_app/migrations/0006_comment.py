# Generated by Django 3.0.6 on 2020-06-08 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20200530_2318'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(max_length=50, verbose_name='Автор комментария')),
                ('comment_text', models.CharField(max_length=200, verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(verbose_name='Дата публикации')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Article')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
    ]