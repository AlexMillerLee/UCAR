import json
from django.utils import timezone
from users.models import AccessToken
import traceback

def get_token(request):
    """
    функция  проверки токена  POST запрос подается json с полем token
    :param request:
    :return: возвращаем  словарь  вида {"success": False/True, 'error': 'Error message / empty', "status": 405/400/401/500/200, "data": {}} в  случае success": True  запускается  функция  из API
    """
    try:
        if request.method != 'POST':
            return {"success": False, 'error': 'POST required', "status": 405, "data": {}}
        try:
            data = json.loads(request.body)
            token = data.get('token')
        except Exception:
            return {"success": False, 'error': 'Invalid JSON', "status": 400, "data": {}}
        if not token:
            return {"success": False, 'error': 'Token is required', "status": 400, "data": {}}
        token_obj = AccessToken.objects.filter(token=token).first()
        if not token_obj:
            return {"success": False, 'error': 'Invalid token', "status": 401, "data": {}}
        else:
            now = timezone.now()
            if token_obj.expires_at < now:
                return {"success": False, 'error': 'Token is expired', "status": 401, "data": {}}
            else:
                return {"success": True, 'error': '', "status": 200, "data": {}}
    except Exception:
        tb = traceback.format_exc()
        print(tb)
        return {"success": False, 'error': 'Global error try later', "status": 500, "data": {}}
