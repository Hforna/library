# Generated by Django 4.2 on 2024-06-12 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library_app', '0004_avaliationsbook_avaliation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avaliationsbook',
            name='avaliation',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='avaliationsbook',
            name='user',
            field=models.ForeignKey(default='Anonymous', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
