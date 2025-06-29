from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page # импортируем декоратор для кэширования отдельного представления
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/profile.html'

@login_required
@cache_page(60 * 5) # в аргументы к декоратору передаём количество секунд, которые хотим, чтобы страница держалась в кэше.
## Внимание! Пока страница находится в кэше, изменения, происходящие на ней, учитываться не будут!
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/')
