from django.shortcuts import render
from django.db import transaction
import logging

# получаем экземпляр логгера, который будем использовать
logger = logging.getLogger(__name__)


@transaction.atomic     # декоратор для выполнения действий функции с БД в одной транзакции
def publish_blog_post(user_id, post_id, scope_value):
    '''Функция - представление для публикации статьи и списания баллов пользователя'''
    logger.info('Вызвана функция-представление publish_blog_post')  # вывод сообщения лога
    pass    # выполняем какие-либо действия(публикация и списание баллов в нашем примере)


def publish_blog_post_2(user_id, post_id, scope_value):
    '''Функция - представление для публикации статьи и списания баллов пользователя'''
    with transaction.atomic():  # контекст-менеджер для выполнения действий функции с БД в одной транзакции
        pass    # выполняем какие-либо действия(публикация и списание баллов в нашем примере)
