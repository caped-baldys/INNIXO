# Generated by Django 4.1.2 on 2024-02-27 16:56

import base.models
from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_rename_participant_eventregistration_teamleader_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventregistration',
            old_name='submitted_name_1',
            new_name='memeber_1',
        ),
        migrations.RenameField(
            model_name='eventregistration',
            old_name='submitted_name_2',
            new_name='memeber_2',
        ),
        migrations.RenameField(
            model_name='eventregistration',
            old_name='submitted_name_3',
            new_name='memeber_3',
        ),
        migrations.RenameField(
            model_name='eventregistration',
            old_name='submitted_name_4',
            new_name='memeber_4',
        ),
        migrations.RenameField(
            model_name='eventregistration',
            old_name='submitted_name_5',
            new_name='memeber_5',
        ),
        migrations.AddField(
            model_name='event',
            name='members_required',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='payment',
            field=models.ImageField(blank=True, null=True, upload_to=base.models.participant_event_directory_path),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True),
        ),
        migrations.AddField(
            model_name='eventregistration',
            name='team_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
