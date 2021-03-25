from django.contrib.auth import views as auth_views
from django.urls import include, path

from .views import CustomUserCreateView


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True)),
    path('create/', CustomUserCreateView.as_view(), name='user_create'),
    path('', include('django.contrib.auth.urls'))
]
