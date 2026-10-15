"""
Интеграционные тесты для класса Controller.
Используются тестовые заглушки (mock) для изоляции модулей.
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from controller import Controller
from calculator import DiscountCalculator
from database import Database


class TestControllerIntegration(unittest.TestCase):
    """Интеграционные тесты для сквозного сценария Controller."""

    def setUp(self):
        """Инициализация компонентов перед каждым тестом."""
        self.calculator = DiscountCalculator()
        self.database = Database(":memory:")
        self.mock_ui = Mock()
        self.mock_external = Mock()
        self.controller = Controller(
            self.calculator, self.database, self.mock_ui, self.mock_external
        )

    def tearDown(self):
        """Закрытие БД после каждого теста."""
        self.database.close()

    def test_full_scenario_new_calculation(self):
        """
        Интеграционный тест: полный сценарий с новым вычислением.
        Запись отсутствует в БД -> вычисление -> сохранение -> отправка.
        """
        # Настройка заглушек
        self.mock_ui.get_input.return_value = (100.0, 3, False)
        self.mock_external.send_data.return_value = True

        # Выполнение
        result = self.controller.process()

        # Проверки
        self.assertEqual(result, 285.0)
        self.mock_ui.get_input.assert_called_once()
        self.mock_external.send_data.assert_called_once()
        self.mock_ui.display_result.assert_called_once_with(285.0)

        # Проверка, что запись добавлена в БД
        record = self.database.get_record(100.0, 3, False)
        self.assertIsNotNone(record)
        self.assertEqual(record["result"], 285.0)

    def test_full_scenario_existing_record(self):
        """
        Интеграционный тест: полный сценарий с существующей записью.
        Запись есть в БД -> результат берется из БД -> отправка.
        """
        # Предварительное добавление записи в БД
        self.database.add_record(100.0, 5, True, 427.5)

        # Настройка заглушек
        self.mock_ui.get_input.return_value = (100.0, 5, True)
        self.mock_external.send_data.return_value = True

        # Выполнение
        result = self.controller.process()

        # Проверки
        self.assertEqual(result, 427.5)
        self.mock_ui.get_input.assert_called_once()
        self.mock_external.send_data.assert_called_once()
        self.mock_ui.display_result.assert_called_once_with(427.5)

    def test_full_scenario_with_error(self):
        """
        Интеграционный тест: сценарий с ошибкой валидации.
        Ошибка -> сохранение в БД -> отображение ошибки.
        """
        # Настройка заглушек
        self.mock_ui.get_input.return_value = (0, 1, False)
        self.mock_external.send_data.return_value = True

        # Выполнение
        result = self.controller.process()

        # Проверки
        self.assertIsNone(result)
        self.mock_ui.display_error.assert_called_once()
        self.mock_external.send_data.assert_not_called()

    def test_full_scenario_vip_discount(self):
        """
        Интеграционный тест: сценарий со VIP-скидкой.
        """
        # Настройка заглушек
        self.mock_ui.get_input.return_value = (200.0, 10, True)
        self.mock_external.send_data.return_value = True

        # Выполнение
        result = self.controller.process()

        # Проверки (200 * 10 * 0.80 = 1600)
        self.assertEqual(result, 1600.0)
        self.mock_ui.display_result.assert_called_once_with(1600.0)


if __name__ == '__main__':
    unittest.main()
