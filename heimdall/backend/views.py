from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import MyUser
import json
from .validator import UserForm, LoginForm
from icecream import ic
from .models import MyUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


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
        k = login(request,user_instance, backend='django.contrib.auth.backends.ModelBackend')
        print(k)

        success = {
            'status': 'OK',
            'message': 'user created successfully',
            'user':'user'
        }
        return JsonResponse(success)

    else:
        return JsonResponse(form.errors)



@csrf_exempt
def my_login(request):

    body = json.loads(request.body)
    print(body)
    form = LoginForm(body)

    if form.is_valid():

        data = form.cleaned_data
        user_instance = MyUser.objects.get(
            username = data['username'],
            password = data['password']
        )

        user_instance.save()
        k = login(request,user_instance, backend='django.contrib.auth.backends.ModelBackend')
        print(k)

        success = {
            'status': 'OK',
            'message': 'user created successfully',
            'user':'user'
        }
        return JsonResponse(success)

    else:
        return JsonResponse(form.errors)


@csrf_exempt
def token(request):

    if not request.user.is_authenticated:
        return JsonResponse({'isAuthenticated': False})

    return JsonResponse({'isAuthenticated': True})

@csrf_exempt
def catchall(request, url):
    ic("catchall")

    if not request.user.is_authenticated:
        response = redirect("http://localhost:3003" + url)
        return JsonResponse({'isAuthenticated': False})

    response = redirect("http://localhost:3003" + url)
    ic(response)
    u = 'http://localhost:3003/oauth/evernote/signin/'
    ic(u)
    return HttpResponseRedirect(u)



from django.utils.module_loading import import_module
from django.conf import settings
from django.contrib.auth import get_user
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend


def validate_token(request):

    sess_key = json.loads(request.body)['session']

    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore(sess_key)


    try:
        user_id = session[SESSION_KEY]
        backend_path = session[BACKEND_SESSION_KEY]
        backend = load_backend(backend_path)
        user = backend.get_user(user_id) or AnonymousUser()
        ic(user)
        res = {
            "status" : "ok",
            "user" : {
                "username" : user.username,
                "email" : user.email
            }
        }

    except KeyError:
        user = AnonymousUser()
        ic("anon user")

        res = {
            "status": "anon",
            "user": {}
        }

    return JsonResponse(res)