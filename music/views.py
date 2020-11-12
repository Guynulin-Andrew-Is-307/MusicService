from django.shortcuts import render
from django.views import View
from music.models import *
from django.http import Http404, HttpResponseNotFound, HttpResponseServerError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

# Create your views here.
class startmusic(View):
    def get(self, request, id, *args, **kwargs):
        try:
            son = Song.objects.get(id=id)
        except Song.DoesNotExist:
            raise Http404

        context = { 'qun': Song.objects.count(), 'song': son, 'isauth': request.user.is_authenticated }
        return render(request, 'song.html', context=context)

class listmusic(View):
    def get(self, request, *args, **kwargs):
        context = {'sosng': Song.objects.all(), 'user_c': User.objects.count(), 'isauth': request.user.is_authenticated}
        return render(request, 'index.html', context=context)
    def post(self, request, *args, **kwargs):
        if request.POST.get("sbros"):
            Song.objects.all().delete()
            User.objects.all().delete()

            userk = User.objects.create_user("Andrew_Guynulin_is407", "gaynulin2000@gmail.com", "1")
            nm = Song.objects.create(title="vitality", artist="mittsies-vitality.mp3", path_to_file="mittsies-vitality.mp3")
            nm.favorite_by.add(userk)

            # login(request, userk)
        elif request.POST.get("exit"):
            logout(request)
        return HttpResponseRedirect(reverse('main'))

class addfovorite(View):
    def get(self, request, *args, **kwargs):
        raise Http404
    def post(self, request, *args, **kwargs):
        song_id = request.POST.get("song_id")
        try:
            son = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            raise Http404
        son.favorite_by.add(request.user)
        son.save()
        return HttpResponseRedirect(reverse('song', args=[song_id]))


class authorization(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404
        context = { }
        return render(request, 'authorization.html', context=context)
    def post(self, request, *args, **kwargs):
        username = request.POST['name']
        password = request.POST['password']
        userk = authenticate(username=username, password=password)
        if userk is None:
            context = { 'info': 'Неверные данные'}
            return render(request, 'authorization.html', context=context)
        else:
            login(request, userk)
            return HttpResponseRedirect(reverse('main'))

class registration(View):
    def get(self, request, *args, **kwargs):
        context = {  }
        return render(request, 'registration.html', context=context)
    def post(self, request, *args, **kwargs):
        username = request.POST['name']
        password = request.POST['password']
        if username and password:
            if User.objects.filter(username=username).count() != 0:
                context = { 'info': 'Пользователь с таким именем уже есть в системе'}
                return render(request, 'registration.html', context=context)
            else:
                User.objects.create_user(username=username, password=password)
                nUk = authenticate(username=username, password=password)
                login(request, nUk)
                return HttpResponseRedirect(reverse('main'))
        else:
            context = {'info': '!Не все поля заполнены!'}
            return render(request, 'registration.html', context=context)

class addmusic(View):
    def get(self, request, *args, **kwargs):
        context = {  }
        return render(request, 'addmusic.html', context=context)
    def post(self, request, *args, **kwargs):
        title = request.POST['title']
        artist = request.POST['artist']
        path_to_file = request.POST['path_to_file']
        if title and artist and path_to_file:
            if Song.objects.filter(title=title, artist=artist).count() != 0:
                context = { 'info': '!Такая песня уже есть в библиотеке!'}
                return render(request, 'addmusic.html', context=context)
            else:
                Song.objects.create(title=title, artist=artist, path_to_file=path_to_file)
                return HttpResponseRedirect(reverse('main'))
        else:
            context = {'info': '!Не все поля заполнены!'}
            return render(request, 'addmusic.html', context=context)