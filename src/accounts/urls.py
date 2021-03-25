from django.urls import include, path

from .views import CustomUserCreateView


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('create/', CustomUserCreateView.as_view(), name='create')
]
