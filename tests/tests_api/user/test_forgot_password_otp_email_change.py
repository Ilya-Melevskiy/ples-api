import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Восстановление пароля")
@allure.story("Восстановление пароля: сменить пароль (email)")
class TestForgotPasswordByOtpEmailChange:
    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/change Успешная смена пароля по почте"
    )
    def test_forgot_password_by_email_change_correct_body_200(
        self, api_client_no_auth, forgot_password_confirm_otp_email, faker_ru
    ):
        email = forgot_password_confirm_otp_email
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"email": email, "newPassword": new_password}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CHANGE_PASSWORD, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Смена пароля прошла успешно" in body["data"]["message"]
        assert body["errors"] == []
        assert body["data"]["redirectUrl"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/change Вход с новым паролем после смены"
    )
    def test_forgot_password_by_email_change_login_after_change_200(
        self, api_client_no_auth, forgot_password_confirm_otp_email, faker_ru
    ):
        email = forgot_password_confirm_otp_email
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"email": email, "newPassword": new_password}
        api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CHANGE_PASSWORD, json=payload
        )
        payload = {"email": email, "password": new_password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Авторизация прошла успешно" in body["data"]["message"]
        assert body["errors"] == []
        assert body["data"]["redirectUrl"] == "/"

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/change Вход со старым паролем не работает"
    )
    def test_forgot_password_by_email_change_login_with_old_password_after_change_502(
        self,
        api_client_no_auth,
        forgot_password_send_otp_email,
        forgot_password_confirm_otp_email,
        faker_ru,
    ):
        email, old_password = forgot_password_send_otp_email
        email = forgot_password_confirm_otp_email
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"email": email, "newPassword": new_password}
        api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CHANGE_PASSWORD, json=payload
        )

        payload = {"email": email, "password": old_password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_EMAIL, json=payload)

        assert response.status_code == 502
        body = response.json()
        assert body["data"] is None
        assert (
            "Введен некорректный email или неверный пароль"
            in body["errors"][0]["message"]
        )
        assert body["status"] == "error"
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/change Change без предварительного confirm"
    )
    def test_forgot_password_by_email_change_before_confirm_502(
        self, api_client_no_auth, registration_natural_person, faker_ru
    ):
        email = registration_natural_person["email"]
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"email": email, "newPassword": new_password}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CHANGE_PASSWORD, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["data"] is None
        assert body["status"] == "error"
        assert (
            "Unauthorized request to change the user's password"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/change Change из другой сессии"
    )
    def test_forgot_password_by_email_change_another_session_502(
        self, api_client_no_auth, forgot_password_confirm_otp_email, faker_ru
    ):
        api_client_no_auth.session.cookies.clear()
        email = forgot_password_confirm_otp_email
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"email": email, "newPassword": new_password}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CHANGE_PASSWORD, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["data"] is None
        assert body["status"] == "error"
        assert (
            "Unauthorized request to change the user's password"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/change Запрос с пустым телом"
    )
    def test_forgot_password_by_email_change_empty_body_400(self, api_client_no_auth):
        payload = {}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CHANGE_PASSWORD, json=payload
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
        assert "Значение поля не может быть пустым" in body["errors"][1]["message"]
        assert body["errors"][1]["code"] == "newPassword"
        assert body["errors"][1]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/email/otp/change Запрос без обязательного поля email"
    )
    def test_forgot_password_by_email_change_without_field_email_400(
        self, api_client_no_auth, faker_ru
    ):
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"newPassword": new_password}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CHANGE_PASSWORD, json=payload
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
        "POST /api/v1/auth/forgotPassword/email/otp/change Запрос без обязательного поля newPassword"
    )
    def test_forgot_password_by_email_change_without_field_new_password_400(
        self, api_client_no_auth, forgot_password_confirm_otp_email
    ):
        email = forgot_password_confirm_otp_email
        payload = {"email": email}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_EMAIL_CHANGE_PASSWORD, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Значение поля не может быть пустым" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "newPassword"
        assert body["errors"][0]["customData"] is None
