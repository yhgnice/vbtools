# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-22 20:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20170216_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='http://www.iqiyi.com/v_19rrakb0jk.html#vfrm=24-9-0-1', max_length=100, verbose_name='\u8fde\u63a5\u5730\u5740'),
        ),
    ]
