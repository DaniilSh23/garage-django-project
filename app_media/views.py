import datetime
from _csv import reader
from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app_media.forms import UploadFileForm, UploadPriceForm, MultiFileForm
from app_media.models import SaveFiles
from django.utils.translation import gettext as _
from django.utils.formats import date_format


def upload_file(request):
    # проверяем ПОСТ запрос ли это
    if request.method == 'POST':
        # заполняем форму данными из пост запроса и отдельно ОБЪЕКТ ФАЙЛА из запроса(это важно)
        upload_file_form = UploadFileForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            # берём файл из запроса в отдельную переменную(по ключу 'file' в нашем случа)
            file = request.FILES['file']
            # возвращаем имя файла и статус 200 (хз по поводу этих статусов, надо почитать)
            return HttpResponse(content=file.name, status=200)
    # а если запрос НЕ ПОСТ
    else:
        # берём форму в переменную
        upload_file_form = UploadFileForm()
        # кидаем её в контекст, как словарь
        context = {'form': upload_file_form}
        # рендерим пользователю, чтобы заполнял
        return render(request, 'app_media/download_file.html', context=context)


def update_prices(request):
    '''
    Функция-представление - пример обработки файла csv
    и изменений данных на сайте данными из файла
    '''
    if request.method == 'POST':
        # вставляем в форму данные ПОСТ-запроса и файл из запроса клиента
        upload_file_form = UploadPriceForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            # берём "чистые" данные, обращаемся по ключу file и читаем полученный файл
            price_file = upload_file_form.cleaned_data['file'].read()
            # декодируем полученную инфу из файла и сплитуем по символу переноса строки
            price_str = price_file.decode('utf-8').split('\n')
            # применяем функцию reader из библиотеки csv, в качестве параметров передаются:
            # объект с информацией, delimeter - в нём определяем символ,
            # который будет служить разделителем для ячеек с инфой (по умолчанию это запятая)
            # quotechar - символ, в который будет обёрнут разделитель или спец.символы типо переноса строки
            csv_reader = reader(price_str, delimiter=',', quotechar='"')
            # далее итерируемся по данным из файла построчно
            for row in csv_reader:
                # артикул будем брать из нулевого столбца, а цену из первого
                # а Decimal - это что-то отсюда from decimal import Decimal
                # на модель не обращаем внимание, написал любую, чтобы просто не было ошибки
                SaveFiles.objects.filter(code=row[0]).update(price=Decimal(row[1]))
            return HttpResponse(content='Цены успешно изменены', status=200)
    else:
        upload_file_form = UploadPriceForm()

    context = {'form': upload_file_form}
    return render(request, 'путь к шаблону', context=context)


def upload_many_files(request):
    '''
    Функция-представления, образец для загрузки нескольких файлов
    '''

    if request.method == 'POST':
        form = MultiFileForm(request.POST, request.FILES)
        if form.is_valid():
            # здесь небольшое отличие
            # берём все загруженные файлы в виде списка
            files = request.FILES.getlist('file_field')
            # итерируемся по списку с файлами
            for i_file in files:
                # берём каждый из файлов и добавляем его в модель для загрузки одного файла
                instance = SaveFiles(file=i_file)
                # сохраняем новую инфу в БД
                instance.save()
            return redirect('/')

    else:
        form = MultiFileForm()
    return render(request, 'путь к шаблону', {'form': form})


def translation_example(request, *args, **kwargs):
    # тут применяем вид форматирования строк через %
    # синтаксис записи такой %(<переменная>)<тип данных>
    # после строки указывается % и в словаре передаются
    # {<ключ - указанная нами в строке переменная>: значение}
    # в метод gettext передаём чисто строку, без записей форматирования
    # gettext заменяется на нижнее подчёркивание _, благодаря записи 'as _' при импорте
    greating_messages = _('Hello there! Today is %(date)s %(time)s') % {
        # применим метод date_format к значениям форматированной строки,
        # чтобы они изменялись согласно выбранной пользователем локализации
        # используем для этого параметры метода format(для короткого формата даты) и use_l10n (локализация)
        'date': date_format(datetime.datetime.now().date(), format='SHORT_DATE_FORMAT', use_l10n=True),
        'time': datetime.datetime.now().time(),
    }
    return render(request, 'app_media/translation_example.html', context={'greating_messages': greating_messages})











