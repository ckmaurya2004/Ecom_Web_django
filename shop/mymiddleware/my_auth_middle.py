from django.shortcuts import redirect

def auth_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        print("helo")
        print(request.user)
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if  (request.user):
            return  redirect ('/login') # not apply because login is a modal not any html page
        

        

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware