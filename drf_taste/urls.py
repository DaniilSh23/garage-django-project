from django.urls import path
from rest_framework import routers
from drf_taste.api import UserViewSet
from drf_taste.views import items_list, ItemsModelList, ItemsModelListMixin, ItemsModelListMixinVol2

# здесь мы используем router, который входит в поставку DRF
# он автоматически создаёт и связывает url приложения с представлением
# таким образом у нас автоматически сгенерируются url для CRUD модели
# и свяжутся с нужными методами представления
router = routers.DefaultRouter()
router.register('users', UserViewSet)
# urlpatterns = router.urls

# это для урока 13.3
urlpatterns = [
    path('items/', items_list, name='items_list'),
    path('model_items/', ItemsModelList.as_view(), name='model_item'),
    path('mixin_items/', ItemsModelListMixin.as_view(), name='mixin_item'),
    path('filter_items/', ItemsModelListMixinVol2.as_view(), name='filter_items')
]