from rest_framework import viewsets
from django.contrib.auth.models import User
from drf_taste.serializers import UserSerializer


#  ModelViewSet содержит реализации для различных действий с API
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
