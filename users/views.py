from django.http import JsonResponse
from .services import authorization
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def authorization_views(request):
    data = authorization.get_token(request)
    print(data)
    status = data["status"]
    del data["status"]
    return JsonResponse(data, status=status)
