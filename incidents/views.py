from django.http import JsonResponse
from .services import core, create, get
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def get_all_views(request):
    data = core.get_token(request)
    if data["success"] is False:
        print(data)
        status = data["status"]
        del data["status"]
        return JsonResponse(data, status=status)
    data = get.get_all(request)
    print(data)
    status = data["status"]
    del data["status"]
    return JsonResponse(data, status=status)



@csrf_exempt
def update_views(request):
    data = core.get_token(request)
    if data["success"] is False:
        print(data)
        status = data["status"]
        del data["status"]
        return JsonResponse(data, status=status)
    data = create.update(request)
    print(data)
    status = data["status"]
    del data["status"]
    return JsonResponse(data, status=status)


@csrf_exempt
def create_views(request):
    data = core.get_token(request)
    print(data)
    if data["success"] is False:
        print(data)
        status = data["status"]
        del data["status"]
        return JsonResponse(data, status=status)
    data = create.create(request)
    print(data)
    status = data["status"]
    del data["status"]
    return JsonResponse(data, status=status)
