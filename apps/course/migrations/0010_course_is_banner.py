# Generated by Django 2.1.1 on 2018-10-07 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_auto_20181001_0325'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否轮播'),
        ),
    ]