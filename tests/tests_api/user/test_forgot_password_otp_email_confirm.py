import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Восстановление пароля")
@allure.story("Восстановление пароля: подтвердить OTP (email)")
class TestForgotPasswordByOtpEmailConfirm:
    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/confirm Успешное подтверждение OTP с корректным шестизначным кодом"
    )
    def test_forgot_password_by_email_confirm_otp_correct_body_200(
        self, api_client_no_auth, forgot_password_send_otp_email
    ):
        email, code = forgot_password_send_otp_email
        payload = {"email": email, "digitCode": code}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Email успешно верифицирован" in body["data"]["message"]
        assert body["errors"] == []
        assert body["data"]["redirectUrl"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/confirm Подтверждение с неверным OTP-кодом"
    )
    def test_forgot_password_by_email_confirm_otp_incorrect_otp_502(
        self, api_client_no_auth, forgot_password_send_otp_email
    ):
        email, code = forgot_password_send_otp_email
        incorrect_code = "111111"
        payload = {"email": email, "digitCode": incorrect_code}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Ошибка верификации Email" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/confirm Подтверждение для не зарегистрированной почты"
    )
    def test_forgot_password_by_email_confirm_otp_unregistered_email_502(
        self, api_client_no_auth, faker_ru
    ):
        email = faker_ru.email()
        code = faker_ru.numerify(text="######")
        payload = {"email": email, "digitCode": code}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Пользователь с указанной эл. почтой не существует"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/confirm Запрос с пустым телом"
    )
    def test_forgot_password_by_email_confirm_otp_empty_body_400(
        self, api_client_no_auth
    ):
        payload = {}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CONFIRM_OTP, json=payload
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

        assert (
            "Значения поля не соответствует регулярному выражению"
            in body["errors"][1]["message"]
        )
        assert body["errors"][1]["code"] == "digitCode"
        assert body["errors"][1]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/confirm Запрос без обязательного поля email"
    )
    def test_forgot_password_by_email_confirm_otp_without_field_email_400(
        self, api_client_no_auth, faker_ru
    ):
        code = faker_ru.numerify(text="######")
        payload = {"digitCode": code}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CONFIRM_OTP, json=payload
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
        "POST /api/v1/auth/forgotPassword/email/otp/confirm Запрос без обязательного поля digitCode"
    )
    def test_forgot_password_by_email_confirm_otp_without_field_digit_code_400(
        self, api_client_no_auth, faker_ru
    ):
        email = faker_ru.email()
        payload = {"email": email}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CONFIRM_OTP, json=payload
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
