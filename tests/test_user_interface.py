"""
Юнит-тесты для класса ConsoleInterface с использованием заглушек.
"""

import unittest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from user_interface import ConsoleInterface


class TestConsoleInterface(unittest.TestCase):
    """Тесты для консольного интерфейса."""

    def setUp(self):
        """Инициализация интерфейса перед каждым тестом."""
        self.ui = ConsoleInterface()

    @patch('builtins.input', side_effect=['100.0', '3', 'нет'])
    def test_get_input_not_vip(self, mock_input):
        """Получение входных данных (не VIP)."""
        price, quantity, is_vip = self.ui.get_input()
        self.assertEqual(price, 100.0)
        self.assertEqual(quantity, 3)
        self.assertEqual(is_vip, False)

    @patch('builtins.input', side_effect=['200.0', '5', 'да'])
    def test_get_input_vip(self, mock_input):
        """Получение входных данных (VIP)."""
        price, quantity, is_vip = self.ui.get_input()
        self.assertEqual(price, 200.0)
        self.assertEqual(quantity, 5)
        self.assertEqual(is_vip, True)

    @patch('builtins.print')
    def test_display_result(self, mock_print):
        """Отображение результата."""
        self.ui.display_result(285.0)
        mock_print.assert_called_once_with("Результат: 285.0")

    @patch('builtins.print')
    def test_display_error(self, mock_print):
        """Отображения ошибки."""
        self.ui.display_error("Цена должна быть положительной")
        mock_print.assert_called_once_with("Ошибка: Цена должна быть положительной")


if __name__ == '__main__':
    unittest.main()
