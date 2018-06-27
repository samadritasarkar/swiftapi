class MyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Auth-Token'] = "0184e98d9cc041b5803ce4faf9bff33b"
        return response