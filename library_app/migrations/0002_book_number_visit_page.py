# Generated by Django 4.2 on 2024-06-11 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='number_visit_page',
            field=models.IntegerField(default=0),
        ),
    ]
