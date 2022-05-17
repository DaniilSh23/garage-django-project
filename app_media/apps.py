from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppMediaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_media'
    # определяет название для нашего приложения
    # применим метод gettext_lazy
    verbose_name = _('media')
