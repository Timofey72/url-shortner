from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from short.models import Link


def index(request):
    return render(request, 'short/index.html')


def about(request):
    return render(request, 'short/about.html')


@login_required
def profile(request):
    user = User.objects.get(id=request.user.id)
    context = {
        'user': user
    }

    if request.method == "POST":
        try:
            username = request.POST.get('username')
            user.username = username
            user.email = request.POST.get('email')
            user.save()
            context['message'] = 'Данные успешно обновлены!'
        except IntegrityError:
            context['error'] = 'Пользователь с таким именем уже существует!'

    return render(request, 'short/profile.html', context)


@login_required
def link(request):
    user = request.user
    links = Link.objects.filter(user=user)
    context = {'links': links}
    if request.method == "POST":
        long_link = request.POST['long_link']
        short_link = request.POST['short_link']
        if long_link and short_link:
            if not Link.objects.filter(short_link=short_link):
                Link.objects.create(
                    user=user,
                    long_link=long_link,
                    short_link=short_link,
                )
                return render(request, 'short/link.html', context)
            else:
                return render(request, 'short/link.html', context | {'error': 'Ссылка уже существует'})
        else:
            return render(request, 'short/link.html', context | {'error': 'Введите правильные данные'})
    else:
        return render(request, 'short/link.html', context)


def open_link(request, link_str):
    link_redirect = get_object_or_404(Link, short_link=link_str, user=request.user).long_link
    return redirect(link_redirect)
