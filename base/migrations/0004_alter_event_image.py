# Generated by Django 4.1.2 on 2024-02-24 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(default='/backgrounds/background.jpg', upload_to='images/'),
        ),
    ]
