import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Восстановление пароля")
@allure.story("Восстановление пароля: сменить пароль (phone)")
class TestForgotPasswordByOtpPhoneChange:
    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/change Успешная смена пароля по SMS"
    )
    def test_forgot_password_by_phone_change_correct_body_200(
        self, api_client_no_auth, forgot_password_confirm_otp_phone, faker_ru
    ):
        phone = forgot_password_confirm_otp_phone
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"phone": phone, "newPassword": new_password}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CHANGE_PASSWORD, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Смена пароля прошла успешно" in body["data"]["message"]
        assert body["errors"] == []
        assert body["data"]["redirectUrl"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/change Вход с новым паролем после смены"
    )
    def test_forgot_password_by_phone_change_login_after_change_200(
        self, api_client_no_auth, forgot_password_confirm_otp_phone, faker_ru
    ):
        phone = forgot_password_confirm_otp_phone
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"phone": phone, "newPassword": new_password}
        api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CHANGE_PASSWORD, json=payload
        )
        payload = {"phone": phone, "password": new_password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Авторизация прошла успешно" in body["data"]["message"]
        assert body["errors"] == []
        assert body["data"]["redirectUrl"] == "/"

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/change Вход со старым паролем не работает"
    )
    def test_forgot_password_by_phone_change_login_with_old_password_after_change_502(
        self,
        api_client_no_auth,
        forgot_password_send_otp_phone,
        forgot_password_confirm_otp_phone,
        faker_ru,
    ):
        phone, old_password = forgot_password_send_otp_phone
        phone = forgot_password_confirm_otp_phone
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"phone": phone, "newPassword": new_password}
        api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CHANGE_PASSWORD, json=payload
        )

        payload = {"phone": phone, "password": old_password}
        response = api_client_no_auth.post(UserEndpoints.LOGIN_BY_PHONE, json=payload)

        assert response.status_code == 502
        body = response.json()
        assert body["data"] is None
        assert (
            "Введен некорректный номер телефона или неверный пароль"
            in body["errors"][0]["message"]
        )
        assert body["status"] == "error"
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/change Change без предварительного confirm"
    )
    def test_forgot_password_by_phone_change_before_confirm_502(
        self, api_client_no_auth, registration_natural_person, faker_ru
    ):
        phone = registration_natural_person["phone"]
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"phone": phone, "newPassword": new_password}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CHANGE_PASSWORD, json=payload
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
        "POST /api/v1/auth/forgotPassword/phone/otp/change Change из другой сессии"
    )
    def test_forgot_password_by_phone_change_another_session_502(
        self, api_client_no_auth, forgot_password_confirm_otp_phone, faker_ru
    ):
        api_client_no_auth.session.cookies.clear()
        phone = forgot_password_confirm_otp_phone
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"phone": phone, "newPassword": new_password}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CHANGE_PASSWORD, json=payload
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
        "POST /api/v1/auth/forgotPassword/phone/otp/change Запрос с пустым телом"
    )
    def test_forgot_password_by_phone_change_empty_body_400(self, api_client_no_auth):
        payload = {}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CHANGE_PASSWORD, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефон" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None
        assert "Не указан пароль" in body["errors"][1]["message"]
        assert body["errors"][1]["code"] == "newPassword"
        assert body["errors"][1]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/change Запрос без обязательного поля phone"
    )
    def test_forgot_password_by_phone_change_without_field_phone_400(
        self, api_client_no_auth, faker_ru
    ):
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"newPassword": new_password}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CHANGE_PASSWORD, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефон" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/change Запрос без обязательного поля newPassword"
    )
    def test_forgot_password_by_phone_change_without_field_new_password_400(
        self, api_client_no_auth, forgot_password_confirm_otp_phone
    ):
        phone = forgot_password_confirm_otp_phone
        payload = {"phone": phone}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CHANGE_PASSWORD, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Не указан пароль" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "newPassword"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/change Запрос с телефоном, начинающимся с 8"
    )
    def test_forgot_password_by_phone_change_phone_starting_8_400(
        self, api_client_no_auth, forgot_password_confirm_otp_phone, faker_ru
    ):
        phone = forgot_password_confirm_otp_phone
        phone_starting_8 = phone.replace("+7", "8")
        new_password = f"a1{faker_ru.password(length=4)}"
        payload = {"phone": phone_starting_8, "newPassword": new_password}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CHANGE_PASSWORD, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/change Запрос с newPassword из 5 символов"
    )
    def test_forgot_password_by_phone_change_password_5_symbols_400(
        self, api_client_no_auth, forgot_password_confirm_otp_phone, faker_ru
    ):
        phone = forgot_password_confirm_otp_phone
        new_password = f"a1{faker_ru.password(length=3, digits=False)}"
        payload = {"phone": phone, "newPassword": new_password}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CHANGE_PASSWORD, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Пароль должен  быть не менее 6 символов длиной"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None
