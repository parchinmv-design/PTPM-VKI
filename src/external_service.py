"""
Класс сторонней зависимости.
Реализован через абстрактный базовый класс (интерфейс).
"""

from abc import ABC, abstractmethod


class ExternalService(ABC):
    """Абстрактный базовый класс для сторонних зависимостей."""

    @abstractmethod
    def send_data(self, data: str) -> bool:
        """
        Отправка данных стороннему сервису.

        Args:
            data: Данные для отправки.

        Returns:
            True, если отправка успешна, False в противном случае.
        """
        pass


class EmailService(ExternalService):
    """Реализация отправки данных через email (имитация)."""

    def send_data(self, data: str) -> bool:
        """
        Имитация отправки данных на email-сервер.

        Args:
            data: Данные для отправки.

        Returns:
            True, если отправка успешна (имитация всегда успешна).
        """
        print(f"[EmailService] Отправка данных: {data}")
        return True
