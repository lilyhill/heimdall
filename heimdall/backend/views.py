from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import MyUser
import json
from .validator import UserForm
from icecream import ic
from .models import MyUser

# Create your views here.
@csrf_exempt
def signup(request):

    body = json.loads(request.body)
    form = UserForm(body)
    ic(form.errors)
    ic(json.loads(request.body))

    ic(MyUser)

    if form.is_valid():

        data = form.cleaned_data
        user_instance = MyUser.objects.create(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )

        user_instance.save()

        success = {
            'status': 'OK',
            'message': 'user created successfully',
            'user':'user'
        }
        return JsonResponse(success)
    else:
        return JsonResponse(form.errors)



@csrf_exempt
def login(request):

    return JsonResponse({'input':'login'})

@csrf_exempt
def token(request):
    return JsonResponse({'input': 'token'})