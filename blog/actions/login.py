from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate, login, logout


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/blog")

    return render(request, 'blog/login.html', {})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/blog")
