from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path,include
from . import views
from django.conf.urls import url
from django.conf.urls import handler404

app_name = 'cart'

urlpatterns = [
    path('', views.HomeView.as_view(), name='MyView'),
    path('checkout/',views.checkout.as_view(),name="checkout"),
    path('payment/',views.payment.as_view(),name="payment"),
    path('product/<slug>/',views.ItemDetailView.as_view(), name='product'),
    path('cart_add_item/<slug>', views.cart_add_item, name='cart_add_item'),
    path('home_add_item/<slug>', views.home_add_item, name='home_add_item'),
    path('add_qty/<slug>', views.add_qty, name='add_qty'),
    path('delete_item/<slug>/', views.delete_item, name='delete_item'),
    path('remove_qty/<slug>/', views.remove_qty, name='remove_qty'),
    path('order-details/', views.OrderSummary.as_view(), name='order-details'),
    path('<slug:category_slug>/',views.categories, name="categories"),
    path('brands/<brand_slug>/',views.brands, name="brands"),
    path('filter-data', views.filter_data, name='filter_data'),
    # path('paginator', views.paginator, name='paginator'),
    path('wish_list/<int:id>', views.wish_list, name="wish_list"),
    path('verification/', include('verify_email.urls')),
    path('search',views.search, name="search"),
    path('review/<int:id>', views.review, name='review'),
   
   ]




