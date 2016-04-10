# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=255)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(max_length=255, verbose_name='Name', db_index=True)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('image', models.ImageField(max_length=255, upload_to=b'categories', null=True, verbose_name='Image', blank=True)),
                ('slug', models.SlugField(max_length=255, verbose_name='Slug')),
            ],
            options={
                'ordering': ['path'],
                'abstract': False,
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
    ]
