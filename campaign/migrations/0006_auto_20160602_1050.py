# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-02 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0005_video_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(default='The Title', max_length=100),
        ),
    ]
