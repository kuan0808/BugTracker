# Generated by Django 3.1.4 on 2021-01-14 18:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_project_latest'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='liked',
            field=models.ManyToManyField(blank=True, default=None, related_name='likes', to=settings.AUTH_USER_MODEL, verbose_name='Liked by'),
        ),
        migrations.AlterField(
            model_name='project',
            name='manager',
            field=models.ManyToManyField(blank=True, default=None, related_name='is_manager_in', to=settings.AUTH_USER_MODEL, verbose_name='Manager'),
        ),
        migrations.AlterField(
            model_name='project',
            name='member',
            field=models.ManyToManyField(blank=True, default=None, related_name='is_member_in', to=settings.AUTH_USER_MODEL, verbose_name='Member'),
        ),
    ]