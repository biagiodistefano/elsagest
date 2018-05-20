import re
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout

EXEMPT_URLS = [settings.LOGIN_URL.lstrip('/')] + [url for url in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')

        url_is_exempt = any(url.startswith(path) for url in EXEMPT_URLS)

        if path == 'logout/':
            logout(request)

        if request.user.is_authenticated and url_is_exempt:
            return None
        elif request.user.is_authenticated or url_is_exempt:
            return None
        else:
            return redirect(settings.LOGIN_URL)
