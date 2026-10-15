"""
Класс взаимодействия с пользователем.
Реализован через абстрактный базовый класс (интерфейс).
"""

from abc import ABC, abstractmethod
from typing import Tuple


class UserInterface(ABC):
    """Абстрактный базовый класс для взаимодействия с пользователем."""

    @abstractmethod
    def get_input(self) -> Tuple[float, int, bool]:
        """
        Получение входных данных от пользователя.

        Returns:
            Кортеж (price, quantity, is_vip).
        """
        pass

    @abstractmethod
    def display_result(self, result: float) -> None:
        """
        Отображение результата пользователю.

        Args:
            result: Результат вычисления.
        """
        pass

    @abstractmethod
    def display_error(self, message: str) -> None:
        """
        Отображение ошибки пользователю.

        Args:
            message: Сообщение об ошибке.
        """
        pass


class ConsoleInterface(UserInterface):
    """Консольная реализация интерфейса пользователя."""

    def get_input(self) -> Tuple[float, int, bool]:
        """
        Получение входных данных через консоль.

        Returns:
            Кортеж (price, quantity, is_vip).
        """
        price = float(input("Введите цену товара: "))
        quantity = int(input("Введите количество товара: "))
        is_vip = input("Является ли клиент VIP? (да/нет): ").strip().lower() == "да"
        return price, quantity, is_vip

    def display_result(self, result: float) -> None:
        """Вывод результата в консоль."""
        print(f"Результат: {result}")

    def display_error(self, message: str) -> None:
        """Вывод ошибки в консоль."""
        print(f"Ошибка: {message}")
