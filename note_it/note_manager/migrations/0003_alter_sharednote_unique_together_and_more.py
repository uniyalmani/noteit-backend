# Generated by Django 5.0.2 on 2024-02-24 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('note_manager', '0002_sharednote'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sharednote',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='sharednote',
            name='note',
        ),
        migrations.RemoveField(
            model_name='sharednote',
            name='user',
        ),
        migrations.DeleteModel(
            name='NoteVersion',
        ),
        migrations.DeleteModel(
            name='SharedNote',
        ),
    ]
