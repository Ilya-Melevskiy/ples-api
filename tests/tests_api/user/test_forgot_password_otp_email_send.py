import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Восстановление пароля")
@allure.story("Восстановление пароля: Отправить OTP (email)")
class TestForgotPasswordOtpEmailSend:
    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/send Успешная отправка OTP на не зарегистрированный email"
    )
    def test_forgot_password_by_email_send_otp_correct_body_200(
        self, api_client_no_auth, registration_natural_person
    ):
        email = registration_natural_person["email"]
        payload = {"email": email}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_SEND_OTP, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert (
            f"На указанный Email {email} отправлен временный код подтверждения"
            in body["data"]["message"]
        )
        assert body["data"]["redirectUrl"] is None
        assert body["errors"] == []

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/send Повторная отправка раньше минуты"
    )
    def test_forgot_password_by_email_send_otp_before_minute_502(
        self, api_client_no_auth, registration_natural_person
    ):
        email = registration_natural_person["email"]
        payload = {"email": email}
        api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_SEND_OTP, json=payload
        )
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_SEND_OTP, json=payload
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
        "POST /api/v1/auth/forgotPassword/email/otp/send Отправка на не зарегистрированный email"
    )
    def test_forgot_password_by_email_send_otp_unregistered_email_502(
        self, api_client_no_auth, faker_ru
    ):
        email = faker_ru.email()
        payload = {"email": email}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_SEND_OTP, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Пользователь с указанной эл. почтой не найден"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/send Запрос с пустым телом"
    )
    def test_forgot_password_by_email_send_otp_empty_body_400(self, api_client_no_auth):

        payload = {}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_SEND_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Значение поля не является адресом электронной почты"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "email"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/send Запрос с email без @"
    )
    def test_forgot_password_by_email_send_otp_email_without_at_400(
        self, api_client_no_auth, registration_natural_person
    ):
        email = registration_natural_person["email"]
        email_without_at = email.replace("@", "")
        payload = {"email": email_without_at}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_SEND_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Значение поля не является адресом электронной почты"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == "email"
        assert body["errors"][0]["customData"] is None
