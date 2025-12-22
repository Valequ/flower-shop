from django.shortcuts import redirect

def protect_admin(get_response):
    def middleware(request):
        if request.path.startswith('/admin/'):
            if not request.user.is_authenticated or not request.user.is_staff:
                return redirect('/')
        return get_response(request)
    return middleware