from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Trail, Activity
import requests
import json
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class TrailUpdate(UpdateView):
    model = Trail
    fields = ['name', 'location', 'country', 'description', 'length']


class TrailDelete(DeleteView):
    model = Trail
    success_url = '/trails/'


class TrailCreate(LoginRequiredMixin, CreateView):
    model = Trail
    fields = ['name', 'location', 'country', 'description', 'length']
    success_url = '/trails/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def about(request):
    return render(request, 'about.html')


@login_required
def trails_index(request):
    trails = Trail.objects.filter(user=request.user)
    return render(request, 'trails/index.html', {'trails': trails})


def trails_detail(request, trail_id):
    trail = Trail.objects.get(id=trail_id)
    activities_trail_doesnt_have = Activity.objects.exclude(
        id__in=trail.activities.all().values_list('id'))

    url = "https://api.openweathermap.org/data/2.5/weather?q={},{}&appid=74e08e29a06113b27d6bba189d6e2c27"

    r = requests.get(url.format(trail.location, trail.country)).json()

    city_weather = {
        'city': r['name'],
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
        'speed': r['wind']['speed'],
    }

    return render(request, 'trails/detail.html', {'city_weather': city_weather, 'trail': trail, 'activities': activities_trail_doesnt_have})


def assoc_activity(request, trail_id, activity_id):
    Trail.objects.get(id=trail_id).activities.add(activity_id)
    return redirect('detail', trail_id=trail_id)


def unassoc_activity(request, trail_id, activity_id):
    Trail.objects.get(id=trail_id).activities.remove(activity_id)
    return redirect('detail', trail_id=trail_id)


def weathers_index(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'Toronto'

    url = "https://api.openweathermap.org/data/2.5/find?q={}&units=metric&appid=74e08e29a06113b27d6bba189d6e2c27"

    r = requests.get(url.format(city)).json()

    context = {'all_weather': r['list']}

    return render(request, 'weathers/index.html', context)


def weathers_detail(request, city_id):

    url = "https://api.openweathermap.org/data/2.5/weather?id={}&units=metric&appid=74e08e29a06113b27d6bba189d6e2c27"

    r = requests.get(url.format(city_id))
    data = json.loads(r.text)

    city_weather = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
        'speed': data['wind']['speed'],
    }

    context = {'city_weather': city_weather}
    return render(request, 'weathers/details.html', context)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
