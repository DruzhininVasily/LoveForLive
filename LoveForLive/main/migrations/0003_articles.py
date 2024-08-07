# Generated by Django 5.0.3 on 2024-03-13 08:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_requestconsultation_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок статьи')),
                ('text', models.TextField(verbose_name='Текст статьи')),
                ('img', models.ImageField(default='default.png', upload_to='articles', verbose_name='Изображение статьи')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Статью',
                'verbose_name_plural': 'Статьи',
            },
        ),
    ]
