# Generated by Django 3.1.4 on 2021-01-21 22:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0004_auto_20210115_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='liked', to=settings.AUTH_USER_MODEL, verbose_name='Liked by'),
        ),
    ]
