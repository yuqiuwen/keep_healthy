from users.models import User


def fetch_user(request):
    auth = eval(request.META.get("HTTP_AUTHORIZATION"))

    user = User.objects.get(id=int(auth.get('user')), is_active=True)
    return user
