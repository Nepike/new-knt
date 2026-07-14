from django.core.mail.backends.console import EmailBackend


class DevConsoleBackend(EmailBackend):
    """Печатает письмо в читаемом виде — стандартный console-бекенд выводит сырой MIME (base64 для кириллицы)."""

    def write_message(self, message):
        self.stream.write(f"От: {message.from_email}\nКому: {', '.join(message.to)}\nТема: {message.subject}\n\n{message.body}\n")
        self.stream.write("-" * 79 + "\n")
