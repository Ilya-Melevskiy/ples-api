import re
import time


class EmailService:
    @staticmethod
    def get_otp_code(
        db_cursor,
        email: str,
        timeout: float = 15,
        poll_interval: float = 0.5,
    ) -> str:
        """
        Ждёт письмо с OTP-кодом на email в b_event.
        Ищет OTP_CODE в C_FIELDS, берёт последнее по DATE_EXEC.
        Фильтр по EVENT_NAME = EMAIL_USER_OTP_AUTH_CODE.
        Без фильтра по времени — email уникален на тест (faker), race не нужен.
        """
        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            db_cursor.execute(
                "SELECT C_FIELDS, DATE_EXEC FROM b_event "
                "WHERE EVENT_NAME = %s "
                "AND C_FIELDS LIKE %s "
                "ORDER BY DATE_EXEC DESC LIMIT 1",
                ("EMAIL_USER_OTP_AUTH_CODE", f"%{email}%"),
            )
            row = db_cursor.fetchone()

            if row and row["C_FIELDS"]:
                match = re.search(r"OTP_CODE.*?(\d{4,6})", row["C_FIELDS"])
                if match:
                    return match.group(1)

            time.sleep(poll_interval)

        raise TimeoutError(f"Код для {email} не получен за {timeout} секунд")
