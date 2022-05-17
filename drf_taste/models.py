from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name='name')
    description = models.TextField(blank=True, verbose_name='description')
    weight = models.FloatField(verbose_name='weight')


