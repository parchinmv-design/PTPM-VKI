"""
Юнит-тесты для класса DiscountCalculator.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from calculator import DiscountCalculator


class TestDiscountCalculator(unittest.TestCase):
    """Тесты для класса DiscountCalculator."""

    def setUp(self):
        """Инициализация калькулятора перед каждым тестом."""
        self.calc = DiscountCalculator()

    def test_no_discount_for_single_item(self):
        """Одна единица товара — без скидки."""
        result = self.calc.calculate_discount(100.0, 1)
        self.assertEqual(result, 100.0)

    def test_5_percent_discount_for_3_items(self):
        """3 единицы — скидка 5%."""
        result = self.calc.calculate_discount(100.0, 3)
        self.assertEqual(result, 285.0)

    def test_15_percent_discount_for_10_items(self):
        """10 единиц — скидка 15% (5% + 10%)."""
        result = self.calc.calculate_discount(100.0, 10)
        self.assertEqual(result, 850.0)

    def test_vip_discount_5_percent(self):
        """VIP-клиент — дополнительная скидка 5%."""
        result = self.calc.calculate_discount(100.0, 1, is_vip=True)
        self.assertEqual(result, 95.0)

    def test_vip_with_quantity_discount(self):
        """VIP + 3 единицы — суммарная скидка 10%."""
        result = self.calc.calculate_discount(100.0, 3, is_vip=True)
        self.assertEqual(result, 270.0)

    def test_zero_price_raises_error(self):
        """Нулевая цена — исключение."""
        with self.assertRaises(ValueError):
            self.calc.calculate_discount(0, 1)

    def test_negative_quantity_raises_error(self):
        """Отрицательное количество — исключение."""
        with self.assertRaises(ValueError):
            self.calc.calculate_discount(100.0, -5)

    def test_discount_cap_at_25_percent(self):
        """Скидка не может превышать 25%."""
        result = self.calc.calculate_discount(100.0, 10, is_vip=True)
        self.assertEqual(result, 800.0)


if __name__ == '__main__':
    unittest.main()
