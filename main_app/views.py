from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from .models import Trail, Activity
import requests
import json


class TrailUpdate(UpdateView):
    model = Trail
    fields = ['name', 'location', 'description', 'length']


class TrailDelete(DeleteView):
    model = Trail
    success_url = '/trails/'


class TrailCreate(CreateView):
    model = Trail
    fields = ['name', 'location', 'description', 'length']
    success_url = '/trails/'

def about(request):
    return render(request, 'about.html')


def trails_index(request):
    trails = Trail.objects.all()
    return render(request, 'trails/index.html', {'trails': trails})


def trails_detail(request, trail_id):
    trail = Trail.objects.get(id=trail_id)
    activities_trail_doesnt_have = Activity.objects.exclude(
        id__in=trail.activities.all().values_list('id'))

    url = "https://api.openweathermap.org/data/2.5/find?q={}&units=metric&appid=74e08e29a06113b27d6bba189d6e2c27"

    print(trail.location)
    r = requests.get(url.format(trail.location))
    c = list(filter(lambda item : item['sys']['country'] == 'CA', r['list']))[0]
    data = json.loads(r)
    

    city_weather = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'icon': data['weather'][0]['icon'],
        'speed': data['wind']['speed'],
    }

    context = {'city_weather': city_weather }
    # context = { 'all_weather': r['list'] }
    return render(request, 'trails/detail.html', {'trail': trail, 'activities': activities_trail_doesnt_have}, context)


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
 
    
    context = { 'all_weather': r['list'] }
        
    return render(request, 'weathers/index.html', context )


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

    context = {'city_weather': city_weather }
    return render(request, 'weathers/detail.html', context)
