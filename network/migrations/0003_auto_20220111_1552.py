# Generated by Django 3.2.9 on 2022-01-11 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_auto_20220111_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='following_count',
            field=models.IntegerField(default=0),
        ),
    ]