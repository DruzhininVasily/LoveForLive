# Generated by Django 5.0.3 on 2024-03-19 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_lessonprogress_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonprogress',
            name='feedback',
            field=models.TextField(blank=True, verbose_name='Обратная связь'),
        ),
    ]