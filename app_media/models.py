from django.db import models


class SaveFiles(models.Model):
    '''
    Модель-пример для работы с файлами
    '''
    # создаём поле для хранения файлов и указываем параметр upload_to,
    # который определяет путь к месту хранения загруженных файлов
    file = models.FileField(upload_to='files/')
