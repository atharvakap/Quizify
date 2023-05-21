from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.contrib import messages
from datetime import datetime
import random


# Create your views here.
def index(request):
    return render(request, 'index.html')


def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/quizselect')
        else:
            return render(request, 'login.html')

    return render(request, 'login.html')


def logoutuser(request):
    logout(request)
    return redirect('/login')


def quizselect(request):
    if request.user.is_anonymous:
        return redirect('/login')
    return render(request, 'quizselect.html')


def quizpage(request):
    if request.user.is_anonymous:
        return redirect('/login')

    question_objs = list(Question.objects.all())
    data = []
    random.shuffle(question_objs)
    for question_obj in question_objs:
        data.append({
            "category": question_obj.category.category_name,
            "question": question_obj.question,
            "marks": question_obj.marks,
            "answers": question_obj.get_answers()
        })

    payload_question = []
    payload_answers = []
    for element in data:
        payload_question.append(element["question"])
        temp = []
        for i in range(4):
            temp.append(element["answers"][0]["answer"])
        payload_answers.append(temp)

    print(payload_answers)
    payload = {"status": True, "data": payload_question, "data_options": payload_answers}
    context = {'category': request.GET.get('category')}
    return render(request, 'quizpage.html', payload)


def score(request):
    if request.user.is_anonymous:
        return redirect('/login')

    context = {'category': request.GET.get('category')}

    return render(request, 'score.html', context)


def signupuser(request):
    if request.method == "POST":
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        desc = request.POST.get('message')

        contact = Usercreds(name=name, username=username, email=email, password=password, desc=desc, date=datetime.today())
        # print("Object created")
        contact.save()

        flname = name.split()
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = flname[0]
        myuser.last_name = flname[1]
        myuser.save()
        messages.success(request, 'Your message has been sent!')
        return redirect('/')

    return render(request, 'index.html')


def get_quiz(request):
    try:
        question_objs = list(Question.objects.all())
        data = []
        random.shuffle(question_objs)
        for question_obj in question_objs:
            data.append({
                "category": question_obj.category.category_name,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "answers": question_obj.get_answers()
            })
        payload = {"status": True, "data": data}
        return JsonResponse(payload)
    except Exception as e:
        print(e)
    return HttpResponse('Something went wrong!!')
