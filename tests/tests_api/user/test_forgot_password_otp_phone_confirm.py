import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Восстановление пароля")
@allure.story("Восстановление пароля: подтвердить OTP (phone)")
class TestForgotPasswordByOtpPhoneConfirm:
    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/confirm Успешное подтверждение OTP с корректным шестизначным кодом"
    )
    def test_forgot_password_by_phone_confirm_otp_correct_body_200(
        self, api_client_no_auth, forgot_password_send_otp_phone
    ):
        phone, code = forgot_password_send_otp_phone
        payload = {"phone": phone, "digitCode": code}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Номер телефона успешно верифицирован" in body["data"]["message"]
        assert body["errors"] == []
        assert body["data"]["redirectUrl"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/confirm Подтверждение с неверным OTP-кодом"
    )
    def test_forgot_password_by_phone_confirm_otp_incorrect_otp_502(
        self, api_client_no_auth, forgot_password_send_otp_phone
    ):
        phone, code = forgot_password_send_otp_phone
        incorrect_code = "111111"
        payload = {"phone": phone, "digitCode": incorrect_code}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Ошибка верификации номера телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/confirm Подтверждение для не зарегистрированного номера"
    )
    def test_forgot_password_by_phone_confirm_otp_unregistered_phone_502(
        self, api_client_no_auth, faker_phone_number_starting_plus_7, faker_ru
    ):
        phone = faker_phone_number_starting_plus_7()
        code = faker_ru.numerify(text="######")
        payload = {"phone": phone, "digitCode": code}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Пользователь с указанным номером не существует"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/confirm Запрос с пустым телом"
    )
    def test_forgot_password_by_phone_confirm_otp_empty_body_400(
        self, api_client_no_auth
    ):
        payload = {}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CONFIRM_OTP, json=payload
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
        "POST /api/v1/auth/forgotPassword/phone/otp/confirm Запрос без обязательного поля phone"
    )
    def test_forgot_password_by_phone_confirm_otp_without_phone_400(
        self, api_client_no_auth, faker_ru
    ):
        code = faker_ru.numerify(text="#" * 6)
        payload = {"code": code}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None

    @allure.title(
        "POST /api/v1/auth/forgotPassword/phone/otp/confirm Запрос без обязательного поля digitCode"
    )
    def test_forgot_password_by_phone_confirm_otp_without_digit_code_400(
        self, api_client_no_auth, registration_natural_person
    ):
        phone = registration_natural_person["phone"]
        payload = {"phone": phone}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CONFIRM_OTP, json=payload
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
        "POST /api/v1/auth/forgotPassword/phone/otp/confirm Запрос без обязательного поля digitCode"
    )
    def test_forgot_password_by_phone_confirm_otp_phone_starting_8_400(
        self, api_client_no_auth, registration_natural_person
    ):
        phone = registration_natural_person["phone"]
        phone_starting_8 = phone.replace("+7", "8")
        payload = {"phone": phone_starting_8}
        response = api_client_no_auth.post(
            UserEndpoints.FORGOT_PASSWORD_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None
