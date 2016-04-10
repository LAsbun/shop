#!/usr/bin/env python
# encoding: utf-8
# LAsbun  @ 2016-03-30

from django.conf import settings
from django.contrib.auth import models as auth_models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.template import Context, Template, TemplateDoesNotExist
from django.template.loader import get_template
from django.utils import six, timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


class UserManager(auth_models.BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError(_('The given username must be set'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          # is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)


class AbstractUser(auth_models.AbstractBaseUser):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    copy From AbstractUser  But No Fisrstname and Lastname


    """
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, digits and '
                    '/./+/-/_ only.'),
        validators=[
            RegexValidator(r'^[\w.+-]+$',
            # '输入一个合法的昵称,只包含字母,数字和@  . + - _', 'invalid'),
                                      _('Enter a valid username. '
                                        'This value may contain only letters, numbers '
                                        'and @/./+/-/_ characters.'), 'invalid')
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        })

    real_name = models.CharField(verbose_name=_('real name'), max_length=30, blank=True, default='还没有填写哦')
    email = models.EmailField(_('email address'), blank=True, unique=True,
                              help_text=_('Required.'),
            validators=[
            RegexValidator(r'^[^._-][\w.]*@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$',
            # '输入一个合法的昵称,只包含字母,数字和@  . + - _', 'invalid'),
                                      _('Enter a valid Email. '
                                        'This value may contain only letters, numbers '), 'invalid')
        ],
        error_messages={
            'unique': _("A user with that email already exists."),
        })
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(verbose_name='时间合并', default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = True

    def get_real_name(self):

        return self.real_name

    # 后续加
    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     """
    #     Sends an email to this User.
    #     """
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

# @python_2_unicode_compatible
# class AbstractEmail(models.Model):
#     """
#     后续加
#     """
#
#     class Meta:
#         verbose_name = 'email'
#         verbose_name_plural = 'emails'
#         abstract = True