"""
Простейший сервер, генерирует ошибку по адресу /fail и скидывает ошибку в sentry_sdk
Возвращает HTTP ответ 200 по /success и корню с пустой страницей

Согласно задания:
Необходимо написать простой веб-сервер с помощью фреймворка Bottle. Все ошибки приложения должны попадать в вашу информационную панель Sentry.
Приложение должно размещаться на Heroku, иметь минимум два маршрута:
    /success, который должен возвращать как минимум HTTP ответ со статусом 200 OK
    /fail, который должен возвращать "ошибку сервера" (на стороне Bottle это может быть просто RuntimeError), то есть HTTP ответ со статусом 500
"""
import os
import sentry_sdk

from bottle import Bottle, request
from sentry_sdk.integrations.bottle import BottleIntegration

sentry_sdk.init(
    dsn="https://<key>@sentry.io/<project>",
    integrations=[BottleIntegration()]
)

app = Bottle()

@app.route('/')
def root():
    return " "

@app.route('/fail')
def fail():
    raise RuntimeError("There is an error!")
    return

@app.route('/success')
def success():
    return " "

if os.environ.get("APP_LOCATION") == "heroku":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3,
    )
else:
    app.run(host='localhost', port=8080)
