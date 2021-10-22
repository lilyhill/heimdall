from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from .validator import UserForm, LoginForm
from icecream import ic
from .models import MyUser
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.utils.module_loading import import_module
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, load_backend
from .utils import get_user_data


@csrf_exempt
def heimdall_signup(request):

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
def heimdall_login(request):

    body = json.loads(request.body)
    print(body)
    form = LoginForm(body)

    if form.is_valid():

        data = form.cleaned_data
        user_instance = MyUser.objects.get(
            username = data['username'],
            password = data['password']
        )
        if user_instance:
            login(request,user_instance, backend='django.contrib.auth.backends.ModelBackend')

            res = {
                'success': True,
                'user': get_user_data(user_instance)
            }
            return JsonResponse(res)
        else:
            res = {
                "success": False,
                "error": "user not found"
            }
            return JsonResponse(res, status=401)
    else:
        return JsonResponse(form.errors)



@csrf_exempt
def logout_user(request):

    logout(request)

    return JsonResponse({'logged_out': True})


@csrf_exempt
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
        u = get_user_data(user)
        res = {
            "status": "ok",
            "user": u
        }

    except KeyError:
        user = AnonymousUser()
        ic("anon user")

        res = {
            "status": "anon",
            "user": {}
        }

    return JsonResponse(res)


@csrf_exempt
def catchall(request, url):
    ic("catchall")

    if not request.user.is_authenticated:

        return JsonResponse({'isAuthenticated': False})

    response = redirect("http://localhost:3003" + url)
    ic(response)
    u = 'http://localhost:3003/' + url
    ic(u)
    return HttpResponseRedirect(u)
