from django.shortcuts import render
from django.utils.http import urlencode
from django.http import HttpResponseRedirect, JsonResponse
from source import settings
from django.contrib.auth.decorators import login_required
from zeo import helper
from .models import ThreadTask

def index(request):
    return render(request, 'index.html')

def logout(request):
    return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
    logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
                 (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
    request.session.flush()
    return HttpResponseRedirect(logout_url)

def checkTask(request, id):
    task = ThreadTask.objects.get(pk=id)
    return JsonResponse({'is_done': task.is_done, 'task': task.task})

def startTask(request):
    task = ThreadTask()
    task.save()
    temp = helper.Helper()
    temp.query5(task.id)
    return JsonResponse({'id': task.id})

@login_required
def task1(request):
    temp = helper.Helper()
    array = temp.query1()
    return render(request, 'tasks/task1.html', {'Value': array[0], "Query": array[1]})

@login_required
def task2(request):
    temp = helper.Helper()
    array = temp.query2()
    count = 0
    sum = 0
    for i in array[1]:
        t = i["initial_release_date"].split("-")
        sum += int(t[0])
        count += 1
    avg = int(sum / count)

    return render(request, 'tasks/task2.html', {'Value': array[0], "Year": avg, "Query": array[2]})

@login_required
def task3(request):
    user = request.user
    temp = helper.Helper()
    name = user.first_name.split(" ")
    array = temp.query3(name[0], "Day")
    return render(request, 'tasks/task3.html', {'Value': array[0], "Value2": array[1], "Query": array[2], "fname": name[0], "lname": "Day"})

@login_required
def task4(request):
    temp = helper.Helper()
    array = temp.query4()
    return render(request, 'tasks/task4.html', {'Value': array[0], "Query": array[1]})

@login_required
def task5(request):
    return render(request, 'tasks/task5.html')

@login_required
def task6(request):
    temp = helper.Helper()
    array = temp.query6()
    return render(request, 'tasks/task6.html', {'Value': array[0], "Query": array[1]})

@login_required
def task7(request):
    if request.method == "POST":
        genre = request.POST['genre']
        year = request.POST['year']
        temp = helper.Helper()
        array = temp.query7(year, genre)
        return render(request, 'tasks/task7.html', {'Value': array, 'Genre': genre})
    return render(request, 'tasks/task7.html')

@login_required
def task8(request):
    if request.method == "POST":
        genre = request.POST['genre']
        director = request.POST['director']
        actor = request.POST['actor']
        year = request.POST['year']
        character = request.POST['character']
        movie = request.POST['movie']
        temp = helper.Helper()
        array = temp.query8(movie, actor, character, genre, year, director)
        if array != []:
            new_array = temp.getUid(array[0]["uid"])
            return render(request, 'tasks/task8.html', {'Value': new_array})
    return render(request, 'tasks/task8.html')