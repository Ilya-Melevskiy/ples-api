import re
import time


class SMSService:
    @staticmethod
    def get_otp_code(
        db_cursor,
        phone: str,
        timeout: float = 5,
        poll_interval: float = 0.5,
    ) -> str:
        """
        Ждёт SMS-код, появившийся в b_event_log ПОСЛЕ старта метода.
        Не требует old_code: фильтрует по TIMESTAMP_X.
        Бросает SMSCodeTimeoutError при таймауте.
        """

        phone_with_plus = phone if phone.startswith("+") else f"+{phone}"

        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            db_cursor.execute(
                "SELECT DESCRIPTION, TIMESTAMP_X FROM b_event_log "
                "WHERE AUDIT_TYPE_ID=%s AND ITEM_ID=%s "
                "ORDER BY TIMESTAMP_X DESC LIMIT 1",
                ("Debug SMS", phone_with_plus),
            )
            message = db_cursor.fetchone()

            if message and message["DESCRIPTION"]:
                match = re.search(r"\b\d{4,6}\b", message["DESCRIPTION"])
                if match:
                    return match.group(0)

            time.sleep(poll_interval)

        raise TimeoutError(f"Новый код для {phone} не получен за {timeout} секунд")
