# Generated by Django 4.1.2 on 2024-02-18 07:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_event_options_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
