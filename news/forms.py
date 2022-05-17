from django import forms
from news.models import News, Comment, FilesForNews


class NewsModelForms(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'slug']


class NewsWithFiles(forms.ModelForm):
    class Meta:
        # берём модель файлов
        model = FilesForNews
        # от туда поле file
        fields = ['file']
        # назначаем этому полю виджет для загрузки нескольких файлов
        widgets = {'file': forms.ClearableFileInput(attrs={'multiple': True})}


class UploadFile(forms.Form):
    file = forms.FileField()


class CommentModelForms(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'


class FilterForm(forms.Form):
    slug = forms.SlugField(max_length=25)

    class Meta:
        verbose_name_plural = 'Слаги'
        verbose_name = 'Слаг'
