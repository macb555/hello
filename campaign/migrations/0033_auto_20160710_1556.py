# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-10 15:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0032_auto_20160710_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='region_of_birth',
            field=models.CharField(blank=True, choices=[(b'Awdal', b'Awdal'), (b'Bakool', b'Bakoo'), (b'Banaadir', b'Banaadir'), (b'Bari', b'Bari'), (b'Bay', b'Bay'), (b'Galguduud', b'Galguduud'), (b'Gedo', b'Gedo'), (b'Hiiraan', b'Hiiraan'), (b'Jubada Dhexe', b'Jubada Dhexe'), (b'Jubada Hoose', b'Jubada Hoose'), (b'Nugaal', b'Nugaal'), (b'Sanaag', b'Sanaag'), (b'Shabeelaha Dhexe', b'Shabeelaha Dhexe'), (b'Shabeelaha Hoose', b'Shabeelaha Hoose'), (b'Sool', b'Sool'), (b'Togdheer', b'Togdheer'), (b'Waqooyi Galbeed', b'Waqooyi Galbeed')], default=2, max_length=30, null=True),
        ),
    ]
