import requests
import json


def post_request(url, payload: dict):
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    code = response.status_code
    try:
        result = response.json()
    except ValueError:  # если JSONDecodeError
        result = {"error": "Response is not valid JSON", "text": response.text}
    return {"code": code, "result": result}

def print_incidents(data):
    for item in data:
        print(f'incident: {item["incident"]}  status: {item["status"]}  source: {item["source"]}  created_at: {item["created_at"]}')



URL = "http://127.0.0.1:8000/users/authorization/"
LOGIN = "test"
PASSWORD = "test123test"

#получаем токен
result = post_request(URL, {"username": LOGIN, "password": PASSWORD})
token = result["result"]['data']["token"]

date = "2025-11-11T23:08:12.266Z"

# создаем инцендент
URL = "http://127.0.0.1:8000/incidents/create/"
post = {"token": token, "incident": f"some incident {date}", "source": "operator", "date": date}
result = post_request(URL, post)
id = result["result"]['data']["id"]

# создаем меняем статус
URL = "http://127.0.0.1:8000/incidents/update/"
post = {"token": token, "id": id, "status": "completed"}
result = post_request(URL, post)
print("----view status ")
# смотрим со статусом
URL = "http://127.0.0.1:8000/incidents/get_all/"
post = {"token": token, "status": "completed"}
result = post_request(URL, post)
print_incidents(result["result"]['data']["incidents"])
print("----view all ")
# смотрим все
URL = "http://127.0.0.1:8000/incidents/get_all/"
post = {"token": token}
result = post_request(URL, post)
print_incidents(result["result"]['data']["incidents"])



# создаем инцендент
URL = "http://127.0.0.1:8000/incidents/create/"
post = {"token": token, "incident": f"some incident simple", "source": "operator"}
result = post_request(URL, post)
id = result["result"]['data']["id"]

# создаем меняем статус
URL = "http://127.0.0.1:8000/incidents/update/"
post = {"token": token, "id": id, "status": "completed"}
result = post_request(URL, post)

print("----view status ")
# смотрим со статусом
URL = "http://127.0.0.1:8000/incidents/get_all/"
post = {"token": token, "status": "completed"}
result = post_request(URL, post)
print_incidents(result["result"]['data']["incidents"])
print("----view all ")
# смотрим все
URL = "http://127.0.0.1:8000/incidents/get_all/"
post = {"token": token}
result = post_request(URL, post)
print_incidents(result["result"]['data']["incidents"])