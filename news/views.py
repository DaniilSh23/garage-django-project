from _csv import reader

from django.core import serializers
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views import generic, View
from news.forms import *
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page


class NewsListView(generic.ListView):
    model = News
    # эта строка не обязательна, ей меняем шаблон,
    # по умолчанию будет взят шаблон с <названием используемой модели>_list.html
    template_name = 'news_list.html'
    # не обязательна, задаёт имя переменной в шаблоне для этой вьюхи
    context_object_name = 'news_list'
    # указываем какие именно данные из модели нам нужны
    queryset = News.objects.all()


class NewsAddFormView(View):
    def get(self, request):
        # проверяем, чтобы пользователь был аутентифицирован и авторизирован
        if not request.user.is_authenticated or not request.user.profile.verification_flag:
            return HttpResponse('К сожалению, вы не прошли верификацию.')
        add_news_form = NewsModelForms()
        return render(request, 'news/add_news.html', context={'add_news_form': add_news_form})

    def post(self, request):
        '''
        !!!Важен такой порядок: СНАЧАЛА валидация данных от пользователя,
        а ПОТОМ дополнение своими данными!!!
        '''
        # принимаем запрос, там не все данные для формы, но многие у нас по дефаулту
        # заполняются определёнными значениями и модель сама их себе запишет, но потом
        add_news_form = NewsModelForms(request.POST)
        # здесь мы проверяем данные на валидность
        if add_news_form.is_valid():
            # после валидации мы можем использовать "чистые" данные
            title = add_news_form.cleaned_data.get('title')
            content = add_news_form.cleaned_data.get('content')
            # формируем словарь для модели, в котором прописываем те данные,
            # которые нужно ввести, но выбирать пользователю их нельзя
            data_to_model = {
                'title': title,
                'content': content,
                'status': 'r',  # вот статус, например. Я с ним заебался.
            }
            # создаём модель с нужными данными, словарь распаковываем
            News.objects.create(**data_to_model)
            return HttpResponseRedirect('/news_added/')
        return HttpResponse(f'Ошибка в следующем: {add_news_form.errors}')


def news_added_successfully(request):
    return render(request, 'news/news_added_succesfully.html')


class EditNews(View):
    def get(self, request, news_id):
        edited_news = News.objects.get(pk=news_id)
        edited_news_form = NewsModelForms(instance=edited_news)
        return render(request, 'news/edit_news.html',
                      context={'edited_news_form': edited_news_form, 'news_id': news_id})

    def post(self, request, news_id):
        edited_news = News.objects.get(pk=news_id)
        edited_news_form = NewsModelForms(request.POST, instance=edited_news)

        if edited_news_form.is_valid():
            edited_news.save()
            return HttpResponseRedirect('/news_added/')
        else:
            return render(request, 'news/edit_news.html',
                          context={'edited_news_form': edited_news_form, 'news_id': news_id})


class NewsDetailView(View):
    def get(self, request, news_pk):
        news_detail = News.objects.get(pk=news_pk)
        all_comments = Comment.objects.filter(from_news=news_detail)
        comment_form = CommentModelForms()
        if FilesForNews.objects.filter(news_id=news_pk):
            news_files = FilesForNews.objects.filter(news_id=news_pk)
        else:
            news_files = None
        return render(request, 'news/news_detail.html', context={
            'news_detail': news_detail,
            'comment_form': comment_form,
            'all_comments': all_comments,
            'news_files': news_files,
        })

    def post(self, request, news_pk):
        if request.user.is_authenticated:
            # вытягиваю данные, поступившие из пост запроса(нам нужен только текст коммента)
            form_data_comment_text = CommentModelForms(request.POST).data.get('comment_text')
            # беру ту новость, которую комментировали
            news_detail = News.objects.get(pk=news_pk)
            # беру инстанс пользователя, который комментировал (это нужно для FK на него)
            user_foreign = User.objects.get(pk=request.user.pk)
            # заполняю словарик с данными для модели комментария
            data_to_model = {
                'user_name': request.user,
                'from_news': news_detail,
                'user': user_foreign,
                'comment_text': form_data_comment_text
            }
            # заполняю инстанс коммента данными из словарика
            # походу форма принимает словарь, в отличие от модели
            this_fucking_comment = CommentModelForms(data_to_model)

        else:
            # вытягиваю данные, поступившие из пост запроса(нам нужен текст коммента)
            form_data_comment_text = CommentModelForms(request.POST).data.get('comment_text')
            # вытягиваю данные, поступившие из пост запроса(нам нужно имя пользователя)
            form_data_user_name = CommentModelForms(request.POST).data.get('user_name')
            # беру ту новость, которую комментировали
            news_detail = News.objects.get(pk=news_pk)
            # комментировал аноним, поэтому для него None
            user_foreign = None
            # заполняю словарик с данными для модели комментария
            data_to_model = {
                'user_name': ' '.join(['[аноним]', form_data_user_name]),
                'from_news': news_detail,
                'user': user_foreign,
                'comment_text': form_data_comment_text
            }
            # заполняю инстанс коммента данными из словарика
            # походу форма принимает словарь, в отличие от модели
            this_fucking_comment = CommentModelForms(data_to_model)

        # проходим валидацию
        if this_fucking_comment.is_valid():
            # cоздаю запись в ТБ коммента(модели Comment), а не формы
            # это, в общем, так как-то там работает
            this_fucking_comment.save()
        return HttpResponseRedirect(f'/detail_news/{news_pk}/')


class PublicationNews(View):
    def post(self, request, news_id):
        # берём объект пользователя
        user = request.user
        # проверяем наличие разрешения
        # для стандартных разрешений Джанго работало так:
        # <приложение>.<разрешение>_<модель>
        # для наших разрешений актуален такой синтаксис
        # <имя приложения>.<имя разрешения>
        if request.user.has_perm('news.permit'):
            # заполняем форму данными пост запроса, чтобы проверить их валидность
            form = NewsModelForms(request.POST)
            if form.is_valid():
                # берём редактируемую новость
                this_news = News.objects.get(pk=news_id)
                # меняем значения её атрибутов
                this_news.status = 'p'
                this_news.title = form.cleaned_data.get('title')
                this_news.content = form.cleaned_data.get('content')
                this_news.is_published = True
                # обязательно сохраняем изменения в ТБД
                this_news.save()
                return HttpResponse('Новость опубликована')
            return HttpResponse(f'Ошибки: {form.errors}')
        return HttpResponse('У вас отсутствуют права для публикации новостей')


class HeadPage(View):
    # кэшируем страницу на 30 секунд
    @cache_page(30)
    def get(self, request):
        news_list = News.objects.all()
        filter_form = FilterForm()
        return render(request, 'news/news_list.html', context={'news_list': news_list, 'filter_form': filter_form})

    def post(self, request):
        form = FilterForm(request.POST)
        if form.is_valid():

            # функция для отправки писем
            # (нужен импорт: from django.core.mail import send_mail)
            send_mail(
                # subject - заголовок письма
                subject='Кто-то фильтрует на главной',
                # message - текст письма
                message=f'пользователь id={request.user.pk} username={request.user.username} фильтрует базар на сайте',
                # from_email - от кого письмо
                from_email='admin@company.com',
                # recipient_list - список получателей
                recipient_list=['any@company.ru']
            )

            slug = form.cleaned_data.get('slug')
            news_list = News.objects.filter(slug=slug)
            filter_form = FilterForm()
            return render(request, 'news/news_list.html', context={'news_list': news_list, 'filter_form': filter_form})
        return HttpResponse(f'Что-то не так: {form.errors}')


def add_news_with_many_files(request):
    '''
    Добавление новости со множеством файлов
    '''

    if request.method == 'POST':
        if request.user.is_authenticated:
            form_news = NewsModelForms(request.POST)
            form_file = NewsWithFiles(request.POST, request.FILES)

            if form_news.is_valid() and form_file.is_valid():
                files = request.FILES.getlist('file')   # file - имя поля в модели
                news_instance = form_news.save()
                print(f"Айди новости: {news_instance}")
                for i_file in files:
                    file_instance = FilesForNews(file=i_file, news=news_instance)
                    file_instance.save()
                return redirect('/news_added/')
        else:
            return redirect('/')
    else:
        news_form = NewsModelForms()
        files_form = NewsWithFiles()
    return render(request, 'news/add_news.html', {'news_form': news_form, 'files_form': files_form})


def upload_many_news_from_file(request):
    '''
    Функция для добавления нескольких новостей из файла csv
    '''

    # добавление доступно только аутентифицированным пользователям
    if request.user.is_authenticated:
        if request.method == 'POST':
            # кидаем в форму ПОСТ-запрос и файл из запроса
            file_form = UploadFile(request.POST, request.FILES)
            if file_form.is_valid():
                # берём "чистые" данные по ключу file
                # получим название загруженного файла
                file_data = file_form.cleaned_data['file']
                print(f'Чистые данные по ключу file {file_data}')
                # читаем данные файла
                # прочтётся всё, что не кирилица
                file_data = file_data.read()
                print(f'Читаем данные файла {file_data}')
                # декодируем данные файла
                # часто для русских букв используют кодировку UTF-8
                # но с 11 виндой все файлы кодируются в windows-1251
                file_data = file_data.decode('windows-1251')
                print(f'Декодируем данные file {file_data}')
                # сплитуем данные файла по переносу строки
                file_data_lst = file_data.split('\n')
                print(f'Смотрим, что будет когда сплитанём по новой строке {file_data_lst}')
                # используем из библиотеки csv метод reader
                csv_reader = reader(file_data_lst, delimiter=';', quotechar='"')
                print(f'csv_reader: {csv_reader}')
                # идём по списку из строк
                for i_line in csv_reader:
                    print(f'Строка в csv reader: {i_line}')
                    # Строка в csv reader: i_line будет представлять с собой список,
                    # элементы - содержимое заполненных ячеек
                    # разбиты они будут по значению delimiter в методе reader()
                    # поэтому если там стоит не тот разделитель, то список получится из 1 элемента
                    # каждую итерацию добавляем в инстанс новости данные и сохраняем
                    # заголовок у нас в нулевой колонке был, контен - в первой, слаг - 2
                    # и не забываем сохранить всё в БД
                    try:
                        News(title=i_line[0], content=i_line[1], slug=i_line[2]).save()
                    except IndexError:
                        # если будут проблемы с индексами элементов, то мы пойдём дальше
                        # это полезно, если в файле случайно добавили пустую строку в конце
                        # она будет считаться как итерируемый объект, но в ней не будет элементов
                        # и мы получим IndexError, а наш код сломается
                        continue
                return HttpResponse(
                    'Новости успешно добавлены\n'
                    '<p><a href="/">Перейти к списку новостей</a></p>'
                                    )
        # если пришел не ПОСТ-запрос
        else:
            file_form = UploadFile()
            context = {'file_form': file_form}
            return render(request, 'news/add_many_news.html/', context=context)
    # для анонимного пользователя возврат на главную
    else:
        return redirect('/')


# кэшируем страницу на 30 секунд
@cache_page(30)
def cache_example(request):
    return HttpResponse('Gooood cache for 30 sec')


def views_by_format(request):
    '''Представление для выполнение запроса клиента в случае передачи формата в запросе из указанных'''

    # берём формат
    format = request.GET['format']
    # проверяем, что формат не входит в заданный список
    if format not in ['xml', 'json']:
        # возвращаем ответ о неудачном запросе
        return HttpResponseBadRequest()
    # сериализуем под формат наши данные
    data = serializers.serialize(format, News.objects.all())
    # отдаём клиенту наши данные
    return HttpResponse(data)

