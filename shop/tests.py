"""Четыре автоматические проверки бизнес-правил корзины.

В каждом тесте: подготовка данных (Arrange) -> действие (Act) -> сравнение результата (Assert).
Данные — фиксированный учебный каталог G01/G02/G03 (shop/catalog.py).
"""
from django.test import TestCase

from .catalog import seed_catalog
from .services import CartError, add_item, calculate_cart


class CartRulesTests(TestCase):
    def setUp(self):
        seed_catalog()  # G01 4500/3, G02 7200/2, G03 3000/0

    def test_total_for_regular_cart(self):
        # Arrange
        cart = {"G01": 2, "G02": 1}
        # Act
        result = calculate_cart(cart)
        # Assert
        self.assertEqual(result["total"], 16200)

    def test_empty_cart_total_is_zero(self):
        # Arrange
        cart = {}
        # Act
        result = calculate_cart(cart)
        # Assert
        self.assertEqual(result["total"], 0)

    def test_quantity_above_stock_is_rejected(self):
        # Arrange: на складе доступно 3 шт. G01
        cart = {}
        # Act + Assert: 4 шт. отклоняются целиком
        with self.assertRaises(CartError):
            add_item(cart, "G01", "4")
        self.assertEqual(cart, {})

    def test_unknown_product_is_rejected(self):
        # Arrange
        cart = {}
        # Act + Assert
        with self.assertRaises(CartError) as ctx:
            add_item(cart, "G99", "1")
        self.assertEqual(str(ctx.exception), "Товар не найден")
