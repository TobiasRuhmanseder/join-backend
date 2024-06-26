# Generated by Django 5.0.6 on 2024-06-01 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('join', '0003_rename_created_at_task_due_date_task_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='category_color',
            field=models.CharField(default='#000000', max_length=20),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('todo', 'To Do'), ('inprogress', 'In Progress'), ('awaitfeedback', 'Awaiting Feedback'), ('done', 'Done')], default='todo', max_length=20),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('urgent', 'urgent'), ('medium', 'medium'), ('low', 'low')], default='low', max_length=20),
        ),
    ]
