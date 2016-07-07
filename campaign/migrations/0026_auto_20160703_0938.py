# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-03 09:38
from __future__ import unicode_literals

from django.db import migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0025_auto_20160703_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='photo',
            field=easy_thumbnails.fields.ThumbnailerImageField(default='images/None/no-image.png', upload_to='images/%Y/%m/%d'),
        ),
    ]
