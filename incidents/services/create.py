import json
from datetime import datetime
from incidents.models import Incident
from constans import incidents


def create(request):
    """
    Создает инцидент,     в POST запрос подается json с полями incident(текстовое), source(текстовое, доступны варианты operator, monitoring, partner, unknown)
    date в формате 2025-11-11T23:08:12.266Z (поле не обязательное, если не указывать будет текущая)
    :param request:
    :return:  возвращаем  словарь  вида {"success": False/True, 'error': 'Error message / empty', "status": 405/400/401/500/201, "data": {"id":ID}}  - в случае success
    """
    try:
        data = json.loads(request.body)
        incident = data.get('incident')
        source = data.get('source')
        created_at = data.get('date')
        if not incident:
            return {"success": False, 'error': 'Incident is required', "status": 400, "data": {}}
        source_dict = {name: idx for idx, name in incidents.get_source()}
        if source not in source_dict:
            allowed = ", ".join(source_dict.keys())
            return {"success": False, 'error': f'Source is required or wrong, use one of: {allowed}', "status": 400, "data": {}}
        if not created_at:
            created_at = datetime.now()
        else:
            created_at = incidents.parse_datetime(created_at)
            if created_at is None:
                return {"success": False, 'error': 'Wrong date format', "status": 400, "data": {}}
        obj = Incident.objects.create(
            incident=incident,
            status=0,
            created_at=created_at,
            source=source_dict[source]
        )
        # obj.save()
        return {"success": True, 'error': '', "status": 201, "data": {"id": obj.id}}
    except Exception:
        return {"success": False, 'error': 'Global error, try later', "status": 500, "data": {}}


def update(request):
    """
        Изменяет статус инцидента, в POST запрос подается json с полями id(число), status(текстовое, доступны варианты new, processing, completed, fake, unknown)
        :param request:
        :return:  возвращаем  словарь  вида {"success": False/True, 'error': 'Error message / empty', "status": 405/400/401/404/500/200, "data": {}   код  200 - в случае success
        """
    try:
        data = json.loads(request.body)
        id = data.get('id')
        status = data.get('status')
        if not id:
            return {"success": False, 'error': 'ID is required', "status": 400, "data": {}}
        try:
            id = int(id)
        except Exception:
            return {"success": False, 'error': 'ID must be numeric', "status": 400, "data": {}}
        status_dict = {name: idx for idx, name in incidents.get_status()}
        allowed = ", ".join(status_dict.keys())
        if status not in status_dict:
            return {"success": False, 'error': f'Status is required or wrong, use one of: {allowed}', "status": 400, "data": {}}
        obj = Incident.objects.filter(id=id).first()
        if not obj:
            return {"success": False, 'error': 'Incident have not found', "status": 404, "data": {}}
        obj.status = status_dict[status]
        obj.save()
        return {"success": True, 'error': '', "status": 200, "data": {}}
    except Exception:
        return {"success": False, 'error': 'Global error try later', "status": 500, "data": {}}
