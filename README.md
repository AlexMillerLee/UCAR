# Incident Tracking API

Минималистичный REST API-сервис для учёта и обработки инцидентов (создание, обновление, просмотр)
Функциональность:

Инцидент должен иметь:

- id

- текст/описание

- статус (любой вменяемый набор, не 0/1)

- источник (например, operator / monitoring / partner)

- время создания

Нужны 3 вещи:

1. **Создать инцидент**

2. **Получить список инцидентов (с фильтром по статусу)**

3. **Обновить статус инцидента по id**
   Если не найден — вернуть 404.

## Установка и запуск

1. Клонируем проект или копируем `docker-compose.yml` на сервер.
2. При необходимости меняем логин/пароль суперпользователя. (User.objects.create_superuser(\"admin\",\"admin@example.com\",\"complexpassword\"))
3. Запускаем сервис:

   ```bash
   docker compose up -d --build


## API
Все запросы идут методом POST, в теле отправляется json. Ответы тоже в json.
Авторизация:
Запрос на адрес: http://ip:port/users/authorization/

        Запрос: {"username": LOGIN, "password": PASSWORD}

        Ответ:  "success": False/True 
                'error': 'Error message / empty', 
                "status": 405/400/401/500/200, 
                "data": {} / {"token": token}
                В случае неудачи отдает  код ошибки и текст. В случае успеха возвращает токен. Токен живет 1 час
    
    Создать инцидент:
        Запрос на адрес: http://ip:port/incidents/create/

        Запрос: {"token": token, "incident": f"some incident {date}", "source": "operator", "date": date}
            token - ваш токен
            incident(текстовое) 
            source текстовое, доступны варианты operator, monitoring, partner, unknown
            date в формате 2025-11-11T23:08:12.266Z (поле не обязательное, если не указывать будет текущая)
            Статус ставится как новый

        Ответ:  "success": False/True, 
                'error': 'Error message / empty', 
                "status": 405/400/401/500/201, 
                "data": {"id":ID}} 
                В случае неудачи отдает  код ошибки и текст. В случае успеха возвращает id инцидента. 
    
    Получить список инцидентов: 
        Запрос на адрес: http://ip:port/incidents/get_all/

        Запрос: {"token": token, "status": "completed"}
            token - ваш токен, 
            status текстовое, доступны варианты new, processing, completed, fake, unknown (не обязательное)
        
        Ответ:  "success": False/True, 
                'error': 'Error message / empty', 
                "status": 400/401/404/500/200, 
                "data": {"incidents": []} 
                Список  ассоциативный массив {incident:value, status:value, source:value, created_at:value}

    Обновить статус инцидента по id 
        Запрос на адрес: http://ip:port/incidents/update/

        Запрос: {"token": token, "id": id, "status": "completed"}
            id - id инцидента
            token - ваш токен, 
            status текстовое, доступны варианты new, processing, completed, fake, unknown
        
        Ответ:  
                "success": False/True, 
                'error': 'Error message / empty', 
                "status": 405/400/401/404/500/200, 
                "data": {}   
                код  200 - в случае успеха

## Полезные файлы
    client.py - демонстрация функционал, создает, обновляет статус, выводит список
    tests.py - тестирование
    При использование не забудьте поменять Ip/port, логин и пароль