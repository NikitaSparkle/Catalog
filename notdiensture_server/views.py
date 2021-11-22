import json
import random
from urllib import request

from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from notdiensture_server.forms import SingUpForm, ConfirmForm, LoginForm
from notdiensture_server.models import User, Country, EmergencyServes, History


def registration(request):
    submitbutton = request.POST.get("submit")
    form = SingUpForm(request.POST or None)
    if form.is_valid():
        if form.cleaned_data.get("password") == form.cleaned_data.get("password1"):
            User.objects.create_user(username=form.cleaned_data.get("email"),
                                     email=form.cleaned_data.get("email"),
                                     phone_number=form.cleaned_data.get("phone"),
                                     password=form.cleaned_data.get("password"),
                                     country=form.cleaned_data.get("country"))
            code = str(random.randint(1111, 9999))
            print(send_mail(
                'code',
                code,
                'zachtomneetoaaa@gmail.com',
                [form.cleaned_data.get("email")]
            ))
            user = authenticate(request, username=form.cleaned_data.get("email"),
                                password=form.cleaned_data.get("password"))
            login(request, user)
            request.session.setdefault('code', 0)
            request.session['code'] = code
            print(request.session)
            print(request.COOKIES)
            return redirect(confirm)

    return render(request, 'registration.html', {'form': form, 'submitbutton': submitbutton})


def loginPage(request):
    if request.user.is_active:
        return redirect(index)
    submitbutton = request.POST.get("submit")

    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(request, username=form.cleaned_data.get("username"),
                            password=form.cleaned_data.get("password"))
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            form.add_error(None, 'Имя пользователя или пароль не верны')
            form.clean()
            return render(request, 'login.html', {'form': form, 'submitbutton': submitbutton})
    return render(request, 'login.html', {'form': form, 'submitbutton': submitbutton})


def confirm(request):
    submitbutton = request.POST.get("submit")
    print(request.session['code'])
    code = request.session['code']
    form = ConfirmForm(request.POST or None)
    if form.is_valid():
        if form.cleaned_data.get("code") == code:
            return redirect(index)
        else:
            print("ne ok")
    return render(request, 'confirm.html', {'form': form, 'submitbutton': submitbutton})


def index(request):
    user = User.objects.get(id=request.user.id)
    serves = EmergencyServes.objects.filter(country=user.country).values()
    print(serves)
    return render(request, 'index.html', {'serves': serves})

def history(request):
    serv = json.loads(request.body.decode('utf-8'))
    print(serv)
    History.objects.create(service=EmergencyServes.objects.get(id=serv['serv']),
                           user=User.objects.get(id=request.user.id))
    # if request.method == 'POST':
    #     print(request.POST["test"])
    return HttpResponse(201)
