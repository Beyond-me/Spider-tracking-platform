# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticelType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('typename', models.CharField(max_length=50)),
                ('isDelete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '\u7c7b\u578b\u540d\u79f0',
                'verbose_name_plural': '\u7c7b\u578b\u540d\u79f0',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1000)),
                ('articel_id', models.FloatField(default=1506761596.216787)),
                ('author', models.CharField(max_length=1000)),
                ('release_date', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('content', DjangoUeditor.models.UEditorField(default='', blank=True)),
                ('mark', models.CharField(default=b'no mark', max_length=1000)),
                ('shortnote', models.CharField(default=b'no shortnote', max_length=1000)),
                ('isDelete', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': '\u6587\u7ae0',
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('release_date', models.DateTimeField(auto_now_add=True)),
                ('isDelete', models.BooleanField(default=False)),
                ('content', DjangoUeditor.models.UEditorField(default='', blank=True)),
                ('user', models.CharField(max_length=50)),
                ('articel', models.ForeignKey(to='content.Article')),
            ],
            options={
                'verbose_name': '\u6587\u7ae0\u8bc4\u8bba',
                'verbose_name_plural': '\u6587\u7ae0\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='TagType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tagname', models.CharField(max_length=50)),
                ('isDelete', models.BooleanField(default=False)),
                ('articel', models.ManyToManyField(to='content.Article')),
            ],
            options={
                'verbose_name': '\u6807\u7b7e\u540d\u79f0',
                'verbose_name_plural': '\u6807\u7b7e\u540d\u79f0',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='articel_tag',
            field=models.ManyToManyField(to='content.TagType'),
        ),
        migrations.AddField(
            model_name='article',
            name='articel_type',
            field=models.ForeignKey(to='content.ArticelType'),
        ),
    ]
