# Generated by Django 4.0.4 on 2022-05-09 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_app', '0006_alter_url_short_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='full_url',
            field=models.URLField(max_length=300),
        ),
    ]