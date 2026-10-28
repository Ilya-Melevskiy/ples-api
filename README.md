# API Tests — PLES

Автотесты API для сайта на 1С-Битрикс. Стек: `pytest`, `requests`, `allure`, `pymysql`.

---

## Установка окружения

```powershell
# Создать и активировать venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# Установить зависимости
python -m pip install -r requirements.txt
```

---

## 🏃 Запуск тестов

Всегда запускай **из корня проекта** — где лежит `pytest.ini`:

```powershell
# Все тесты
python -m pytest tests 

# Только конкретный файл
python -m pytest tests/tests_api/user/test_login_email.py

# Упавшие в прошлый раз
python -m pytest tests --lf
```

> **Важно:** запуск через `python -m pytest` (не просто `pytest`). Иначе возможен `ModuleNotFoundError: No module named 'api'` — `python -m` добавляет корень проекта в `sys.path`.

---

## 📊 Allure-отчёты

```powershell
# Сгенерировать HTML отчёт (--clean обязателен, иначе упадёт)
allure generate allure-results -o allure-report --clean

# Открыть отчёт в браузере
allure open allure-report

# Если нужно просто быстро посмотреть
allure serve allure-results

### Структура проекта
```
---

```text
API_TESTS_PLES/
├── api/                       # Транспортный слой (клиент и эндпоинты)
│   ├── __init__.py
│   ├── client.py              # APIClient (обёртка над requests.Session)
│   └── endpoints.py           # Константы путей (AuthEndpoints, UserEndpoints)
│
├── config/                    # Настройки
│   ├── __init__.py
│   └── settings.py            # Dataclass Settings (читает .env)
│
├── tests/                     # Тесты
│   ├── __init__.py
│   ├── conftest.py            # Общие фикстуры (faker_ru, api_client)
│   └── tests_api/             # Слой API-тестов
│       └── user/              # Домен (авторизация, регистрация, пароли)
│           ├── __init__.py
│           ├── conftest.py    # Локальные фикстуры (send_otp, confirm_otp, login)
│           ├── test_forgot_password_otp_email_change.py
│           ├── test_forgot_password_otp_email_confirm.py
│           ├── test_forgot_password_otp_email_send.py
│           ├── test_forgot_password_otp_phone_change.py
│           ├── test_forgot_password_otp_phone_confirm.py
│           ├── test_forgot_password_otp_phone_send.py
│           ├── test_login_email.py
│           ├── test_login_phone.py
│           ├── test_logout.py
│           ├── test_registration_otp_email_confirm.py
│           ├── test_registration_otp_email_send.py
│           ├── test_registration_otp_phone_confirm.py
│           ├── test_registration_otp_phone_send.py
│           └── test_registration_submit.py
│
├── utils/                     # Утилиты
│   ├── email.py               # EmailService (чтение OTP из БД)
│   └── sms.py                 # SMSService (чтение OTP из БД)
│
├── .env                       # Секреты
├── .env.example               # Шаблон переменных
├── .gitignore
├── pytest.ini                 # Конфиг pytest
├── requirements.txt
└── README.md
```