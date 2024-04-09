# Generated by Django 5.0.3 on 2024-03-14 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(unique=True, verbose_name='Название курса')),
                ('img', models.ImageField(default='default.png', upload_to='courses', verbose_name='Изображение курса')),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_slug', models.SlugField(max_length=80, verbose_name='Название урока')),
                ('text', models.TextField(verbose_name='Текстовый материал')),
                ('number', models.IntegerField(verbose_name='Номер урока')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.courses')),
            ],
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_text', models.TextField(verbose_name='Текст задания')),
                ('lesson', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='courses.lesson')),
            ],
        ),
    ]
