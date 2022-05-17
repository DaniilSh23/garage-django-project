from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    # отношение таблиц БД ОДИН-К-ОДНОМУ
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=35, blank=True)
    # date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True, null=True, default=None)
    telephone = models.CharField(max_length=12, default='+7', blank=True)
    discount_card_number = models.IntegerField(blank=True, null=True, default=None)
    verification_flag = models.BooleanField(blank=True, null=True, default=False, verbose_name='Флаг верификации')
    news_counter = models.IntegerField(blank=True, null=True, default=0, verbose_name='Опубликовано новостей')
    avatar = models.ImageField(blank=True, null=True, upload_to=f'image/profiles/avatars/%Y/%m/%d')

    class Meta:
        db_table = 'Профиль пользователя'
        ordering = ['news_counter']
        permissions = (('verifications', 'verifications'),)

    def __str__(self):
        return f'Профиль пользователя: {self.user}'
