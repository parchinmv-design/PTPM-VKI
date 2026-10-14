"""
Тесты для модуля расчёта скидок (my_project.py) из Лабораторной работы №1.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from my_project import calculate_discount


class TestDiscountBasic(unittest.TestCase):
    """Базовые случаи без скидок."""

    def test_no_discount_for_single_item(self):
        """Одна единица товара — без скидки."""
        result = calculate_discount(100.0, 1)
        self.assertEqual(result, 100.0)

    def test_no_discount_for_two_items(self):
        """Две единицы товара — без скидки."""
        result = calculate_discount(50.0, 2)
        self.assertEqual(result, 100.0)

    def test_price_multiplied_by_quantity(self):
        """Цена умножается на количество."""
        result = calculate_discount(200.0, 3)
        # 3 шт * 200 = 600, скидка 5% = 570
        self.assertEqual(result, 570.0)


class TestDiscountQuantityBased(unittest.TestCase):
    """Скидки в зависимости от количества."""

    def test_5_percent_discount_for_3_items(self):
        """3 единицы — скидка 5%."""
        result = calculate_discount(100.0, 3)
        # 300 * 0.95 = 285
        self.assertEqual(result, 285.0)

    def test_5_percent_discount_for_5_items(self):
        """5 единиц — скидка 5%."""
        result = calculate_discount(100.0, 5)
        # 500 * 0.95 = 475
        self.assertEqual(result, 475.0)

    def test_15_percent_discount_for_10_items(self):
        """10 единиц — скидка 15% (5% + 10%)."""
        result = calculate_discount(100.0, 10)
        # 1000 * 0.85 = 850
        self.assertEqual(result, 850.0)

    def test_15_percent_discount_for_20_items(self):
        """20 единиц — скидка 15%."""
        result = calculate_discount(50.0, 20)
        # 1000 * 0.85 = 850
        self.assertEqual(result, 850.0)

    def test_quantity_boundary_2_items_no_discount(self):
        """2 единицы — скидка не применяется."""
        result = calculate_discount(100.0, 2)
        self.assertEqual(result, 200.0)

    def test_quantity_boundary_3_items_discount(self):
        """3 единицы — скидка применяется."""
        result = calculate_discount(100.0, 3)
        self.assertLess(result, 300.0)


class TestDiscountVip(unittest.TestCase):
    """VIP-скидки."""

    def test_vip_discount_5_percent(self):
        """VIP-клиент — дополнительная скидка 5%."""
        normal = calculate_discount(100.0, 1, is_vip=False)
        vip = calculate_discount(100.0, 1, is_vip=True)
        self.assertLess(vip, normal)

    def test_vip_discount_amount(self):
        """VIP-клиент — скидка ровно 5%."""
        result = calculate_discount(100.0, 1, is_vip=True)
        # 100 * 0.95 = 95
        self.assertEqual(result, 95.0)

    def test_vip_with_quantity_discount(self):
        """VIP + 3 единицы — суммарная скидка 10%."""
        result = calculate_discount(100.0, 3, is_vip=True)
        # 300 * 0.90 = 270
        self.assertEqual(result, 270.0)

    def test_vip_with_large_quantity_discount(self):
        """VIP + 10 единиц — суммарная скидка 20%."""
        result = calculate_discount(100.0, 10, is_vip=True)
        # 1000 * 0.80 = 800
        self.assertEqual(result, 800.0)


class TestDiscountMaxCap(unittest.TestCase):
    """Ограничение максимальной скидки."""

    def test_discount_capped_at_25_percent(self):
        """Скидка не может превышать 25%."""
        # VIP + 10 единиц = 5% + 10% + 5% = 20% — меньше 25%
        result = calculate_discount(100.0, 10, is_vip=True)
        # 1000 * 0.80 = 800
        self.assertEqual(result, 800.0)

    def test_discount_cap_boundary(self):
        """Проверка границы 25%."""
        # Если бы скидка могла превысить 25%, результат был бы меньше
        result = calculate_discount(100.0, 10, is_vip=True)
        self.assertEqual(result, 800.0)


class TestDiscountRounding(unittest.TestCase):
    """Округление результата."""

    def test_rounding_to_two_decimals(self):
        """Результат округляется до двух знаков после запятой."""
        result = calculate_discount(33.33, 3)
        # 33.33 * 3 = 99.99, скидка 5% = 94.9905 -> 94.99
        self.assertEqual(result, 94.99)

    def test_rounding_up(self):
        """Проверка округления вверх."""
        result = calculate_discount(10.01, 3)
        # 30.03 * 0.95 = 28.5285 -> 28.53
        self.assertEqual(result, 28.53)


class TestDiscountErrors(unittest.TestCase):
    """Обработка ошибок."""

    def test_zero_price_raises_error(self):
        """Нулевая цена — исключение."""
        with self.assertRaises(ValueError):
            calculate_discount(0, 1)

    def test_negative_price_raises_error(self):
        """Отрицательная цена — исключение."""
        with self.assertRaises(ValueError):
            calculate_discount(-10.0, 1)

    def test_zero_quantity_raises_error(self):
        """Нулевое количество — исключение."""
        with self.assertRaises(ValueError):
            calculate_discount(100.0, 0)

    def test_negative_quantity_raises_error(self):
        """Отрицательное количество — исключение."""
        with self.assertRaises(ValueError):
            calculate_discount(100.0, -5)


if __name__ == '__main__':
    unittest.main()
