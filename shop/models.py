from django.db import models


class Game(models.Model):
    """Учебная настольная игра. Цена — целые тенге, stock — верхняя граница позиции в корзине."""
    code = models.CharField("Код", max_length=10, unique=True)
    title = models.CharField("Название", max_length=100)
    price = models.PositiveIntegerField("Цена, тенге")
    stock = models.PositiveIntegerField("Доступно")

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} {self.title}"
