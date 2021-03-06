#!/usr/bin/env python
# encoding: utf-8
# LAsbun  @ 2016-03-30

import re
import zlib

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
from django.utils.translation import pgettext_lazy
from django.core import exceptions


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


@python_2_unicode_compatible
class AbstractAddress(models.Model):
    """
    Superclass address object

    This is subclassed and extended to provide models for
    user, shipping and billing addresses.
    """
    MR, MISS, MRS, MS, DR = ('Mr', 'Miss', 'Mrs', 'Ms', 'Dr')
    TITLE_CHOICES = (
        (MR, _("Mr")),
        (MISS, _("Miss")),
        (MRS, _("Mrs")),
        (MS, _("Ms")),
        (DR, _("Dr")),
    )

    POSTCODE_REQUIRED = 'postcode' in settings.REQUIRED_ADDRESS_FIELDS

    # Regex for each country. Not listed countries don't use postcodes
    # Based on http://en.wikipedia.org/wiki/List_of_postal_codes
    POSTCODES_REGEX = {
        'AC': r'^[A-Z]{4}[0-9][A-Z]$',
        'AD': r'^AD[0-9]{3}$',
        'AF': r'^[0-9]{4}$',
        'AI': r'^AI-2640$',
        'AL': r'^[0-9]{4}$',
        'AM': r'^[0-9]{4}$',
        'AR': r'^([0-9]{4}|[A-Z][0-9]{4}[A-Z]{3})$',
        'AS': r'^[0-9]{5}(-[0-9]{4}|-[0-9]{6})?$',
        'AT': r'^[0-9]{4}$',
        'AU': r'^[0-9]{4}$',
        'AX': r'^[0-9]{5}$',
        'AZ': r'^AZ[0-9]{4}$',
        'BA': r'^[0-9]{5}$',
        'BB': r'^BB[0-9]{5}$',
        'BD': r'^[0-9]{4}$',
        'BE': r'^[0-9]{4}$',
        'BG': r'^[0-9]{4}$',
        'BH': r'^[0-9]{3,4}$',
        'BL': r'^[0-9]{5}$',
        'BM': r'^[A-Z]{2}([0-9]{2}|[A-Z]{2})',
        'BN': r'^[A-Z}{2}[0-9]]{4}$',
        'BO': r'^[0-9]{4}$',
        'BR': r'^[0-9]{5}(-[0-9]{3})?$',
        'BT': r'^[0-9]{3}$',
        'BY': r'^[0-9]{6}$',
        'CA': r'^[A-Z][0-9][A-Z][0-9][A-Z][0-9]$',
        'CC': r'^[0-9]{4}$',
        'CH': r'^[0-9]{4}$',
        'CL': r'^([0-9]{7}|[0-9]{3}-[0-9]{4})$',
        'CN': r'^[0-9]{6}$',
        'CO': r'^[0-9]{6}$',
        'CR': r'^[0-9]{4,5}$',
        'CU': r'^[0-9]{5}$',
        'CV': r'^[0-9]{4}$',
        'CX': r'^[0-9]{4}$',
        'CY': r'^[0-9]{4}$',
        'CZ': r'^[0-9]{5}$',
        'DE': r'^[0-9]{5}$',
        'DK': r'^[0-9]{4}$',
        'DO': r'^[0-9]{5}$',
        'DZ': r'^[0-9]{5}$',
        'EC': r'^EC[0-9]{6}$',
        'EE': r'^[0-9]{5}$',
        'EG': r'^[0-9]{5}$',
        'ES': r'^[0-9]{5}$',
        'ET': r'^[0-9]{4}$',
        'FI': r'^[0-9]{5}$',
        'FK': r'^[A-Z]{4}[0-9][A-Z]{2}$',
        'FM': r'^[0-9]{5}(-[0-9]{4})?$',
        'FO': r'^[0-9]{3}$',
        'FR': r'^[0-9]{5}$',
        'GA': r'^[0-9]{2}.*[0-9]{2}$',
        'GB': r'^[A-Z][A-Z0-9]{1,3}[0-9][A-Z]{2}$',
        'GE': r'^[0-9]{4}$',
        'GF': r'^[0-9]{5}$',
        'GG': r'^([A-Z]{2}[0-9]{2,3}[A-Z]{2})$',
        'GI': r'^GX111AA$',
        'GL': r'^[0-9]{4}$',
        'GP': r'^[0-9]{5}$',
        'GR': r'^[0-9]{5}$',
        'GS': r'^SIQQ1ZZ$',
        'GT': r'^[0-9]{5}$',
        'GU': r'^[0-9]{5}$',
        'GW': r'^[0-9]{4}$',
        'HM': r'^[0-9]{4}$',
        'HN': r'^[0-9]{5}$',
        'HR': r'^[0-9]{5}$',
        'HT': r'^[0-9]{4}$',
        'HU': r'^[0-9]{4}$',
        'ID': r'^[0-9]{5}$',
        'IL': r'^[0-9]{7}$',
        'IM': r'^IM[0-9]{2,3}[A-Z]{2}$$',
        'IN': r'^[0-9]{6}$',
        'IO': r'^[A-Z]{4}[0-9][A-Z]{2}$',
        'IQ': r'^[0-9]{5}$',
        'IR': r'^[0-9]{5}-[0-9]{5}$',
        'IS': r'^[0-9]{3}$',
        'IT': r'^[0-9]{5}$',
        'JE': r'^JE[0-9]{2}[A-Z]{2}$',
        'JM': r'^JM[A-Z]{3}[0-9]{2}$',
        'JO': r'^[0-9]{5}$',
        'JP': r'^[0-9]{3}-?[0-9]{4}$',
        'KE': r'^[0-9]{5}$',
        'KG': r'^[0-9]{6}$',
        'KH': r'^[0-9]{5}$',
        'KR': r'^[0-9]{5}$',
        'KY': r'^KY[0-9]-[0-9]{4}$',
        'KZ': r'^[0-9]{6}$',
        'LA': r'^[0-9]{5}$',
        'LB': r'^[0-9]{8}$',
        'LI': r'^[0-9]{4}$',
        'LK': r'^[0-9]{5}$',
        'LR': r'^[0-9]{4}$',
        'LS': r'^[0-9]{3}$',
        'LT': r'^(LT-)?[0-9]{5}$',
        'LU': r'^[0-9]{4}$',
        'LV': r'^LV-[0-9]{4}$',
        'LY': r'^[0-9]{5}$',
        'MA': r'^[0-9]{5}$',
        'MC': r'^980[0-9]{2}$',
        'MD': r'^MD-?[0-9]{4}$',
        'ME': r'^[0-9]{5}$',
        'MF': r'^[0-9]{5}$',
        'MG': r'^[0-9]{3}$',
        'MH': r'^[0-9]{5}$',
        'MK': r'^[0-9]{4}$',
        'MM': r'^[0-9]{5}$',
        'MN': r'^[0-9]{5}$',
        'MP': r'^[0-9]{5}$',
        'MQ': r'^[0-9]{5}$',
        'MT': r'^[A-Z]{3}[0-9]{4}$',
        'MV': r'^[0-9]{4,5}$',
        'MX': r'^[0-9]{5}$',
        'MY': r'^[0-9]{5}$',
        'MZ': r'^[0-9]{4}$',
        'NA': r'^[0-9]{5}$',
        'NC': r'^[0-9]{5}$',
        'NE': r'^[0-9]{4}$',
        'NF': r'^[0-9]{4}$',
        'NG': r'^[0-9]{6}$',
        'NI': r'^[0-9]{3}-[0-9]{3}-[0-9]$',
        'NL': r'^[0-9]{4}[A-Z]{2}$',
        'NO': r'^[0-9]{4}$',
        'NP': r'^[0-9]{5}$',
        'NZ': r'^[0-9]{4}$',
        'OM': r'^[0-9]{3}$',
        'PA': r'^[0-9]{6}$',
        'PE': r'^[0-9]{5}$',
        'PF': r'^[0-9]{5}$',
        'PG': r'^[0-9]{3}$',
        'PH': r'^[0-9]{4}$',
        'PK': r'^[0-9]{5}$',
        'PL': r'^[0-9]{2}-?[0-9]{3}$',
        'PM': r'^[0-9]{5}$',
        'PN': r'^[A-Z]{4}[0-9][A-Z]{2}$',
        'PR': r'^[0-9]{5}$',
        'PT': r'^[0-9]{4}(-?[0-9]{3})?$',
        'PW': r'^[0-9]{5}$',
        'PY': r'^[0-9]{4}$',
        'RE': r'^[0-9]{5}$',
        'RO': r'^[0-9]{6}$',
        'RS': r'^[0-9]{5}$',
        'RU': r'^[0-9]{6}$',
        'SA': r'^[0-9]{5}$',
        'SD': r'^[0-9]{5}$',
        'SE': r'^[0-9]{5}$',
        'SG': r'^([0-9]{2}|[0-9]{4}|[0-9]{6})$',
        'SH': r'^(STHL1ZZ|TDCU1ZZ)$',
        'SI': r'^(SI-)?[0-9]{4}$',
        'SK': r'^[0-9]{5}$',
        'SM': r'^[0-9]{5}$',
        'SN': r'^[0-9]{5}$',
        'SV': r'^01101$',
        'SZ': r'^[A-Z][0-9]{3}$',
        'TC': r'^TKCA1ZZ$',
        'TD': r'^[0-9]{5}$',
        'TH': r'^[0-9]{5}$',
        'TJ': r'^[0-9]{6}$',
        'TM': r'^[0-9]{6}$',
        'TN': r'^[0-9]{4}$',
        'TR': r'^[0-9]{5}$',
        'TT': r'^[0-9]{6}$',
        'TW': r'^[0-9]{5}$',
        'UA': r'^[0-9]{5}$',
        'US': r'^[0-9]{5}(-[0-9]{4}|-[0-9]{6})?$',
        'UY': r'^[0-9]{5}$',
        'UZ': r'^[0-9]{6}$',
        'VA': r'^00120$',
        'VC': r'^VC[0-9]{4}',
        'VE': r'^[0-9]{4}[A-Z]?$',
        'VG': r'^VG[0-9]{4}$',
        'VI': r'^[0-9]{5}$',
        'VN': r'^[0-9]{6}$',
        'WF': r'^[0-9]{5}$',
        'XK': r'^[0-9]{5}$',
        'YT': r'^[0-9]{5}$',
        'ZA': r'^[0-9]{4}$',
        'ZM': r'^[0-9]{5}$',
    }

    title = models.CharField(
        pgettext_lazy(u"Treatment Pronouns for the customer", u"Title"),
        max_length=64, choices=TITLE_CHOICES, blank=True)
    first_name = models.CharField(_("First name"), max_length=255, blank=True)
    last_name = models.CharField(_("Last name"), max_length=255, blank=True)

    # We use quite a few lines of an address as they are often quite long and
    # it's easier to just hide the unnecessary ones than add extra ones.
    line1 = models.CharField(_("First line of address"), max_length=255)
    line2 = models.CharField(
        _("Second line of address"), max_length=255, blank=True)
    line3 = models.CharField(
        _("Third line of address"), max_length=255, blank=True)
    line4 = models.CharField(_("City"), max_length=255, blank=True)
    state = models.CharField(_("State/County"), max_length=255, blank=True)
    postcode = models.CharField(
        _("Post/Zip-code"), max_length=64, blank=True)


    #: A field only used for searching addresses - this contains all the
    #: relevant fields.  This is effectively a poor man's Solr text field.
    search_text = models.TextField(
        _("Search text - used only for searching addresses"), editable=False)

    def __str__(self):
        return self.summary

    class Meta:
        abstract = True
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    # Saving

    def save(self, *args, **kwargs):
        self._update_search_text()
        super(AbstractAddress, self).save(*args, **kwargs)

    def clean(self):
        # Strip all whitespace
        for field in ['first_name', 'last_name', 'line1', 'line2', 'line3',
                      'line4', 'state', 'postcode']:
            if self.__dict__[field]:
                self.__dict__[field] = self.__dict__[field].strip()

        # Ensure postcodes are valid for country
        self.ensure_postcode_is_valid_for_country()

    def ensure_postcode_is_valid_for_country(self):
        """
        Validate postcode given the country
        """
        if not self.postcode and self.POSTCODE_REQUIRED and self.country_id:
            country_code = self.country.iso_3166_1_a2
            regex = self.POSTCODES_REGEX.get(country_code, None)
            if regex:
                msg = _("Addresses in %(country)s require a valid postcode") \
                    % {'country': self.country}
                raise exceptions.ValidationError(msg)

        if self.postcode and self.country_id:
            # Ensure postcodes are always uppercase
            postcode = self.postcode.upper().replace(' ', '')
            country_code = self.country.iso_3166_1_a2
            regex = self.POSTCODES_REGEX.get(country_code, None)

            # Validate postcode against regex for the country if available
            if regex and not re.match(regex, postcode):
                msg = _("The postcode '%(postcode)s' is not valid "
                        "for %(country)s") \
                    % {'postcode': self.postcode,
                       'country': self.country}
                raise exceptions.ValidationError(
                    {'postcode': [msg]})

    def _update_search_text(self):
        search_fields = filter(
            bool, [self.first_name, self.last_name,
                   self.line1, self.line2, self.line3, self.line4,
                   self.state, self.postcode, self.country.name])
        self.search_text = ' '.join(search_fields)

    # Properties

    @property
    def city(self):
        # Common alias
        return self.line4

    @property
    def summary(self):
        """
        Returns a single string summary of the address,
        separating fields using commas.
        """
        return u", ".join(self.active_address_fields())

    @property
    def salutation(self):
        """
        Name (including title)
        """
        return self.join_fields(
            ('title', 'first_name', 'last_name'),
            separator=u" ")

    @property
    def name(self):
        return self.join_fields(('first_name', 'last_name'), separator=u" ")

    # Helpers

    def generate_hash(self):
        """
        Returns a hash of the address summary
        """
        # We use an upper-case version of the summary
        return zlib.crc32(self.summary.strip().upper().encode('UTF8'))

    def join_fields(self, fields, separator=u", "):
        """
        Join a sequence of fields using the specified separator
        """
        field_values = []
        for field in fields:
            # Title is special case
            if field == 'title':
                value = self.get_title_display()
            else:
                value = getattr(self, field)
            field_values.append(value)
        return separator.join(filter(bool, field_values))

    def populate_alternative_model(self, address_model):
        """
        For populating an address model using the matching fields
        from this one.

        This is used to convert a user address to a shipping address
        as part of the checkout process.
        """
        destination_field_names = [
            field.name for field in address_model._meta.fields]
        for field_name in [field.name for field in self._meta.fields]:
            if field_name in destination_field_names and field_name != 'id':
                setattr(address_model, field_name, getattr(self, field_name))

    def active_address_fields(self, include_salutation=True):
        """
        Return the non-empty components of the address, but merging the
        title, first_name and last_name into a single line.
        """
        fields = [self.line1, self.line2, self.line3,
                  self.line4, self.state, self.postcode]
        if include_salutation:
            fields = [self.salutation] + fields
        fields = [f.strip() for f in fields if f]
        try:
            fields.append(self.country.printable_name)
        except exceptions.ObjectDoesNotExist:
            pass
        return fields