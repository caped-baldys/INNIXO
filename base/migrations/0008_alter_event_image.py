# Generated by Django 4.1.2 on 2024-02-24 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(default='images/background.jpg', upload_to='backgrounds/'),
        ),
    ]
