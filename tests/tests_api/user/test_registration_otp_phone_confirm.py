import allure

from api.endpoints import UserEndpoints


@allure.epic("Users")
@allure.feature("Регистрация")
@allure.story("Регистрация: подтвердить OTP (phone)")
class TestRegistrationOtpPhoneConfirm:
    @allure.title(
        "POST /api/v1/auth/register/otp/phone/confirm Успешное подтверждение OTP с корректным шестизначным кодом"
    )
    def test_registration_by_phone_confirm_otp_correct_body_200(
        self, api_client_no_auth, send_otp_phone
    ):
        phone, code = send_otp_phone
        payload = {"phone": phone, "digitCode": code}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        assert "Номер телефона успешно подтвержден" in body["data"]["message"]
        assert body["errors"] == []
        assert body["data"]["redirectUrl"] is None

    @allure.title(
        "POST /api/v1/auth/register/otp/phone/confirm Подтверждение с неверным OTP-кодом"
    )
    def test_registration_by_phone_confirm_otp_incorrect_otp_502(
        self, api_client_no_auth, send_otp_phone
    ):
        phone, code = send_otp_phone
        incorrect_code = "111111"
        payload = {"phone": phone, "digitCode": incorrect_code}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
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
        "POST /api/v1/auth/register/otp/phone/confirm Подтверждение для зарегистрированного номера"
    )
    def test_registration_by_phone_confirm_otp_existing_phone_502(
        self, api_client_no_auth, registration_natural_person
    ):
        phone = registration_natural_person["phone"]
        code = "111111"
        payload = {"phone": phone, "digitCode": code}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 502
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert (
            "Пользователь с указанным номером уже существует"
            in body["errors"][0]["message"]
        )
        assert body["errors"][0]["code"] == 0
        assert body["errors"][0]["customData"] is None

    def test_registration_by_phone_confirm_otp_empty_body_400(self, api_client_no_auth):
        payload = {}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
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
        self, api_client_no_auth, send_otp_phone
    ):
        phone, code = send_otp_phone
        payload = {"digitCode": code}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
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
        self, api_client_no_auth, send_otp_phone
    ):
        phone, code = send_otp_phone
        payload = {"phone": phone}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
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
        self, api_client_no_auth, send_otp_phone
    ):
        phone, code = send_otp_phone
        phone_starting_8 = phone.replace("+7", "8", 1)
        payload = {"phone": phone_starting_8, "digitCode": code}
        response = api_client_no_auth.post(
            UserEndpoints.REGISTRATION_PHONE_CONFIRM_OTP, json=payload
        )

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "error"
        assert body["data"] is None
        assert "Некорректный номер телефона" in body["errors"][0]["message"]
        assert body["errors"][0]["code"] == "phone"
        assert body["errors"][0]["customData"] is None
