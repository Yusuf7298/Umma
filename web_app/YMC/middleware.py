
from django.shortcuts import redirect
from django.contrib.auth import logout

class CaptureIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        request.session['user_ip'] = ip_address

        response = self.get_response(request)
        return response


class ValidateIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            
            session_ip = request.session.get('user_ip')
            
            current_ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')

            if session_ip != current_ip:
                logout(request)
                return redirect('login') 

        response = self.get_response(request)
        return response