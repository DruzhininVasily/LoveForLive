# Generated by Django 5.0.3 on 2024-03-21 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_alter_lessonprogress_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='description',
            field=models.TextField(default=None, max_length=500, verbose_name='Описание курса'),
        ),
    ]
