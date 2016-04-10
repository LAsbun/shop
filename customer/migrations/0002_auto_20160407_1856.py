# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(validators=[django.core.validators.RegexValidator(b'^[^._-][\\w.]*@(?:[A-Za-z0-9]+\\.)+[A-Za-z]+$', 'Enter a valid Email. This value may contain only letters, numbers ', b'invalid')], error_messages={b'unique': 'A user with that email already exists.'}, max_length=254, blank=True, help_text='Required.', unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={b'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator(b'^[\\w.+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', b'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and /./+/-/_ only.', unique=True, verbose_name='username'),
        ),
    ]
