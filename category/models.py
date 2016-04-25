#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from datetime import datetime, date

from django.utils.encoding import python_2_unicode_compatible
from treebeard.mp_tree import MP_Node
from django.db import models
from django.utils import six
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.apps import apps
from django.core.files import File


@python_2_unicode_compatible
class Category(MP_Node):
    """
    A product category. Merely used for navigational purposes; has no
    effects on business logic.

    Uses django-treebeard.
    """
    name = models.CharField('分类名', max_length=255, db_index=True)
    description = models.TextField('分类描述', blank=True)
    image = models.ImageField('图片', upload_to='images/categories', blank=True,
                              null=True, max_length=255)
    slug = models.SlugField('简单描述', max_length=255, db_index=True)

    _slug_separator = '/'
    _full_name_separator = ' > '

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        """
        Returns a string representation of the category and it's ancestors,
        e.g. 'Books > Non-fiction > Essential programming'.

        It's rarely used in Oscar's codebase, but used to be stored as a
        CharField and is hence kept for backwards compatibility. It's also
        sufficiently useful to keep around.
        """
        names = [category.name for category in self.get_ancestors_and_self()]
        return self._full_name_separator.join(names)

    @property
    def full_slug(self):
        """
        Returns a string of this category's slug concatenated with the slugs
        of it's ancestors, e.g. 'books/non-fiction/essential-programming'.

        Oscar used to store this as in the 'slug' model field, but this field
        has been re-purposed to only store this category's slug and to not
        include it's ancestors' slugs.
        """
        slugs = [category.slug for category in self.get_ancestors_and_self()]
        return self._slug_separator.join(slugs)

    def generate_slug(self):
        """
        Generates a slug for a category. This makes no attempt at generating
        a unique slug.
        """
        # return slugify(self.name)
        return self.name

    def ensure_slug_uniqueness(self):
        """
        Ensures that the category's slug is unique amongst it's siblings.
        This is inefficient and probably not thread-safe.
        """
        unique_slug = self.slug
        siblings = self.get_siblings().exclude(pk=self.pk)
        next_num = 2
        while siblings.filter(slug=unique_slug).exists():
            unique_slug = '{slug}_{end}'.format(slug=self.slug, end=next_num)
            next_num += 1

        if unique_slug != self.slug:
            self.slug = unique_slug
            self.save()

    def save(self, *args, **kwargs):
        """
        Oscar traditionally auto-generated slugs from names. As that is
        often convenient, we still do so if a slug is not supplied through
        other means. If you want to control slug creation, just create
        instances with a slug already set, or expose a field on the
        appropriate forms.
        """
        if self.slug:
            # Slug was supplied. Hands off!
            super(Category, self).save(*args, **kwargs)
        else:
            self.slug = self.generate_slug()
            super(Category, self).save(*args, **kwargs)
            # We auto-generated a slug, so we need to make sure that it's
            # unique. As we need to be able to inspect the category's siblings
            # for that, we need to wait until the instance is saved. We
            # update the slug and save again if necessary.
            self.ensure_slug_uniqueness()

    def get_ancestors_and_self(self):
        """
        Gets ancestors and includes itself. Use treebeard's get_ancestors
        if you don't want to include the category itself. It's a separate
        function as it's commonly used in templates.
        """
        return list(self.get_ancestors()) + [self]

    def get_descendants_and_self(self):
        """
        Gets descendants and includes itself. Use treebeard's get_descendants
        if you don't want to include the category itself. It's a separate
        function as it's commonly used in templates.
        """
        return list(self.get_descendants()) + [self]

    # def get_absolute_url(self):
    #     """
    #     Our URL scheme means we have to look up the category's ancestors. As
    #     that is a bit more expensive, we cache the generated URL. That is
    #     safe even for a stale cache, as the default implementation of
    #     ProductCategoryView does the lookup via primary key anyway. But if
    #     you change that logic, you'll have to reconsider the caching
    #     approach.
    #     """
    #     cache_key = 'CATEGORY_URL_%s' % self.pk
    #     url = cache.get(cache_key)
    #     if not url:
    #         url = reverse(
    #             'catalogue:category',
    #             kwargs={'category_slug': self.full_slug, 'pk': self.pk})
    #         cache.set(cache_key, url)
    #     return url

    class Meta:

        app_label = 'category'
        ordering = ['path']
        verbose_name = '产品目录'
        verbose_name_plural = verbose_name
    @property
    def has_children(self):
        return self.get_num_children() > 0

    def get_num_children(self):
        return self.get_children().count()


# 产品类别 (e.g BOOK, T-SHIRT)
class ProductClass(models.Model):

    name = models.CharField(max_length=35, unique=True,
                            verbose_name='产品种类')

    summary = models.CharField(max_length=256, blank=True,
                               verbose_name='产品种类简述')

    detail = models.TextField(blank=True, verbose_name='产品种类详述')

    is_shipping = models.BooleanField(default=False, verbose_name='是否需要运输')

    # class Meta:
    #     abstract = True

    def __str__(self):
        return self.name

    @property
    def has_attributes(self):
        return self.attributes.exists()

    class Meta:
        verbose_name_plural = verbose_name = '产品所属种类'

# 附加属性
@python_2_unicode_compatible
class ProductAttribute(models.Model):
    product_class = models.ForeignKey(
        'category.ProductClass', related_name='attributes', blank=True,
        null=True, verbose_name='产品分类的附加属性'
    )

    name = models.CharField('附加属性名', max_length=128)

    TEXT = 'text'
    INTEGER = 'integer'
    BOOLEAN = 'boolean'
    FLOAT = 'float'
    RICHTEXT = "rich text"
    DATE = 'data'
    IMAGE = 'image'

    TYPE_CHOICES = (
        (TEXT, _("Text")),
        (INTEGER, _("Integer")),
        (BOOLEAN, _("True / False")),
        (FLOAT, _("Float")),
        (RICHTEXT, _("RichText")),
        (DATE, _("Date")),
        (IMAGE, _("Image")),
    )

    type = models.CharField(
        choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],
        max_length=20, verbose_name=_('Type')
    )

    required = models.BooleanField(_('Required'), default=False)

    class Meta:
        # abstract = True
        app_label = 'category'
        verbose_name= '附加属性'
        verbose_name_plural = '附加属性'

    @property
    def is_file(self):
        return self.type == self.IMAGE

    def __str__(self):
        return self.name

    def save_value(self, product, value):
        # ProductAttributeValue =
        ProductAttributeValue = apps.get_model('category', 'ProductAttributeValue')

        try:
            value_obj = product.attribute_values.get(attributes=self)
        except ProductAttributeValue.DoesNotExist:
            # FileField uses False for announcing deletion of the file
            # not creating a new value
            delete_file = self.is_file and value is False
            if value is None or value == '' or delete_file:
                return
            value_obj = ProductAttributeValue.objects.create(
                product=product, attribute=self
            )

        if self.is_file:
             # File fields in Django are treated differently, see
            # django.db.models.fields.FileField and method save_form_data
            if value is None:
            #  No change
                return
            elif value is False:
             #   Delete File
                value_obj.delete()
            else:
                # New uploaded file
                value_obj.value = value
                value_obj.save()
        else:
            if value is None or value == '':
                value_obj.delete()
                return
            if value != value_obj.value:
                value_obj.value = value
                value_obj.save()

    def validate_value(self, value):
        validator = getattr(self, '_validate_%s' %self.type)
        validator(value)

    # Validators

    def _validate_text(self, value):
        if not isinstance(value, six.string_types):
            raise ValidationError(_('Must be str or Unicode'))

    _validate_richtext = _validate_text

    def _validate_float(self, value):
        try:
            float(value)
        except ValueError:
            raise ValidationError(_("Must be a float"))

    def _validate_integer(self, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError(_("Must be an integer"))

    def _validate_date(self, value):
        if not (isinstance(value, datetime) or isinstance(value, date)):
            raise ValidationError(_("Must be a date or datetime"))

    def _validate_boolean(self, value):
        if not type(value) == bool:
            raise ValidationError(_("Must be a boolean"))

    def _validate_image(self, value):
        if value and not isinstance(value, File):
            raise ValidationError(_("Must be a file field"))

    def __unicode__(self):
        return self.name



# 附加属性值
class ProductAttributeValue(models.Model):

    attribute = models.ForeignKey(
        'category.ProductAttribute', verbose_name='附加属性'
    )

    product = models.ForeignKey(
        'category.Product', related_name='attribute_values',
        verbose_name='所属产品'
    )

    value_text = models.TextField(_('Text'), blank=True, null=True)
    value_integer = models.IntegerField(
        _('Integer'), blank=True, null=True
    )
    value_float = models.FloatField(
        _('Fload'),blank=True, null=True
    )
    value_richtext = models.TextField(
        _('Richtext'), blank=True, null=True
    )
    value_boolean = models.BooleanField(
        _('Boolean'), blank=True,
    )
    value_date = models.DateField(
        _('Date'), blank=True, null=True
    )
    value_image = models.ImageField(
        upload_to=settings.IMAGE_UPLOAD_FOLDER,
        blank=True, null=True
    )

    # class Meta:
    #     abstract = True

    def _get_value(self):
        return getattr(self, 'value_%s' % self.attribute.type)

    def _set_value(self, new_value):
        setattr(self, 'value_%s' % self.attribute.type, new_value)

    value = property(_get_value, _set_value)

    def __str__(self):
        return self.summary()

    def summary(self):
        """
        Gets a string representation of both the attribute and it's value,
        used e.g in product summaries.
        """
        return u"%s: %s" % (self.attribute.name, self.value_as_text)

    @property
    def value_as_text(self):
        property_name = '_%s_as_text' % self.attribute.type
        return getattr(self, property_name, self.value)

    def __unicode__(self):
        return self.attribute.type


    class Meta:
        ordering = ['-attribute']
        verbose_name_plural = verbose_name = '附加属性值'
# 产品
class Product(models.Model):

    recommended_products = models.ManyToManyField(
        'category.Product', through='RecommendProduct', blank=True,
        verbose_name='推荐的产品',
        help_text=_("These are products that are recommended to accompany the "
                    "main product."))

    product_class = models.ForeignKey(
        'category.ProductClass', verbose_name='产品所属产品种类',
    )

    category = models.ForeignKey(
        'category.Category', verbose_name= '产品所属目录分类',
    )

    images = models.ImageField(
        upload_to='product/%Y/%m/%d', verbose_name='图片', null=True
    )

    attributes = models.ManyToManyField(
        'category.ProductAttribute',
        through='category.ProductAttributeValue',
        verbose_name='产品的附加属性',
        help_text=_("A product attribute is something that this product may "
                    "have, such as a size, as specified by its class"))

    name = models.CharField(max_length=40, verbose_name='产品名')
    summary = models.CharField(
        max_length=256, verbose_name='产品简要', blank=True
    )
    detail = models.TextField(
        verbose_name='产品详细信息', blank=True
    )
    retail = models.FloatField(
        verbose_name='零售价',
    )
    cost = models.FloatField(
        verbose_name='成本',
    )
    date_create = models.DateTimeField(
        verbose_name='产品上架时间'
    )
    store_count = models.IntegerField(
        verbose_name='产品库存量'
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = '产品'
        ordering = ['date_create']

# 推荐产品
class RecommendProduct(models.Model):
    primary = models.ForeignKey(
        'category.Product', related_name='primary_recommendations',
        verbose_name=_("Primary product"))
    recommendation = models.ForeignKey(
        'category.Product', verbose_name=_("Recommended product"))
    ranking = models.PositiveSmallIntegerField(
        _('Ranking'), default=0,
        help_text=_('Determines order of the products. A product with a higher'
                    ' value will appear before one with a lower ranking.'))



    class Meta:
        # abstract = True

        verbose_name = '产品推荐'
        verbose_name_plural = '产品推荐'


    def __unicode__(self):
        return self.primary.name