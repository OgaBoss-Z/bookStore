
from django.urls import path
from .views import (
   BookDetailView,
   #SearchProduct,
   CartSummaryView,
   #CheckoutView,
   #PaymentView,
   )
from . import views

urlpatterns = [
   path('', views.home, name='home-page'),
   path('<slug>/', BookDetailView.as_view(), name='book-detail'),
   #path('<slug>/', views.detail, name='book-detail'),
   #path('search', SearchProduct.as_view(), name='search-query'),
   path('add-to-cart/<slug>/', views.add_to_cart, name='add-to-cart'),
   path("cart-summary/", CartSummaryView.as_view(), name="cart-summary"),

]
