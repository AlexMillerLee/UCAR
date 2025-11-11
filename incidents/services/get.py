import json
from datetime import datetime
from incidents.models import Incident
from constans import incidents


def get_all(request):
    """
           Выводит все инциденты  в POST запрос подается json с полем status(текстовое, доступны варианты new, processing, completed, fake, unknown) - не обзательное
           :param request:
           :return:  возвращаем  словарь  вида {"success": False/True, 'error': 'Error message / empty', "status": 400/401/404/500/200, "data": {"incidents": []} - в случае success
           Список  содержит словари {incident:value, status:value, source:value, created_at:value
           """
    try:
        data = json.loads(request.body)
        status = data.get('status')
        status_dict = {name: idx for idx, name in incidents.get_status()}
        if status and status not in status_dict:
            allowed = ", ".join(status_dict.keys())
            return {"success": False, 'error': f"Status must be one of: {allowed}" , "status": 400, "data": {}}
        if status:
            objs = list(Incident.objects.filter(status=status_dict[status]).all())
        else:
            objs = list(Incident.objects.all())
        result = []
        status_dict = {idx: name for idx, name in incidents.get_status()}
        source_dict = {idx: name for idx, name in incidents.get_source()}
        for obj in objs:
            result.append({"incident": obj.incident, "status": status_dict[obj.status], "source": source_dict[obj.source], "created_at": obj.created_at})
        if result:
            return {"success": True, 'error': '', "status": 200, "data": {"incidents": result}}
        else:
            return {"success": True, 'error': '', "status": 404, "data": {"incidents": []}}
    except Exception:
        return {"success": False, 'error': 'Global error try later', "status": 500, "data": {}}
