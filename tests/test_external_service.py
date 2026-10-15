"""
Юнит-тесты для класса EmailService с использованием заглушек.
"""

import unittest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from external_service import EmailService


class TestEmailService(unittest.TestCase):
    """Тесты для сервиса отправки email."""

    def setUp(self):
        """Инициализация сервиса перед каждым тестом."""
        self.service = EmailService()

    @patch('builtins.print')
    def test_send_data_success(self, mock_print):
        """Успешная отправка данных."""
        result = self.service.send_data("Тестовые данные")
        self.assertTrue(result)
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        self.assertIn("[EmailService]", call_args)
        self.assertIn("Тестовые данные", call_args)

    @patch('builtins.print')
    def test_send_data_with_empty_string(self, mock_print):
        """Отправка пустой строки."""
        result = self.service.send_data("")
        self.assertTrue(result)
        mock_print.assert_called_once_with("[EmailService] Отправка данных: ")

    def test_send_data_return_type(self):
        """Проверка типа возвращаемого значения."""
        result = self.service.send_data("test")
        self.assertIsInstance(result, bool)


if __name__ == '__main__':
    unittest.main()
