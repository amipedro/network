# Generated by Django 3.2.9 on 2022-01-11 18:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='network',
            options={'ordering': ('-created_at', '-updated_at')},
        ),
        migrations.CreateModel(
            name='Following',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='following', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='follower', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]