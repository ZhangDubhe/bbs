# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-07-06 09:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20180706_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='avatars/default_avatar.png', upload_to='avatars/'),
        ),
    ]
