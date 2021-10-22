from .models import MyUser

def get_user_data(MyUser):

    try:
        user = {
            "username": MyUser.username,
            "first_name": MyUser.first_name,
            "email": MyUser.email
        }

        return user
    except KeyError:
        return {}