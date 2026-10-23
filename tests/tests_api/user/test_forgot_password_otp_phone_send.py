import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Восстановление пароля")
@allure.story("Восстановление пароля: отправить OTP (phone)")
class TestForgotPasswordOtpPhoneSend:
    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/send Восстановление пароля: отправить OTP (phone)"
    )
    def test_forgot_password_by_phone_send_otp_correct_body_200(
        self, api_client_no_auth, registration_natural_person
    ):
        phone = registration_natural_person["phone"]
        payload = {"phone": phone}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_SEND_OTP, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert (
            f"На указанный номер телефона {phone} отправлено СМС с кодом подтверждения операции"
            in body["data"]["message"]
        )
        assert body["data"]["redirectUrl"] is None
        assert body["errors"] == []

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/send Повторная отправка раньше минуты"
    )
    def test_forgot_password_by_phone_send_otp_before_minute_502(
        self, api_client_no_auth, registration_natural_person
    ):
        phone = registration_natural_person["phone"]
        payload = {"phone": phone}
        api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_SEND_OTP, json=payload
        )
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_SEND_OTP, json=payload
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

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/send Отправка на не зарегистрированный номер"
    )
    def test_forgot_password_by_phone_send_otp_unregistered_phone_502(
        self, api_client_no_auth, faker_phone_number_starting_plus_7
    ):
        phone = faker_phone_number_starting_plus_7()
        payload = {"phone": phone}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_SEND_OTP, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Пользователь с указанным номером телефона не найден."
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/send Запрос с пустым телом"
    )
    def test_forgot_password_by_phone_send_otp_empty_body_400(self, api_client_no_auth):
        payload = {}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_SEND_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/send Запрос с номером, начинающимся с 8"
    )
    def test_forgot_password_by_phone_send_otp_phone_starting_8_400(
        self, api_client_no_auth, registration_natural_person
    ):
        phone = registration_natural_person["phone"]
        phone_starting_8 = phone.replace("+7", "8")
        payload = {"phone": phone_starting_8}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_SEND_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/send Запрос с номером из 10 цифр"
    )
    def test_forgot_password_by_phone_send_otp_phone_10_numbers_400(
        self, api_client_no_auth, faker_phone_number_starting_plus_7
    ):
        phone = faker_phone_number_starting_plus_7()[:-1]
        payload = {"phone": phone}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_SEND_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/send Запрос с номером из 12 цифр"
    )
    def test_forgot_password_by_phone_send_otp_phone_12_numbers_400(
        self, api_client_no_auth, faker_phone_number_starting_plus_7
    ):
        phone = f"{faker_phone_number_starting_plus_7()}12"
        payload = {"phone": phone}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_SEND_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None
