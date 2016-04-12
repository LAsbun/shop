from django.contrib import admin
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

# Register your models here.
from category.models import *


class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ProductAttributeAdmin(admin.ModelAdmin):
    pass


class ProductAttributeValueAdmin(admin.ModelAdmin):
    pass


class ProductClassAdmin(admin.ModelAdmin):
    pass


class RecommendProductAdmin(admin.ModelAdmin):
    pass


admin.site.register(RecommendProduct, RecommendProductAdmin)
admin.site.register(ProductClass, ProductClassAdmin)
admin.site.register(ProductAttributeValue, ProductAttributeAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)