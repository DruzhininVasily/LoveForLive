# Generated by Django 5.0.3 on 2024-03-19 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_lesson_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonprogress',
            name='feedback',
            field=models.TextField(default='', verbose_name='Обратная связь'),
        ),
    ]
