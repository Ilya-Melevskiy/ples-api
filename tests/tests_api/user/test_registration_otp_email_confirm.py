import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Регистрация")
@allure.story("Регистрация: подтвердить OTP (email)")
class TestRegistrationByOtpEmailConfirm:
    @allure.title(
        "POST /api/v1/auth/register/otp/email/confirm Успешное подтверждение OTP с корректным шестизначным кодом"
    )
    def test_registration_by_email_confirm_otp_correct_body_200(
        self, api_client_no_auth, send_otp_email
    ):
        email, code = send_otp_email
        payload = {"email": email, "digitCode": code}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_EMAIL_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Email успешно подтвержден" in body["data"]["message"]
        assert body["errors"] == []
        assert body["data"]["redirectUrl"] is None

    @allure.title(
        "POST /api/v1/auth/register/otp/email/confirm Подтверждение с неверным OTP-кодом"
    )
    def test_registration_by_email_confirm_otp_incorrect_otp_502(
        self, api_client_no_auth, send_otp_email
    ):
        email, code = send_otp_email
        incorrect_otp = "111111"
        payload = {"email": email, "digitCode": incorrect_otp}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_EMAIL_CONFIRM_OTP, json=payload
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

    @allure.title(
        "POST /api/v1/auth/register/otp/email/confirm Подтверждение для почты без @"
    )
    def test_registration_by_email_confirm_otp_email_without_at_502(
        self, api_client_no_auth, send_otp_email
    ):
        email, code = send_otp_email
        email_without_at = email.replace("@", "", 1)
        payload = {"email": email_without_at, "digitCode": code}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_EMAIL_CONFIRM_OTP, json=payload
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

    @allure.title("POST /api/v1/auth/register/otp/email/confirm Запрос с пустым телом")
    def test_registration_by_email_confirm_otp_empty_body_400(
        self, api_client_no_auth, send_otp_email
    ):
        email, code = send_otp_email
        payload = {}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_EMAIL_CONFIRM_OTP, json=payload
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
        "POST /api/v1/auth/register/otp/email/confirm Запрос без обязательного поля email"
    )
    def test_registration_by_email_confirm_otp_email_without_field_email_400(
        self, api_client_no_auth, send_otp_email
    ):
        email, code = send_otp_email
        payload = {"digitCode": code}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_EMAIL_CONFIRM_OTP, json=payload
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
        "POST /api/v1/auth/register/otp/email/confirm Запрос без обязательного поля digitCode"
    )
    def test_registration_by_email_confirm_otp_email_without_field_digitcode_400(
        self, api_client_no_auth, send_otp_email
    ):
        email, code = send_otp_email
        payload = {"email": email}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_EMAIL_CONFIRM_OTP, json=payload
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
