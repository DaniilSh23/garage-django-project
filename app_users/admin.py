from django.contrib import admin
from django.contrib.auth.decorators import permission_required

from app_users.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'telephone', 'discount_card_number', 'verification_flag', 'news_counter']
    search_fields = ['user', 'city', 'verification_flag', 'news_counter']
    list_filter = ['verification_flag']


admin.site.register(Profile, ProfileAdmin)