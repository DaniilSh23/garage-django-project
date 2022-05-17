from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=25)
    description = forms.CharField(max_length=50)
    file = forms.FileField()


class UploadPriceForm(forms.Form):
    '''
    Форма-образец для работы с загрузкой и обработкой файлов
    '''

    file = forms.FileField()


class MultiFileForm(forms.Form):
    '''
    Образец формы для загрузки нескольких файлов
    '''
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))