from django.shortcuts import redirect
from functools import wraps

def session_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('username'):
            return redirect('loginpage')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
