# Generated by Django 5.0.2 on 2024-02-24 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note_manager', '0002_note_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='pinned_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
