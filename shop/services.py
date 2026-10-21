"""Бизнес-правила корзины. Корзина — словарь {код игры: количество}; хранится в сессии.

Все функции, меняющие корзину, возвращают НОВЫЙ словарь и не трогают старый,
а при ошибке бросают CartError. Поэтому после ошибки прежняя корзина сохраняется.
Цены берутся только из базы данных (каталога), а не из данных формы.
"""
import re

from .models import Game


class CartError(Exception):
    """Понятная пользователю ошибка корзины."""


def get_game(code):
    game = Game.objects.filter(code=str(code).strip()).first()
    if game is None:
        raise CartError("Товар не найден")
    return game


def parse_quantity(raw):
    """Допускаются только целые числа >= 1. Отклоняются: 0, -1, 1.5, пустая строка, текст."""
    text = "" if raw is None else str(raw).strip()
    if not re.fullmatch(r"[0-9]+", text):
        raise CartError("Количество должно быть целым числом (1, 2, 3...).")
    quantity = int(text)
    if quantity < 1:
        raise CartError("Количество должно быть не меньше 1. Для удаления нажмите «Удалить».")
    return quantity


def validate_quantity(raw, stock):
    """Проверка количества: целое число от 1 до доступного остатка."""
    quantity = parse_quantity(raw)
    if quantity > stock:
        raise CartError(f"Доступно только {stock} шт.")
    return quantity


def add_item(cart, code, raw_quantity):
    game = get_game(code)
    if game.stock == 0:
        raise CartError("Нет в наличии")
    quantity = parse_quantity(raw_quantity)
    in_cart = cart.get(game.code, 0)
    if in_cart + quantity > game.stock:
        raise CartError(
            f"Нельзя добавить: доступно {game.stock} шт., в корзине уже {in_cart}."
        )
    new_cart = dict(cart)
    new_cart[game.code] = in_cart + quantity  # одинаковая игра — одна строка
    return new_cart


def set_quantity(cart, code, raw_quantity):
    game = get_game(code)
    if game.code not in cart:
        raise CartError("Этой позиции нет в корзине.")
    quantity = validate_quantity(raw_quantity, game.stock)
    new_cart = dict(cart)
    new_cart[game.code] = quantity
    return new_cart


def remove_item(cart, code):
    code = str(code).strip()
    if code not in cart:
        raise CartError("Этой позиции нет в корзине.")
    return {c: q for c, q in cart.items() if c != code}


def calculate_cart(cart):
    """Серверный расчёт: цена × количество по ценам из каталога, целые тенге."""
    games = Game.objects.in_bulk(list(cart.keys()), field_name="code")
    lines = []
    total = 0
    for code in sorted(cart):
        game = games.get(code)
        if game is None:
            continue
        line_total = game.price * cart[code]
        lines.append({"game": game, "quantity": cart[code], "line_total": line_total})
        total += line_total
    return {"lines": lines, "total": total}
