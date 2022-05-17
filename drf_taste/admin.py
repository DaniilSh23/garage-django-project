from django.contrib import admin
from drf_taste.models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


admin.site.register(Item, ItemAdmin)
