"""Учебный каталог. ЗДЕСЬ меняются игры, цены и остатки (вымышленные товары)."""
from .models import Game

CATALOG = [
    # (код, название, цена в целых тенге, доступное количество)
    ("G01", "Космический маршрут", 4500, 3),
    ("G02", "Город мастеров", 7200, 2),
    ("G03", "Лесные тропы", 3000, 0),
]


def seed_catalog():
    """Идемпотентно создаёт/восстанавливает каталог: повторный вызов не создаёт дублей."""
    for code, title, price, stock in CATALOG:
        Game.objects.update_or_create(
            code=code, defaults={"title": title, "price": price, "stock": stock}
        )
