# Generated by Django 3.1.4 on 2021-01-07 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20201229_2125'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='latest',
            field=models.DateTimeField(auto_now=True, verbose_name='Latest'),
        ),
    ]
