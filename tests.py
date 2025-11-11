import requests
import json


def get_request(url, params=None):
    if params is None:
        params = {}
    response = requests.get(url, params=params)
    code = response.status_code
    try:
        result = response.json()
    except ValueError:  # если JSONDecodeError
        result = {"error": "Response is not valid JSON", "text": response.text}
    return {"code": code, "result": result}


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


def post_simple_request(url, payload: dict):
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=payload)
    code = response.status_code
    try:
        result = response.json()
    except ValueError:  # если JSONDecodeError
        result = {"error": "Response is not valid JSON", "text": response.text}
    return {"code": code, "result": result}


# URL твоего API
URL = "http://127.0.0.1:8000/users/authorization/"
LOGIN = "test"
PASSWORD = "test123test"

success = True
result = get_request(URL)
if result["code"] == 405 and result["result"]['error'] == 'POST required':
    print(f"Authorization GET  passed")
else:
    print(f"Authorization GET  failed {result['code']} {result['result']}")
    success = False

result = get_request(URL, {"username": LOGIN, "password": PASSWORD})
if result["code"] == 405 and result["result"]['error'] == 'POST required':
    print(f"Authorization GET params  passed")
else:
    print(f"Authorization GET params failed {result['code']} {result['result']}")
    success = False


result = post_simple_request(URL, {"username": LOGIN, "password": PASSWORD})
if result["code"] == 400 and result["result"]['error'] == 'Invalid JSON':
    print(f"Authorization simple post  passed")
else:
    print(f"Authorization simple post  failed {result['code']} {result['result']}")
    success = False


result = post_request(URL, {"password": PASSWORD})
if result["code"] == 401 and result["result"]['error'] == 'Invalid credentials':
    print(f"Authorization  no username passed")
else:
    print(f"Authorization  no username  failed {result['code']} {result['result']}")
    success = False


result = post_request(URL, {"username": LOGIN})
if result["code"] == 401 and result["result"]['error'] == 'Invalid credentials':
    print(f"Authorization  no password  passed")
else:
    print(f"Authorization  no password  failed {result['code']} {result['result']}")
    success = False

result = post_request(URL, {"username": "wrong", "password": PASSWORD})
if result["code"] == 401 and result["result"]['error'] == 'Invalid credentials':
    print(f"Authorization  wrong username or password passed")
else:
    print(f"Authorization  wrong username or password  failed {result['code']} {result['result']}")
    success = False

result = post_request(URL, {"username": LOGIN, "password": PASSWORD})
if result["code"] == 200 and result["result"]['data']["token"] and result["result"]['data']["expires_at"]:
    print(f"Authorization  valid data passed token: " + result["result"]['data']["token"] + "  expires_at:  " + result["result"]['data']["expires_at"])
    token = result["result"]['data']["token"]
else:
    print(f"Authorization  valid data  failed {result['code']} {result['result']}")
    success = False

print("-----CREATE-----")
URL = "http://127.0.0.1:8000/incidents/create/"

result = get_request(URL)
post = {"token": token, "incident": "some incident", "source": "operator", "date": "2025-11-11T23:08:12.266Z"}
if result["code"] == 405 and result["result"]['error'] == 'POST required':
    print(f"Create GET  passed  passed")
else:
    print(f"Create GET  passed  failed {result['code']} {result['result']}")
    success = False

result = get_request(URL, post)
if result["code"] == 405 and result["result"]['error'] == 'POST required':
    print(f"Create GET params  passed")
else:
    print(f"Create GET params  failed {result['code']} {result['result']}")
    success = False


result = post_simple_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Invalid JSON':
    print(f"Create simple post passed")
else:
    print(f"Create simple post   failed {result['code']} {result['result']}")
    success = False


del post["token"]
result = post_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Token is required':
    print(f"Create no token  passed")
else:
    print(f"Create no token  failed {result['code']} {result['result']}")
    success = False

post["token"] = "faketoken"
result = post_request(URL, post)
if result["code"] == 401 and result["result"]['error'] == 'Invalid token':
    print(f"Create Invalid token  passed")
else:
    print(f"Create Invalid token    failed {result['code']} {result['result']}")
    success = False

post["token"] = token
del post["incident"]
result = post_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Incident is required':
    print(f"Create Incident is required passed")
else:
    print(f"Create Incident is required  failed {result['code']} {result['result']}")
    success = False

post["incident"] = "some incident"
del post["source"]
result = post_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Source is required or wrong, use one of: operator, monitoring, partner, unknown':
    print(f"Create Source is required passed")
else:
    print(f"Create Source is required failed {result['code']} {result['result']}")
    success = False


post["source"] = "wrong source"
result = post_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Source is required or wrong, use one of: operator, monitoring, partner, unknown':
    print(f"Create wrong source passed")
else:
    print(f"Create wrong source failed {result['code']} {result['result']}")
    success = False


post["source"] = "monitoring"
post["date"] = "wrong date"
result = post_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Wrong date format':
    print(f"Create Wrong date format passed")
else:
    print(f"Create Wrong date format failed {result['code']} {result['result']}")
    success = False
print("-----CREATE Valid-----")
# проверяем валидные данные

del post["date"]
result = post_request(URL, post)
if result["code"] == 201 and "id" in result["result"]['data']:
    print(f'Create valid without date passed id:{result["result"]['data']["id"]}')
else:
    print(f"Create valid without date failed {result['code']} {result['result']}")
    success = False

post["date"] = "2025-11-11T23:10:12.266Z"
result = post_request(URL, post)
if result["code"] == 201 and "id" in result["result"]['data']:
    print(f'Create valid date passed id:{result["result"]['data']["id"]}')
else:
    print(f"Create valid date failed {result['code']} {result['result']}")
    success = False

print("-----UPDATE-----")
URL = "http://127.0.0.1:8000/incidents/update/"

result = get_request(URL)
post = {"token": token, "id": 4, "status": "completed"}
if result["code"] == 405 and result["result"]['error'] == 'POST required':
    print(f"Update GET  passed  passed")
else:
    print(f"Update GET  passed  failed {result['code']} {result['result']}")
    success = False

result = get_request(URL, post)
if result["code"] == 405 and result["result"]['error'] == 'POST required':
    print(f"Update GET params  passed")
else:
    print(f"Update GET params  failed {result['code']} {result['result']}")
    success = False


result = post_simple_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Invalid JSON':
    print(f"Update simple post passed")
else:
    print(f"Update simple post   failed {result['code']} {result['result']}")
    success = False


del post["token"]
result = post_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Token is required':
    print(f"Update no token passed")
else:
    print(f"Update no token failed {result['code']} {result['result']}")
    success = False

post["token"] = "faketoken"
result = post_request(URL, post)
if result["code"] == 401 and result["result"]['error'] == 'Invalid token':
    print(f"Update Invalid token  passed")
else:
    print(f"Update Invalid token    failed {result['code']} {result['result']}")
    success = False

post["token"] = token
del post["id"]
result = post_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'ID is required':
    print(f"Update ID is required passed")
else:
    print(f"Update ID is required failed {result['code']} {result['result']}")
    success = False
post["id"] = "fake"
result = post_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'ID must be numeric':
    print(f"Update ID is required passed")
else:
    print(f"Update ID is required failed {result['code']} {result['result']}")
    success = False

post["id"] = 4
del post["status"]
result = post_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Status is required or wrong, use one of: new, processing, completed, fake, unknown':
    print(f"Update no status passed")
else:
    print(f"Update no status failed {result['code']} {result['result']}")
    success = False

post["status"] = "wrong status"
result = post_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Status is required or wrong, use one of: new, processing, completed, fake, unknown':
    print(f"Update wrong status passed")
else:
    print(f"Update wrong status failed {result['code']} {result['result']}")
    success = False

post["status"] = "completed"
post["id"] = 56205
result = post_request(URL, post)
if result["code"] == 404 and result["result"]['error'] == 'Incident have not found':
    print(f"Update no incident passed")
else:
    print(f"Update no incident failed {result['code']} {result['result']}")
    success = False

print("-----UPDATE valid-----")

post["status"] = "completed"
post["id"] = 4
result = post_request(URL, post)
if result["code"] == 200:
    print(f"Update valid passed")
else:
    print(f"Update valid failed {result['code']} {result['result']}")
    success = False


print("-----GET ALL-----")
URL = "http://127.0.0.1:8000/incidents/get_all/"

result = get_request(URL)
post = {"token": token, "status": "completed"}
if result["code"] == 405 and result["result"]['error'] == 'POST required':
    print(f"GET ALL GET  passed  passed")
else:
    print(f"GET ALL GET  passed  failed {result['code']} {result['result']}")
    success = False

result = get_request(URL, post)
if result["code"] == 405 and result["result"]['error'] == 'POST required':
    print(f"GET ALL GET params  passed")
else:
    print(f"GET ALL GET params  failed {result['code']} {result['result']}")
    success = False


result = post_simple_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Invalid JSON':
    print(f"GET ALL simple post passed")
else:
    print(f"GET ALL simple post   failed {result['code']} {result['result']}")
    success = False


del post["token"]
result = post_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Token is required':
    print(f"GET ALL no token passed")
else:
    print(f"GET ALL no token failed {result['code']} {result['result']}")
    success = False

post["token"] = "faketoken"
result = post_request(URL, post)
if result["code"] == 401 and result["result"]['error'] == 'Invalid token':
    print(f"GET ALL Invalid token  passed")
else:
    print(f"GET ALL Invalid token    failed {result['code']} {result['result']}")
    success = False

post["token"] = token


post["status"] = "wrong status"
result = post_request(URL, post)
if result["code"] == 400 and result["result"]['error'] == 'Status must be one of: new, processing, completed, fake, unknown':
    print(f"GET ALL wrong status passed")
else:
    print(f"GET ALL wrong status failed {result['code']} {result['result']}")
    success = False

print("-----GET ALL valid-----")

post["status"] = "completed"
result = post_request(URL, post)
if result["code"] == 200 and "incidents" in result["result"]['data'] and result["result"]['data']["incidents"]:
    print(f"GET ALL status = completed  passed")
    print(result["result"]['data']["incidents"])
else:
    print(f"GET ALL status = completed  failed {result['code']} {result['result']}")
    success = False

post["status"] = "unknown"
result = post_request(URL, post)
if result["code"] == 404 and "incidents" in result["result"]['data'] and not result["result"]['data']["incidents"]:
    print(f"GET ALL status = unknown  passed")
    print(result["result"]['data']["incidents"])
else:
    print(f"GET ALL status = unknown  failed {result['code']} {result['result']}")
    success = False
del post["status"]
result = post_request(URL, post)
if result["code"] == 200 and "incidents" in result["result"]['data'] and result["result"]['data']["incidents"]:
    print(f"GET ALL status = completed  passed")
    print(result["result"]['data']["incidents"])
else:
    print(f"GET ALL status = completed  failed {result['code']} {result['result']}")
    success = False

if success:
    print("ALL TEST PASSED")
else:
    print(" TEST FAILED")
