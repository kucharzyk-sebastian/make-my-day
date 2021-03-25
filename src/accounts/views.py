from django.shortcuts import redirect
from django.urls.base import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm

from .models import CustomUser


class CustomUserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)
