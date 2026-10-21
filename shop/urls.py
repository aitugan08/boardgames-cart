from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cart/add/", views.add, name="add"),
    path("cart/update/", views.update, name="update"),
    path("cart/remove/", views.remove, name="remove"),
]
