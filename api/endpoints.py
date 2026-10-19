class AuthEndpoints:
    LOGIN_BY_EMAIL = "/api/v1/auth/login/email"
    LOGIN_BY_PHONE = "/api/v1/auth/login/phone"
    FORGOT_PASSWORD_EMAIL_SEND_OTP = "/api/v1/auth/forgotPassword/email/otp/send"
    FORGOT_PASSWORD_EMAIL_CONFIRM_OTP = "/api/v1/auth/forgotPassword/email/otp/confirm"
    FORGOT_PASSWORD_EMAIL_CHANGE_PASSWORD = (
        "/api/v1/auth/forgotPassword/email/otp/change"
    )
    FORGOT_PASSWORD_PHONE_SEND_OTP = "/api/v1/auth/forgotPassword/phone/otp/send"
    FORGOT_PASSWORD_PHONE_CONFIRM_OTP = "/api/v1/auth/forgotPassword/phone/otp/confirm"
    FORGOT_PASSWORD_PHONE_CHANGE_OTP = "/api/v1/auth/forgotPassword/phone/otp/change"
    LOGOUT = "/api/v1/auth/logout "
    REGISTRATION_EMAIL_SEND_OTP = "/api/v1/auth/register/otp/email/send"
    REGISTRATION_EMAIL_CONFIRM_OTP = "/api/v1/auth/register/otp/email/confirm"
    REGISTRATION_PHONE_SEND_OTP = "/api/v1/auth/register/otp/phone/send"
    REGISTRATION_PHONE_CONFIRM = "/api/v1/auth/register/otp/phone/confirm"
    COMPLETION_REGISTRATION = "/api/v1/auth/register/submit  "
