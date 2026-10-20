import re
import time


class EmailService:
    @staticmethod
    def get_otp_code(
        db_cursor,
        email: str,
        timeout: float = 5,
        poll_interval: float = 0.5,
        event_name: str = "EMAIL_USER_OTP_AUTH_CODE",
    ) -> str:
        """
        Ждёт письмо с OTP-кодом на email, появившееся в b_event после старта метода.
        Ищет OTP_CODE в C_FIELDS, сортирует по DATE_EXEC (последнее — первым).
        Фильтрует по EVENT_NAME (по умолчанию — EMAIL_USER_OTP_AUTH_CODE).
        """
        db_cursor.execute("SELECT NOW() AS start_time")
        start_time = db_cursor.fetchone()["start_time"]

        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            db_cursor.execute(
                "SELECT C_FIELDS, DATE_EXEC FROM b_event "
                "WHERE EVENT_NAME = %s "
                "AND C_FIELDS LIKE %s "
                "AND DATE_EXEC >= %s "
                "ORDER BY DATE_EXEC DESC LIMIT 1",
                (event_name, f"%{email}%", start_time),
            )
            row = db_cursor.fetchone()

            if row and row["C_FIELDS"]:
                match = re.search(r"OTP_CODE.*?(\d{4,6})", row["C_FIELDS"])
                if match:
                    return match.group(1)

            time.sleep(poll_interval)

        raise TimeoutError(f"Код для {email} не получен за {timeout} секунд")
