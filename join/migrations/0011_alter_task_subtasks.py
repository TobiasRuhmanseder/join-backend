# Generated by Django 5.0.6 on 2024-06-11 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0010_remove_task_category_color_alter_task_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='subtasks',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
