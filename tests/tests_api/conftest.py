import pytest
from faker import Faker

from api.client import APIClient
from api.endpoints import UserEndpoints
from utils.sms import SMSService
from utils.email import EmailService


@pytest.fixture
def api_client_no_auth():
    """
    Неавторизованный клиент
    """
    api = APIClient(token="")
    yield api
    api.close()


fake = Faker()


@pytest.fixture
def send_otp_phone(api_client_no_auth, faker_phone_number_starting_plus_7, db_cursor):
    """Отправляет OTP и возвращает (phone, code)."""
    phone = faker_phone_number_starting_plus_7()

    r = api_client_no_auth.post(
        UserEndpoints.REGISTRATION_PHONE_SEND_OTP,
        json={"phone": phone},
    )
    assert r.status_code == 200, r.text

    code = SMSService.get_otp_code(db_cursor, phone)
    return phone, code


@pytest.fixture
def send_otp_email(api_client_no_auth, faker_ru, db_cursor):
    """Отправляет OTP и возвращает (email, code)."""
    email = faker_ru.email()
    payload = {"email": email}
    r = api_client_no_auth.post(UserEndpoints.REGISTRATION_EMAIL_SEND_OTP, json=payload)
    assert r.status_code == 200, r.text

    code = EmailService.get_otp_code(db_cursor, email)
    return email, code


@pytest.fixture
def confirm_otp_phone(api_client_no_auth, send_otp_phone):
    """Подтверждает OTP код по номеру и возвращает (phone)"""
    phone, code = send_otp_phone
    payload = {"phone": phone, "digitCode": code}
    r = api_client_no_auth.post(
        UserEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
    )
    assert r.status_code == 200, r.text
    return phone


@pytest.fixture
def confirm_otp_email(api_client_no_auth, send_otp_email):
    """Подтверждает OTP код по номеру и возвращает (phone)"""
    email, code = send_otp_email
    payload = {"email": email, "digitCode": code}
    r = api_client_no_auth.post(
        UserEndpoints.REGISTRATION_EMAIL_CONFIRM_OTP, json=payload
    )
    assert r.status_code == 200, r.text
    return email


@pytest.fixture
def registration_natural_person(
    api_client_no_auth, faker_phone_number_starting_plus_7, faker_ru, db_cursor
):
    """Регистрирует пользователя и возвращает (phone, password, email)"""
    phone = faker_phone_number_starting_plus_7()
    response_send = api_client_no_auth.post(
        UserEndpoints.REGISTRATION_PHONE_SEND_OTP,
        json={"phone": phone},
    )
    assert response_send.status_code == 200, response_send.text

    code = SMSService.get_otp_code(db_cursor, phone)
    payload_confirm = {"phone": phone, "digitCode": code}
    response_confirm = api_client_no_auth.post(
        UserEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload_confirm
    )
    assert response_confirm.status_code == 200, response_confirm.text

    password = f"a1{faker_ru.password(length=4)}"
    email = faker_ru.email()
    payload_registration = {
        "general": {
            "email": email,
            "phone": phone,
            "password": password,
            "passwordRepeat": password,
            "firstName": faker_ru.first_name(),
            "lastName": faker_ru.last_name(),
            "secondName": faker_ru.middle_name(),
        }
    }
    response_submit = api_client_no_auth.post(
        UserEndpoints.REGISTRATION_COMPLETION, json=payload_registration
    )
    assert response_submit.status_code == 200, response_submit.text
    return {"phone": phone, "password": password, "email": email}


@pytest.fixture
def registration_legal_person(
    api_client_no_auth, faker_phone_number_starting_plus_7, faker_ru, db_cursor
):
    """Регистрирует пользователя и возвращает (phone, password, email)"""
    phone = faker_phone_number_starting_plus_7()
    response_send = api_client_no_auth.post(
        UserEndpoints.REGISTRATION_PHONE_SEND_OTP,
        json={"phone": phone},
    )
    assert response_send.status_code == 200, response_send.text

    code = SMSService.get_otp_code(db_cursor, phone)
    payload_confirm = {"phone": phone, "digitCode": code}
    response_confirm = api_client_no_auth.post(
        UserEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload_confirm
    )
    assert response_confirm.status_code == 200, response_confirm.text

    password = f"a1{faker_ru.password(length=4)}"
    email = faker_ru.email()
    inn = faker_ru.businesses_inn()
    payload_registration = {
        "general": {
            "email": faker_ru.email(),
            "phone": phone,
            "password": password,
            "passwordRepeat": password,
            "firstName": faker_ru.first_name(),
            "lastName": faker_ru.last_name(),
            "secondName": faker_ru.middle_name(),
        },
        "legal": {
            "inn": inn,
            "shortName": faker_ru.company(),
            "fullName": f"Общество с ограниченной ответственностью '{faker_ru.large_company()}'",
            "kpp": faker_ru.kpp(),
            "ogrn": faker_ru.businesses_ogrn(),
            "bik": faker_ru.bic(),
            "bankName": faker_ru.bank(),
            "legalAddress": faker_ru.address(),
        },
    }
    response_submit = api_client_no_auth.post(
        UserEndpoints.REGISTRATION_COMPLETION, json=payload_registration
    )
    assert response_submit.status_code == 200, response_submit.text
    return {"phone": phone, "password": password, "email": email, "inn": inn}


@pytest.fixture
def forgot_password_send_otp_email(
    api_client_no_auth, registration_natural_person, db_cursor
):
    """Отправляет OTP и возвращает (email, code) для восстановления пароля"""
    email = registration_natural_person["email"]
    payload = {"email": email}
    r = api_client_no_auth.post(
        UserEndpoints.FORGOT_PASSWORD_EMAIL_SEND_OTP, json=payload
    )
    assert r.status_code == 200, r.text

    code = EmailService.get_otp_code(db_cursor, email)
    return email, code


@pytest.fixture
def forgot_password_send_otp_phone(
    api_client_no_auth, registration_natural_person, db_cursor
):
    """Отправляет OTP и возвращает (phone, code) для восстановления пароля"""
    phone = registration_natural_person["phone"]

    r = api_client_no_auth.post(
        UserEndpoints.FORGOT_PASSWORD_PHONE_SEND_OTP,
        json={"phone": phone},
    )
    assert r.status_code == 200, r.text

    code = SMSService.get_otp_code(db_cursor, phone)
    return phone, code


@pytest.fixture
def login_by_email(api_client_no_auth, registration_natural_person):
    email = registration_natural_person["email"]
    password = registration_natural_person["password"]
    payload = {"email": email, "password": password}
    response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

    assert response.status_code == 200, response.text
    return {"email": email, "password": password}
