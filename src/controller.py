"""
Класс-контроллер (Controller).
Реализует бизнес-логику сквозного сценария.
"""

from typing import Tuple, Optional
from calculator import DiscountCalculator
from database import Database
from user_interface import UserInterface
from external_service import ExternalService


class Controller:
    """
    Класс-контроллер, реализующий бизнес-логику сквозного сценария.

    Сценарий:
    1. Запрос входных данных у пользователя.
    2. Проверка наличия записи в БД:
       - Если записи нет -> вычислить результат и добавить в БД.
       - Если запись есть -> взять результат из БД.
    3. Отправка результата сторонней зависимости.
    4. Возврат результата.
    """

    def __init__(self, calculator: DiscountCalculator, database: Database,
                 user_interface: UserInterface, external_service: ExternalService):
        """
        Инициализация контроллера с зависимостями.

        Args:
            calculator: Экземпляр класса вычислений.
            database: Экземпляр класса работы с БД.
            user_interface: Экземпляр класса взаимодействия с пользователем.
            external_service: Экземпляр класса сторонней зависимости.
        """
        self.calculator = calculator
        self.database = database
        self.user_interface = user_interface
        self.external_service = external_service

    def process(self) -> Optional[float]:
        """
        Основной метод обработки сквозного сценария.

        Returns:
            Результат вычисления или None в случае ошибки.
        """
        try:
            # Шаг 1: Получение входных данных
            price, quantity, is_vip = self.user_interface.get_input()

            # Шаг 2: Проверка наличия записи в БД
            existing_record = self.database.get_record(price, quantity, is_vip)

            if existing_record:
                # Запись найдена — берём результат из БД
                result = existing_record["result"]
                error_message = existing_record["error_message"]
                if error_message:
                    self.user_interface.display_error(error_message)
                    return None
            else:
                # Записи нет — вычисляем результат
                try:
                    result = self.calculator.calculate_discount(price, quantity, is_vip)
                    self.database.add_record(price, quantity, is_vip, result)
                except ValueError as e:
                    error_message = str(e)
                    self.database.add_record(price, quantity, is_vip, 0.0, error_message)
                    self.user_interface.display_error(error_message)
                    return None

            # Шаг 3: Отправка результата сторонней зависимости
            self.external_service.send_data(
                f"Результат вычисления: цена={price}, количество={quantity}, "
                f"VIP={is_vip}, итого={result}"
            )

            # Шаг 4: Отображение и возврат результата
            self.user_interface.display_result(result)
            return result

        except Exception as e:
            self.user_interface.display_error(str(e))
            return None
