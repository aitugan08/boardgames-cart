from django.core.management.base import BaseCommand

from shop.catalog import seed_catalog


class Command(BaseCommand):
    help = "Создаёт или восстанавливает учебный каталог из трёх игр (без дублирования)."

    def handle(self, *args, **options):
        seed_catalog()
        self.stdout.write(self.style.SUCCESS("Каталог готов: G01, G02, G03."))
