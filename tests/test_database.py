"""
Юнит-тесты для класса Database.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from database import Database


class TestDatabase(unittest.TestCase):
    """Тесты для класса Database."""

    def setUp(self):
        """Инициализация БД в памяти перед каждым тестом."""
        self.db = Database(":memory:")

    def tearDown(self):
        """Закрытие БД после каждого теста."""
        self.db.close()

    def test_add_and_get_record(self):
        """Добавление и получение записи."""
        record_id = self.db.add_record(100.0, 3, False, 285.0)
        self.assertIsNotNone(record_id)

        record = self.db.get_record(100.0, 3, False)
        self.assertIsNotNone(record)
        self.assertEqual(record["price"], 100.0)
        self.assertEqual(record["quantity"], 3)
        self.assertEqual(record["is_vip"], False)
        self.assertEqual(record["result"], 285.0)

    def test_get_nonexistent_record(self):
        """Получение несуществующей записи — None."""
        record = self.db.get_record(999.0, 999, False)
        self.assertIsNone(record)

    def test_delete_record(self):
        """Удаление записи."""
        record_id = self.db.add_record(100.0, 3, False, 285.0)
        deleted = self.db.delete_record(record_id)
        self.assertTrue(deleted)

        record = self.db.get_record(100.0, 3, False)
        self.assertIsNone(record)

    def test_delete_nonexistent_record(self):
        """Удаление несуществующей записи — False."""
        deleted = self.db.delete_record(9999)
        self.assertFalse(deleted)

    def test_add_record_with_error_message(self):
        """Добавление записи с сообщением об ошибке."""
        self.db.add_record(0, 1, False, 0.0, "Цена должна быть положительной")
        record = self.db.get_record(0, 1, False)
        self.assertIsNotNone(record)
        self.assertEqual(record["error_message"], "Цена должна быть положительной")


if __name__ == '__main__':
    unittest.main()
