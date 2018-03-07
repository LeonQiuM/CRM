from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout


# Create your views here.

def login(request):
    """
    用户登录验证
    :param request:
    :return:
    """
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        _email = request.POST.get('email')
        _password = request.POST.get('password')
        user = authenticate(request, username=_email, password=_password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                _next = request.GET.get("next",'/crm')
                return redirect(_next)
            else:
                status = "User is not active"
                return render(request, 'login.html', {'status': status})
        else:
            status = "invalid username or password"
            return render(request, 'login.html', {'status': status})


def account_logout(request):
    logout(request)
    return redirect('account_login')
