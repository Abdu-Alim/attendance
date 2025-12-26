from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def is_admin(user):
    try:
        return user.userprofile.role == 'admin'
    except:
        return False

def admin_required(view_func):
    decorated_view_func = user_passes_test(
        is_admin,
        login_url='/login/',
        redirect_field_name=None
    )(view_func)
    return decorated_view_func

def employee_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper