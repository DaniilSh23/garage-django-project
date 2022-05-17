from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app_users.models import Profile


class AuthForm(forms.Form):
    username = forms.CharField()
    # здесь мы указываем виджет, который нужен для поля паролей
    password = forms.CharField(widget=forms.PasswordInput)


# форма регистрации пользователя, как наследник от стандартной родительской формы
class ExtendedRegisterForm(UserCreationForm):
    # добавляем имя
    first_name = forms.CharField(max_length=30, required=False, help_text='Имя')
    # добавляем фамилию
    last_name = forms.CharField(max_length=30, required=False, help_text='Фамилия')
    # добавили поля из модели Profile
    # date_of_birth = forms.DateField(required=True, help_text='Дата рождения')
    city = forms.CharField(max_length=35, required=False, help_text='Город')
    discount_card_number = forms.IntegerField(required=False, help_text='Номер скидочной карты')
    telephone = forms.CharField(max_length=12, required=False, help_text='Номер телефона')

    class Meta:
        # форма будет для заполнения модели User
        model = User
        # отображаемые поля, тут те, что по умолчанию идёт в модели User
        # и соответствующей ему UserCreationForm, а также дополнительные,
        # что прописаны в форме и модели Profile
        fields = (
            'username',
            'last_name',
            'first_name',
            'email',
            'password1',
            'password2',
            'discount_card_number',
            'telephone',
            'city'
        )


class EditProfileForm(forms.Form):
    username = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    first_name = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    discount_card_number = forms.IntegerField(required=False)
    telephone = forms.CharField(required=False)
    city = forms.CharField(required=False)
    avatar = forms.ImageField(required=False, widget=forms.ClearableFileInput)




