# Generated by Django 4.0.4 on 2022-05-09 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('url_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='url',
            old_name='mapped_full_url',
            new_name='full_url',
        ),
        migrations.RenameField(
            model_name='url',
            old_name='url',
            new_name='short_url',
        ),
    ]