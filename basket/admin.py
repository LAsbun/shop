from django.contrib import admin
from basket.models import Line, Basket

# Register your models here.

class BasketAdmin(admin.ModelAdmin):
    list_display = ('owner', 'date_create')

class LineAdmin(admin.ModelAdmin):
    list_display = ('basket', 'product', 'quantity', 'date_create')


admin.site.register(Basket, BasketAdmin)
admin.site.register(Line, LineAdmin)