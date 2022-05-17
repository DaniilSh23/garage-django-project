from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.checks import messages
from django.shortcuts import render, redirect
from .forms import AuthForm, ExtendedRegisterForm, EditProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
import time
from django.contrib.auth.views import LoginView, LogoutView
# это вьюшка для аутентификации собственного производства
from .models import Profile


def login_view(request):
    now_time_hours = int(time.strftime('%H', time.localtime()))
    # с помощью метода запроса "method" проверяем тип запроса пользователя
    if request.method == 'POST':
        print(now_time_hours)
        # если это пост-запрос, то заполняем форму данными из запроса и кидаем её в отдельную переменную
        auth_form = AuthForm(request.POST)
        # проверяем введённые данные на валидность
        if auth_form.is_valid():
            # и фиксируем в отдельные переменные "чистые" данные из формы по ключам 'username' и 'password'
            username = auth_form.cleaned_data['username']
            password = auth_form.cleaned_data['password']
            # вызовем функцию authenticate
            user = authenticate(username=username, password=password)
            # если функция как-то там верно отработала
            # проверяем не 12 ли сейчас часов
            if now_time_hours == 13:
                print('попали в ошибку времени')
                auth_form.add_error('__all__', 'Ошибка. В это время мы закрыты.')
            else:
                if user:
                    # не суперпользователь ли наш товарищ логинящийся
                    if user.is_superuser:
                        print('Попали в ошибку про админа')
                        auth_form.add_error('__all__', 'Ошибка. Админам вход запрещён!')
                    else:
                        # смотрим значение атрибута активности у результата работы authenticate
                        if user.is_active:
                            # вызываем функцию login
                            login(request, user)
                            # и даём пользователю ответ
                            return HttpResponse('Вы успешно вошли в систему')
                        else:
                            auth_form.add_error('__all__', 'Ошибка. Учётная запись не активна!')
                else:
                    auth_form.add_error('__all__', 'Ошибка. Неверный логин или пароль!')
    # для всех остальных запросов берём пустую форму
    else:
        auth_form = AuthForm()
    # берём форму (пустую или с ранее отправленным данными, если они оказались не валидны)
    context = {'form': auth_form}
    # и отправляем её пользователю, с помощью функции render
    return render(request, 'app_users/auth_user.html', context=context)


# стандартная форма вьюхи для аутентификации
class StandardLoginView(LoginView):
    template_name = 'app_users/auth_user.html'


# костыльная вьюха для логаута
def logout_view(request):
    # функция ниже под капотом сама удаляет из БД токен сессии клиента
    logout(request)
    return HttpResponse('Вы успешно разлогинились. Ещё увидимся, пока!')


# стандартная вьюха для логаута
class StandardLogout(LogoutView):
    template_name = 'app_users/logout_user.html'  # это не обязательно, мы сюда все равно не попадём
    next_page = '/'  # если есть этот атрибут


# вьюха для регистрации пользователей
def register_view(request):
    # если тип запроса ПОСТ
    if request.method == 'POST':
        # заполняем форму данными из запроса и кидаем в переменную
        form = UserCreationForm(request.POST)
        # проверяем форму на валидность
        if form.is_valid():
            # на этой строке в БД попадут пароль и имя пользователя
            form.save()

            # аутентифицируем пользователя вручную, чтобы он повторно не вводил логин и пароль
            # берём имя пользователя из чистых данных формы
            username = form.cleaned_data.get('username')
            # берём пароль пользователя из чистых данных формы
            raw_password = form.cleaned_data.get('password1')
            # аутентифицируемся с этими данными и закидываем
            # результат функции аутентификации в переменную
            user = authenticate(username=username, password=raw_password)
            # логинемся через функцию, используя запрос результат функции аутентификации
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'app_users/register.html', {'form': form})


# вьюха для регистрации пользователей c доп.полями
def extended_register_view(request):
    if request.method == 'POST':
        form = ExtendedRegisterForm(request.POST)
        if form.is_valid():
            # при сохранении(добавлении) данных в ТБД о новом пользователе,
            # мы хватаем инстанс этого пользователя в переменную
            user = form.save()
            # берём из чистых данных, полученных из ПОСТ запроса город и ДР
            # date_of_birth = form.cleaned_data.get('date_of_birth')
            city = form.cleaned_data.get('city')
            email = form.cleaned_data.get('email')
            telephone = form.cleaned_data.get('telephone')
            discount_card_number = form.cleaned_data.get('discount_card_number')
            # создаём запись в таблице БД для модели Profile,
            # ссылаясь на user, взятого 2-мя строками выше
            Profile.objects.create(
                user=user,
                # date_of_birth=date_of_birth,
                city=city,
                email=email,
                telephone=telephone,
                discount_card_number=discount_card_number,
            )
            # всё, что ниже для аутентификации и логина пользователя после регистрации
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = ExtendedRegisterForm()
    return render(request, 'app_users/register.html', {'form': form})


def print_account_view(request):
    '''
    Отображение и редактирование данных аккаунта
    '''
    if request.method == 'POST':
        change_flag = False
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            users_profile_data = Profile.objects.get(user_id=request.user.pk)
            users_data = User.objects.get(pk=request.user.pk)
            users_data.username = form.cleaned_data['username']
            users_data.first_name = form.cleaned_data['first_name']
            users_data.last_name = form.cleaned_data['last_name']
            users_profile_data.email = form.cleaned_data['email']
            users_profile_data.discount_card_number = form.cleaned_data['discount_card_number']
            users_profile_data.telephone = form.cleaned_data['telephone']
            users_profile_data.city = form.cleaned_data['city']
            users_profile_data.avatar = form.cleaned_data['avatar']
            users_profile_data.save()
            users_data.save()

            return redirect('/users/account/')

    else:
        user_id = request.user.pk
        user_obj = User.objects.get(pk=user_id)
        profile_obj = user_obj.profile
        context = {
            'username': user_obj.username,
            'last_name': user_obj.last_name,
            'first_name': user_obj.first_name,
            'email': profile_obj.email,
            'discount_card_number': profile_obj.discount_card_number,
            'telephone': profile_obj.telephone,
            'city': profile_obj.city,
            'avatar': profile_obj.avatar,
        }
        avatar = profile_obj.avatar
        form = EditProfileForm(context)

        return render(request, 'app_users/account.html', context={'form': form, 'avatar': avatar})