# Generated by Django 3.2.9 on 2022-01-13 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_following_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='following',
            name='following',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='following', to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
        migrations.AlterField(
            model_name='following',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='follower', to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
