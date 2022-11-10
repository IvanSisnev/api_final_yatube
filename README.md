# **Проект api_final_yatube**
<br><br>
## **Краткое описание проекта**
___
**Бекэнд проекта соцсети, в которой пользователи могут размещать посты, объединять посты в сообщества, читать и комментировать записи других пользователей, подписываться на них.**
<br><br>

## **Запуск проекта**
___

### **1. Развертывание репозитория**


#### **Клонировать репозиторий:**

    git clone https://github.com/IvanSisnev/api_final_yatube.git

#### **В директории проекта создать и активировать виртуальное окружение:**

    python3 -m venv venv
    
    source venv/bin/activate

### **2. Установка зависимостей и запуск**

#### **Установить зависимости:**

    python3 -m pip install --upgrade pip
    
    pip install -r requirements.txt

#### **Выполнить миграции:**

    python3 manage.py migrate

#### **Запустить проект:**

    python3 manage.py runserver
<br><br>
## **Регистрация и авторизация пользователей**
___

### **1. Зарегистировать нового пользователя**

На эндпоинт **`api/v1/users/`** отправить POST-запрос, содержащий пару "логин-пароль" в следующем формате:

```json
{
  "username": "username",
  "password": "password"
}
```
В случае успешной регистрации от API придет ответ в следующем формате:
 ```json
{
  "email": "",
  "username": "username",
  "id": 1
}
```
### **2. Получить токен**

На эндпоинт **`api/v1/jwt/create/`** отправить POST-запрос, содержащий пару "логин-пароль" зарегистированного пользователя. 

Ответ от API будет содержать токен доступа к API (`access`) и код (`refresh`) для обновления токена доступа:

```json
// Пример ответа
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyMDk0MTQ3NywianRpIjoiODUzYzE5MTg5NzMwNDQwNTk1ZjI3ZTBmOTAzZDcxZDEiLCJ1c2VyX2lkIjoxfQ.0vJBPIUZG4MjeU_Q-mhr5Gqjx7sFlO6AShlfeINK8nA",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjIwODU1Mzc3LCJqdGkiOiJkY2EwNmRiYTEzNWQ0ZjNiODdiZmQ3YzU2Y2ZjNGE0YiIsInVzZXJfaWQiOjF9.eZfkpeNVfKLzBY7U0h5gMdTwUnGP3LjRn5g8EIvWlVg"
}
```
> Внимание! Срок действия токена ограничен установками проекта. В разделе **"Взаимодействие с API. 2. Обновление токена."** можно прочитать про то, как получить новый токен взамен устаревшего или скомпрометированного.

<br><br>
## **Взаимодействие с API**
___
### **1. Передача токена в запросе**

Для осуществления запросов к API необходимо **в заголовке каждого запроса** в поле **`Authorization`** передавать действующий токен. Сам токен указывается без кавычек; перед токеном должно быть слово **`Bearer`** и пробел:

```json
{
  "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjY4NjcxOTMzLCJqdGkiOiIxY2UwZjAyZWM3Nzg0MWQ2OWJiOGViMWIzZDFkZjc5OCIsInVzZXJfaWQiOjR9.RJAv3GhQYshQmUgxZ6utrNNdGdImKGAZ3ccTgAP8nM8"
}
```

### **2. Обновление токена**

Для обновления токена необходимо отправить на эндпоинт **`api/v1/jwt/create/`** в заголовке запроса аналогично обычному токену (см. **Взаимодействие с API. 1. Передача токена в запросе.**) значение ключа `"refresh"`:

```json
{
  "Authorization": "refresh eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYyMDk0MTQ3NywianRpIjoiODUzYzE5MTg5NzMwNDQwNTk1ZjI3ZTBmOTAzZDcxZDEiLCJ1c2VyX2lkIjoxfQ.0vJBPIUZG4MjeU_Q-mhr5Gqjx7sFlO6AShlfeINK8nA"
}
```
Ответ от API будет содержать новую пару `"refresh-access"`.

### **3. Примеры запросов-ответов от API**

API проекта содержит ряд эндпоинтов, запросы к которым позволяют получать информацию от приложения и размещать информацию в нем.

#### **Получение списка постов**

Ответ на GET-запрос к эндпоинту **`api/v1/posts/`** будет содержать список постов пользователя, осуществляющего запрос:

```json
[
    {
        "id": 1,
        "author": "username",
        "text": "Текст поста 1.",
        "pub_date": "2022-11-09T09:18:00.295729Z",
        "image": null,
        "group": null
    },
    {
        "id": 2,
        "author": "username",
        "text": "Текст поста 2.",
        "pub_date": "2022-11-09T09:18:05.295729Z",
        "image": null,
        "group": 1
    }
]
```

#### **Размещение нового поста**

Для размещения нового поста надо на эндпоинт **`api/v1/posts/`** отправить POST-запрос, содержащий как минимум одно обязательное поле - текст поста:

```json
{
  "text": "Текст нового поста."
}
```
В запросе также можно передать значения необязательных полей `"image"` и `"group"`.

> Значения полей `"id"`, `"author"` и `"pub_date"` передавать не нужно: они будут присвоены автоматически. 

В случае успешного размещения поста ответ от API будет содержать данные нового поста:
```json
{
  "id": 3,
  "author": "username",
  "text": "Текст нового поста.",
  "pub_date": "2022-11-09T09:18:10.295729Z",
  "image": null,
  "group": null
}
```
Взаимодействие с *сообществами*, *комментариями к постам* и *подписками на авторов* устроено аналогичным образом на соответствующих эндпоинтах.
