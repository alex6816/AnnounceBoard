import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from AdBoard.settings import DEFAULT_FROM_EMAIL
from callboard.models import Category
from sign.forms import RegisterUserForm, OneTimeCodeForm, LoginUserForm
from sign.models import OneTimeCode

menu = [{'title': 'Главная', 'url_name': 'ann_list'},
        {'title': 'Добавить объявление', 'url_name': 'ann_create'},
        {'title': 'Мои объявления', 'url_name': 'my_anns'},
        ]


class BaseRegisterView(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = 'signup.html'
    success_url = reverse_lazy('ann_list')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        passw = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        user = authenticate(username=username, password=passw)
        OneTimeCode.objects.filter(user=user).delete()
        numbers = list('0123456789')
        verify_code = ''
        for x in range(6):
            verify_code += random.choice(numbers)
        OneTimeCode.objects.create(user=user, code=verify_code)
        code = OneTimeCode.objects.get(user=user)
        print(user.email)
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Для подтверждения регистрации, пожалуйста введите код {code.code}',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False)
        return redirect('code_enter')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['cat_selected'] = 0
        context['title'] = 'Регистрация'
        context['cats'] = Category.objects.all()
        return context


def code_enter(request):
    form = OneTimeCodeForm()
    return render(request, 'code_enter.html', {'form': form, 'title': 'Код подтверждения', })


def verify(request):
    username = request.POST['username']
    code = request.POST['code']
    user = User.objects.get(username=username)
    if OneTimeCode.objects.filter(code=code, user=user).exists():
        user.save()
        login(request, user)
        OneTimeCode.objects.filter(user=user).delete()
    else:
        return render(request, 'code_enter.html', {'error': 'Ошибка ввода имени или пароля', })
    return redirect('ann_list')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('ann_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['cat_selected'] = 0
        context['title'] = 'Авторизация'
        context['cats'] = Category.objects.all()
        return context

def logout_user(request):
    logout(request)
    return redirect('login')

