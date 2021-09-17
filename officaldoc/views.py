from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm


# Create your views here.


def index(request):
    template = loader.get_template('index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def user_login(request):
    form = LoginForm()
    template = loader.get_template('login.html')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.GET.get('next'):
                    return HttpResponseRedirect(request.GET.get("next"))
                else:
                    return HttpResponseRedirect('/')
            else:
                messages.error(request, '使用者尚未啟用，請聯絡管理員。')
                return HttpResponseRedirect('/login/')
        else:
            messages.error(request, '使用者帳號或密碼有誤，請再次輸入。')
            return HttpResponseRedirect('/login/')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
