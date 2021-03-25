from django.urls.base import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm

from .models import CustomUser


class CustomUserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
