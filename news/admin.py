from django.contrib import admin
from news.models import News, Comment, Author    # импортируем модель

# это для отображения вида Табулар
# class CommentInline(admin.TabularInline):
#     model = Comment


# это для отображения вида Стэктд
class CommentInline(admin.StackedInline):
    model = Comment


class NewsAdmin(admin.ModelAdmin):
    '''Этот класс используется для настроек админки.'''

    # выбираем поля, которые будем отображать в админке в списке всех новостей
    list_display = ['pk', 'title', 'created_at', 'update_at', 'is_published']
    # указываем по каким полям производить поиск в админке
    search_fields = ['title', 'pk']
    # по каким полям производить фильтр в админке
    list_filter = ['is_published']
    # это для вывода с помощью TabularInline
    inlines = [CommentInline]
    actions = ['mark_as_published', 'mark_as_draft', 'mark_as_review']

    # прописываем метод для админки (пимомо удаления)
    # он будет принимать в параметры запрос и последовательность из БД
    def mark_as_published(self, request, queryset):
        # обновляем в последовательности атрибут status нужным нам значением
        queryset.update(status='p')

    def mark_as_draft(self, request, queryset):
        queryset.update(status='d')

    def mark_as_review(self, request, queryset):
        queryset.update(status='r')

    # пропишем читабельные названия для наших методов
    mark_as_published.short_description = 'Перевести в статус опубликовано'
    mark_as_draft.short_description = 'Перевести в статус черновик'
    mark_as_review.short_description = 'Перевести в статус ревью'


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'from_news']
    search_fields = ['user_name', 'from_news']
    list_filter = ['from_news']
    actions = ['delete_by_admin']

    def delete_by_admin(self, request, queryset):
        queryset.update(comment_text='Удалено именем АДМИНИСТРАТОРА!')

    delete_by_admin.short_description = 'Удалить от имени администратора'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ['author_name']
    search_fields = ['author_name']
    list_filter = ['author_name']
    # группировка полей в админке
    fieldsets = (
        ('Имя автора', {
            'fields': ('author_name', 'author_last_name', 'author_second_name'),
            'description': 'Полное имя автора'
        }),
        ('Биографические данные', {
            'fields': ('birthday', 'biography'),    # поля для группировки
            'description': 'Подробно об авторе',    # описание группы полей
            'classes': ['collapse'], # CSS класс, чтобы поля были свёрнуты
        }),
        ('Контент от автора', {
            'fields': ('authors_news',),
            'description': 'Публикации автора',
        }),
    )


# регистрируем модель из нашего приложения
admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Author, AuthorAdmin)
