from django.shortcuts import HttpResponse, render, redirect
# from django.urls import redirect
from .forms import UserUpdateForm
# djangoning user modelini import qildim
from django.contrib.auth.models import User, Group

from new.models import New
from extra.models import Carusel


def home(request):
    news = New.objects.all()[:3]
    carusels = Carusel.objects.all()
    return render(request, 'pages/home.html', {'news': news, 'carusels': carusels})


def users_view(request):
    users = User.objects.all()
    return render(request, 'accounts/users.html', {"users": users})


def update_view(request, pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()
        return redirect('users')
    form = UserUpdateForm(initial={'supervisor': user})
    return render(request, 'accounts/update_user.html', {"form": form})


def groups_view(request):
    groups = Group.objects.all()
    return render(request, 'accounts/groups.html', {"groups": groups})
 