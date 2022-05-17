from django.urls import path
from app_users.views import login_view, StandardLoginView, logout_view, StandardLogout, register_view, \
    extended_register_view, print_account_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('standard_login/', StandardLoginView.as_view(), name='standard_login'),
    path('logout/', logout_view, name='logout'),
    path('standard_logout/', StandardLogout.as_view(), name='standard_logout'),
    path('register/', register_view, name='register_user'),
    path('ext_register/', extended_register_view, name='ext_register_user'),
    path('account/', print_account_view, name='account'),
]