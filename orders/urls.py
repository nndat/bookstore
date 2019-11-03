from django.urls import path

from . import views


urlpatterns = [
    path('add-item-to-cart/<int:book_id>', views.add_item, name="add-item"),
    path('remove-item-to-cart/<int:book_id>', views.remove_item, name="remove-item"),
    path('remove-item-to-cart/<int:book_id>', views.remove_item, name="remove-item"),
    path('show-order', views.show_order, name="show-order"),
    path('increase-item/<int:book_id>', views.increase, name="increase-item"),
    path('decrease-item/<int:book_id>', views.decrease, name="decrease-item"),
    path('checkout/', views.checkout, name="checkout"),
]
