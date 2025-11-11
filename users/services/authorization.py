import json
import secrets
from django.contrib.auth import authenticate
from users.models import AccessToken
from datetime import  timedelta
from django.utils import timezone
from constans import token_constans
import traceback

def get_token(request):
    """
    Функция авторизации  в POST запрос подается json с полями  username  и password
    :param request:  request  - от  джанго
    :return: возвращаем  словарь  вида  {"success": False/True, 'error': 'Error message / empty', "status": 405/400/401/500/200, "data": {} / {"token": token}}
    """
    try:
        if request.method != 'POST':
            return {"success": False, 'error': 'POST required', "status": 405, "data": {}}
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except Exception:
            return {"success": False, 'error': 'Invalid JSON', "status": 400, "data": {}}
        user = authenticate(username=username, password=password)
        if user is None:
            return {"success": False, 'error': 'Invalid credentials', "status": 401, "data": {}}
        token_obj = AccessToken.objects.filter(user_id=user.id).first()
        now = timezone.now()
        if token_obj:
            print(token_obj.expires_at)
            if token_obj.expires_at > now:
                new_token = secrets.token_hex(32)
                print(token_constans.TOKEN_EXPIRES_TIME)
                expires_at = now + timedelta(seconds=token_constans.TOKEN_EXPIRES_TIME)
                token_obj.token = new_token
                token_obj.created_at = now
                token_obj.expires_at = expires_at
                token_obj.save()
                return {"success": True, 'error': '', "status": 200, "data": {"token": new_token, "expires_at": expires_at}}
            else:
                return {"success": True, 'error': '', "status": 200, "data": {"token": token_obj.token, "expires_at": token_obj.expires_at}}
        else:
            new_token = secrets.token_hex(32)
            expires_at = now + timedelta(seconds=token_constans.TOKEN_EXPIRES_TIME)
            token_obj = AccessToken.objects.create(
                user=user,
                token=new_token,
                created_at=now,
                expires_at=expires_at
            )
            #token_obj.save()
            return {"success": True, 'error': '', "status": 200, "data": {"token": new_token, "expires_at": expires_at}}
    except Exception:
        tb = traceback.format_exc()
        print(tb)
        return {"success": False, 'error': 'Global error, try later', "status": 500, "data": {}}
