# Generated by Django 3.1.4 on 2021-01-21 22:12

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.png', upload_to=user.models.get_profile_image_path),
        ),
    ]
