import allure

from api.endpoints import AuthEndpoints
from utils.sms import SMSService


@allure.epic("Users")
@allure.feature("Регистрация")
@allure.story("Регистрация: Отправить OTP (email)")
class TestRegistrationByEmailSend:
    @allure.title(
        "POST /api/v1/auth/register/otp/email/send Успешная отправка OTP на не зарегистрированный email"
    )
    def test_registration_by_email_send_otp_correct_body_200(
        self, api_client_no_auth, faker_ru
    ):
        email = faker_ru.email()
        payload = {"email": email}
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_EMAIL_SEND_OTP, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert email in body["data"]["message"]
        assert body["data"]["redirectUrl"] is None
        assert body["errors"] == []

    @allure.title(
        "POST /api/v1/auth/register/otp/email/send Повторная отправка раньше минуты"
    )
    def test_registration_by_email_send_otp_before_minute_502(
        self, api_client_no_auth, faker_ru
    ):
        email = faker_ru.email()
        payload = {"email": email}
        api_client_no_auth.post(AuthEndpoints.REGISTRATION_EMAIL_SEND_OTP, json=payload)
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_EMAIL_SEND_OTP, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Повторная отправка кода подтверждения возможна"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    # TODO: Заменить email на email настоящего аккаунта
    # @allure.title(
    #     "POST /api/v1/auth/register/otp/email/send Отправка на уже зарегистрированный email"
    # )
    # def test_registration_by_email_send_otp_existing_email_502(
    #     self, api_client_no_auth, faker_ru
    # ):
    #     email = faker_ru.email()
    #     payload = {"email": email}
    #     api_client_no_auth.post(AuthEndpoints.REGISTRATION_EMAIL_SEND_OTP, json=payload)
    #     response = api_client_no_auth.post(
    #         AuthEndpoints.REGISTRATION_EMAIL_SEND_OTP, json=payload
    #     )
    #

    #     assert response.status_code == 502
    #     body = response.json()
    #     assert body["status"] == "error"
    #     assert body["data"] is None
    #     assert (
    #         "Пользователь с указанной эл. почтой уже существует"
    #         in body["errors"][0]["message"]
    #     )
    #     assert body["errors"][0]["code"] == 0
    #     assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/register/otp/email/send Запрос с пустым телом")
    def test_registration_by_email_send_otp_empty_body_502(self, api_client_no_auth):
        payload = {}
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_EMAIL_SEND_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Значение поля не является адресом электронной почты"
            in body["errors"][0]["message"]
        )
        assert "email" in body["errors"][0]["code"]
        assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/register/otp/email/send Запрос с email без @ ")
    def test_registration_by_email_send_otp_email_without_at_400(
        self, api_client_no_auth, faker_ru
    ):
        email = f"{faker_ru.name()}mail.ru"
        payload = {"email": email}
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_EMAIL_SEND_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Значение поля не является адресом электронной почты"
            in body["errors"][0]["message"]
        )
        assert "email" in body["errors"][0]["code"]
        assert body["errors"][0]["customData"] is None


@allure.epic("Users")
@allure.feature("Регистрация")
@allure.story("Регистрация: отправить OTP (phone)")
class TestRegistrationByPhoneSend:
    @allure.title(
        "POST /api/v1/auth/register/otp/phone/send Успешная отправка SMS с OTP на не зарегистрированный номер"
    )
    def test_registration_by_phone_send_otp_correct_body_200(
        self, api_client_no_auth, faker_phone_number_starting_plus_7
    ):
        phone = faker_phone_number_starting_plus_7
        payload = {"phone": phone}
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_PHONE_SEND_OTP, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert phone in body["data"]["message"]
        assert body["data"]["redirectUrl"] is None
        assert body["errors"] == []

    # TODO: Исправить номер, на номер существующего пользователя
    # @allure.title(
    #     "POST /api/v1/auth/register/otp/phone/send Отправка на зарегистрированный номер"
    # )
    # def test_registration_by_phone_send_otp_existing_phone_502(
    #     self, api_client_no_auth, faker_phone_number
    # ):
    #     phone = faker_phone_number
    #     payload = {"phone": phone}
    #     response = api_client_no_auth.post(
    #         AuthEndpoints.REGISTRATION_PHONE_SEND_OTP, json=payload
    #     )

    #     assert response.status_code == 502
    #     body = response.json()
    #     assert body["status"] == "error"
    #     assert body["data"] is None
    #     assert (
    #         "Пользователь с указанным номером уже существует"
    #         in body["errors"][0]["message"]
    #     )
    #     assert body["errors"][0]["code"] == 0
    #     assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/otp/phone/send Повторная отправка раньше минуты"
    )
    def test_registration_by_phone_send_otp_before_minute_502(
        self, api_client_no_auth, faker_phone_number_starting_plus_7
    ):
        phone = faker_phone_number_starting_plus_7
        payload = {"phone": phone}
        api_client_no_auth.post(AuthEndpoints.REGISTRATION_PHONE_SEND_OTP, json=payload)
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_PHONE_SEND_OTP, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Повторная отправка кода подтверждения возможна"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title("POST /api/v1/auth/register/otp/phone/send Запрос с пустым телом")
    def test_registration_by_phone_send_otp_empty_body_400(self, api_client_no_auth):
        payload = {}
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_PHONE_SEND_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/otp/phone/send Запрос с номером, начинающимся с 8"
    )
    def test_registration_by_phone_send_otp_phone_starting_8(
        self, api_client_no_auth, faker_phone_number_starting_8
    ):
        phone = faker_phone_number_starting_8
        payload = {"phone": phone}
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_PHONE_SEND_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None


@allure.epic("Users")
@allure.feature("Регистрация")
@allure.story("Регистрация: подтвердить OTP (phone)")
class TestRegistrationByPhoneConfirm:
    @allure.title(
        "POST /api/v1/auth/register/otp/phone/confirm Успешное подтверждение OTP с корректным шестизначным кодом"
    )
    def test_registration_by_phone_confirm_otp_correct_body_200(
        self, api_client_no_auth, send_otp
    ):
        phone, code = send_otp
        payload = {"phone": phone, "digitCode": code}
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Номер телефона успешно подтержден" in body["data"]["message"]
        assert body["errors"] == []
        assert body["data"]["redirectUrl"] is None

    @allure.title(
        "POST /api/v1/auth/register/otp/phone/confirm Подтверждение с неверным OTP-кодом"
    )
    def test_registration_by_phone_confirm_otp_incorrect_otp_502(
        self, api_client_no_auth, send_otp
    ):
        phone, code = send_otp
        incorrect_code = "111111"
        payload = {"phone": phone, "digitCode": incorrect_code}
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Введен некорректный код или срок его действия истек"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    # TODO: Добавить регистрацию пользователя через фикстуру, чтобы брать уже занятый номер
    # @allure.title(
    #     "POST /api/v1/auth/register/otp/phone/confirm Подтверждение для зарегистрированного номера"
    # )
    # def test_registration_by_phone_confirm_otp_existing_phone_502(
    #     self, api_client_no_auth, send_otp
    # ):
    #     phone, code = send_otp
    #     payload = {"phone": phone, "digitCode": code}
    #     response = api_client_no_auth.post(
    #         AuthEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
    #     )

    #     assert response.status_code == 502
    #     body = response.json()
    #     assert body["status"] == "error"
    #     assert body["data"] is None
    #     assert (
    #         "Введен некорректный код или срок его действия истек"
    #         in body["errors"][0]["message"]
    #     )
    #     assert body["errors"][0]["code"] == 0
    #     assert body["errors"][0]["customData"] is None

    def test_registration_by_phone_confirm_otp_empty_body_400(self, api_client_no_auth):
        payload = {}
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None
        assert (
            "Значения поля не соответствует регулярному выражению"
            in body["errors"][1]["message"]
        )
        assert body["errors"][1]["code"] == "digitCode"
        assert body["errors"][1]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/otp/phone/confirm Запрос без обязательного поля phone"
    )
    def test_registration_by_phone_confirm_otp_without_field_phone_400(
        self, api_client_no_auth, send_otp
    ):
        phone, code = send_otp
        payload = {"digitCode": code}
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/otp/phone/confirm Запрос без обязательного поля digitCode"
    )
    def test_registration_by_phone_confirm_otp_without_field_digitcode_400(
        self, api_client_no_auth, send_otp
    ):
        phone, code = send_otp
        payload = {"phone": phone}
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Значения поля не соответствует регулярному выражению"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "digitCode"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/register/otp/phone/confirm Запрос без обязательного поля digitCode"
    )
    def test_registration_by_phone_confirm_otp_phone_starting_8(
        self, api_client_no_auth, send_otp
    ):
        phone, code = send_otp
        phone_starting_8 = phone.replace("+7", "8", 1)
        payload = {"phone": phone_starting_8, "digitCode": code}
        response = api_client_no_auth.post(
            AuthEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None
