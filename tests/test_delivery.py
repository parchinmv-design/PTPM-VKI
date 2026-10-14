"""
Тесты для модуля расчёта стоимости доставки (delivery_service.py).
Проверяют корректность бизнес-логики: тарифы, весовые коэффициенты,
типы посылок, экспресс-доставку и сроки.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from delivery_service import calculate_delivery_cost


class TestDeliveryBasicTariff(unittest.TestCase):
    """Базовые тарифы без доп. коэффициентов."""

    def test_minimum_distance_cost(self):
        """Минимальная дистанция (1 км), лёгкая посыка, обычный тип."""
        cost, date = calculate_delivery_cost(0.5, 1, "обычный")
        # 200 + 1*5 = 205
        self.assertEqual(cost, 205)

    def test_distance_cost_linear(self):
        """Стоимость линейно зависит от дистанции."""
        cost_100, _ = calculate_delivery_cost(0.5, 100, "обычный")
        cost_200, _ = calculate_delivery_cost(0.5, 200, "обычный")
        # Разница должна быть ровно 100 * 5 = 500
        self.assertEqual(cost_200 - cost_100, 500)

    def test_base_cost_plus_distance(self):
        """Базовая стоимость 200 + дистанция * 5."""
        cost, _ = calculate_delivery_cost(0.5, 300, "обычный")
        # 200 + 300*5 = 1700
        self.assertEqual(cost, 1700)

    def test_light_package_no_weight_surcharge(self):
        """Вес до 5 кг не добавляет коэффициент."""
        cost_3kg, _ = calculate_delivery_cost(3.0, 100, "обычный")
        cost_5kg, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost_3kg, cost_5kg)


class TestDeliveryWeightCoefficients(unittest.TestCase):
    """Весовые коэффициенты."""

    def test_weight_between_5_and_20_adds_20_percent(self):
        """Вес от 5 до 20 кг добавляет коэффициент 1.2."""
        base_cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        heavy_cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        # (200 + 500) * 1.2 = 840
        self.assertEqual(heavy_cost, 840)

    def test_weight_20_and_above_adds_50_percent(self):
        """Вес от 20 кг добавляет коэффициент 1.5."""
        heavy_cost, _ = calculate_delivery_cost(25.0, 100, "обычный")
        # (200 + 500) * 1.5 = 1050
        self.assertEqual(heavy_cost, 1050)

    def test_weight_boundary_5_kg_no_surcharge(self):
        """Вес ровно 5 кг — коэффициент не применяется."""
        cost_5, _ = calculate_delivery_cost(5.0, 100, "обычный")
        cost_4_9, _ = calculate_delivery_cost(4.9, 100, "обычный")
        self.assertEqual(cost_5, cost_4_9)

    def test_weight_boundary_20_kg(self):
        """Вес ровно 20 кг — применяется коэффициент 1.5."""
        cost_20, _ = calculate_delivery_cost(20.0, 100, "обычный")
        cost_19_9, _ = calculate_delivery_cost(19.9, 100, "обычный")
        # 20 кг должна стоить дороже, чем 19.9 кг
        self.assertGreater(cost_20, cost_19_9)


class TestDeliveryPackageTypes(unittest.TestCase):
    """Надбавки за тип посылки."""

    def test_fragile_package_adds_300(self):
        """Хрупкая посылка добавляет 300 рублей."""
        base_cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        fragile_cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(fragile_cost - base_cost, 300)

    def test_dangerous_package_adds_1000(self):
        """Опасная посылка добавляет 1000 рублей."""
        base_cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        dangerous_cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(dangerous_cost - base_cost, 1000)

    def test_ordinary_package_no_surcharge(self):
        """Обычная посылка не имеет надбавки."""
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

    def test_fragile_with_weight_coefficient(self):
        """Хрупкая посылка с весом > 5 кг: надбавка после коэффициента."""
        cost, _ = calculate_delivery_cost(10.0, 100, "хрупкий")
        # (200 + 500) * 1.2 + 300 = 1140
        self.assertEqual(cost, 1140)


class TestDeliveryExpress(unittest.TestCase):
    """Экспресс-доставка."""

    def test_express_increases_cost(self):
        """Экспресс-доставка должна увеличивать стоимость, а не уменьшать."""
        normal_cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        express_cost, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertGreater(express_cost, normal_cost)

    def test_express_with_light_package(self):
        """Экспресс для лёгкой посылки."""
        normal_cost, _ = calculate_delivery_cost(0.5, 100, "обычный")
        express_cost, _ = calculate_delivery_cost(0.5, 100, "обычный", is_express=True)
        self.assertGreater(express_cost, normal_cost)

    def test_express_with_fragile_package(self):
        """Экспресс для хрупкой посылки."""
        normal_cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        express_cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий", is_express=True)
        self.assertGreater(express_cost, normal_cost)


class TestDeliveryDates(unittest.TestCase):
    """Расчёт дат доставки."""

    def test_delivery_date_for_short_distance(self):
        """Короткая дистанция (до 500 км) — 1 день доставки."""
        _, date = calculate_delivery_cost(1.0, 300, "обычный")
        self.assertEqual(date, "2026-09-04")

    def test_delivery_date_for_long_distance(self):
        """Дистанция 1000 км — 2 дня доставки."""
        _, date = calculate_delivery_cost(1.0, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")

    def test_delivery_date_for_very_long_distance(self):
        """Дистанция 5000 км — 10 дней доставки."""
        _, date = calculate_delivery_cost(1.0, 5000, "обычный")
        self.assertEqual(date, "2026-09-13")

    def test_express_delivery_date_short_distance(self):
        """Экспресс на короткой дистанции — минимум 1 день."""
        _, date = calculate_delivery_cost(1.0, 300, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-04")

    def test_express_delivery_date_long_distance(self):
        """Экспресс на длинной дистанции — вдвое меньше дней."""
        _, date = calculate_delivery_cost(1.0, 1000, "обычный", is_express=True)
        self.assertEqual(date, "2026-09-05")


class TestDeliveryEdgeCases(unittest.TestCase):
    """Граничные случаи и ошибки."""

    def test_invalid_package_type(self):
        """Недопустимый тип посылки — ошибка."""
        cost, date = calculate_delivery_cost(1.0, 100, "негабаритный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_below_minimum(self):
        """Вес ниже минимального (0.1 кг) — ошибка."""
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_weight_above_maximum(self):
        """Вес выше максимального (50 кг) — ошибка."""
        cost, date = calculate_delivery_cost(60.0, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_below_minimum(self):
        """Дистанция меньше 1 км — ошибка."""
        cost, date = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_distance_above_maximum(self):
        """Дистанция больше 5000 км — ошибка."""
        cost, date = calculate_delivery_cost(1.0, 6000, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_maximum_valid_weight(self):
        """Вес ровно 50 кг — допустим."""
        cost, _ = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertGreater(cost, 0)

    def test_maximum_valid_distance(self):
        """Дистанция ровно 5000 км — допустима."""
        cost, _ = calculate_delivery_cost(1.0, 5000, "обычный")
        self.assertGreater(cost, 0)

    def test_minimum_valid_weight(self):
        """Вес ровно 0.1 кг — допустим."""
        cost, _ = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertGreater(cost, 0)


if __name__ == '__main__':
    unittest.main()
