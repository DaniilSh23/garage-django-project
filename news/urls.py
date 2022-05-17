from django.urls import path
from news.views import NewsListView, news_added_successfully, EditNews, NewsDetailView, \
    PublicationNews, HeadPage, add_news_with_many_files, upload_many_news_from_file

urlpatterns = [
    # path('', HeadPage.as_view(), name='head'),
    path('', NewsListView.as_view(), name='news_list'),
    path('add_news/', add_news_with_many_files, name='add_news'),
    path('news_added/', news_added_successfully, name='news_added'),
    path('edit_news/<int:news_id>/', EditNews.as_view(), name='edit_news'),
    path('publication_news/<int:news_id>/', PublicationNews.as_view(), name='publication_news'),
    path('detail_news/<int:news_pk>/', NewsDetailView.as_view(), name='detail_news'),
    path('add_many_news/', upload_many_news_from_file, name='add_many_news'),
]