from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from . import services
from .models import Game
from .services import CartError


def _get_cart(request):
    cart = request.session.get("cart", {})
    return cart if isinstance(cart, dict) else {}


def _apply(request, action, success_message):
    """Применяет действие к корзине. При ошибке корзина в сессии остаётся прежней."""
    try:
        request.session["cart"] = action(_get_cart(request))
        messages.success(request, success_message)
    except CartError as error:
        messages.error(request, str(error))
    return redirect("index")


def index(request):
    summary = services.calculate_cart(_get_cart(request))
    return render(request, "shop/index.html", {"games": Game.objects.all(), "cart": summary})


@require_POST
def add(request):
    code, qty = request.POST.get("code", ""), request.POST.get("quantity")
    # request.POST["price"] намеренно не используется: цена берётся только из каталога
    return _apply(request, lambda cart: services.add_item(cart, code, qty), "Игра добавлена в корзину.")


@require_POST
def update(request):
    code, qty = request.POST.get("code", ""), request.POST.get("quantity")
    return _apply(request, lambda cart: services.set_quantity(cart, code, qty), "Количество изменено.")


@require_POST
def remove(request):
    code = request.POST.get("code", "")
    return _apply(request, lambda cart: services.remove_item(cart, code), "Позиция удалена.")
