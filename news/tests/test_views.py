from django.test import TestCase
from django.urls import reverse
from news.models import News


class TestHomePage(TestCase):
    def test_home_page(self):
        '''
        Функция - тест для проверки главной странице на код ответа сервера == 200
        и наличие на странице текста 'Список новостей'
        '''

        # формирует url для будущего запроса
        # функция reverse принимает имя url, прописанного в urlpatterns в параметре name
        url = reverse('head')
        # отправляем GET-запрос и получаем ответ в переменную
        response = self.client.get(url)
        # проверим код ответа сервера, если ОК, то он равен 200
        self.assertEqual(response.status_code, 200)
        # проверяем наличие определённого текста на странице
        # также в этом ассерте можно было сразу проверить и код ответа сервера
        self.assertContains(response, 'Список новостей', status_code=200)


class TestSendMail(TestCase):
    def test_post_restore_password(self):
        '''
        Тест для проверки отправки письма с восстановлением пароля
        '''

        # делаем ПОСТ-запрос на сервер и получаем ответ
        # в запрос передаём name из urlpatterns и словарь со значением ключа email
        response = self.client.post(reverse('head'), {'slug': 'slug'})
        # проверяем, что получили код статуса 200
        self.assertEqual(response.status_code, 200)
        # импортируем outbox - используется для хранения писем теста
        from django.core.mail import outbox
        # проверяем, что длина outbox == 1, то есть туда упало 1 письмо с восстановлением пароля
        self.assertEqual(len(outbox), 1)


class TestHeadPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        '''
        Устанавливаем начальные данные для новости (вносим записи в БД для теста)
        '''
        for i_news in range(1, 11):
            # устанавливаем разные слаги для чётных и нечётных новостей
            if i_news % 2 == 0:
                slug = '222'
            else:
                slug = '111'
            News.objects.create(
                title=f'test_news_{i_news}',
                content=f'test_news_content_{i_news}',
                slug=slug
            )

    def test_news_num_slug_template(self):
        '''
        Тест для проверки статуса кода ответа сервера,
        используемого шаблона
        длины списка новостей, выводимого в шаблон == 10
        наличие на странице определённых тегов
        '''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/news_list.html')
        self.assertTrue(len(response.context['news_list']) == 10)
        # наличие поля для ввода слага
        # хотел и другие теги сразу проверить, но почему тег <form> не нашёл,
        # а также если указывал несколько тегов через пробел, то тоже тест не проходил
        # можно использовать цикл, в котором пробегаться по нужным тегами и по одному их тестить
        self.assertContains(
                            response,
                            text='<input type="text" name="slug" maxlength="25" required id="id_slug"> ',
                            html=True
        )

    def test_filter_by_slug_with_post_req(self):
        '''
        Тест для проверки вывода новостей после фитрации по слагу
        '''
        for i_slug in ['111', '222']:
            response = self.client.post('/', {'slug': i_slug})
            self.assertTemplateUsed(response, 'news/news_list.html')
            self.assertTrue(len(response.context['news_list']) == 3)
            for i_news in response.context['news_list']:
                self.assertTrue(i_news.slug, '56435')


