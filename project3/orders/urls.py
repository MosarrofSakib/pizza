from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from . import views
from users import views as users_views

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name = "logout"),
    path('register/', users_views.register_view, name = "register"),
    path('menu/', views.menu, name = "menu"),
    path('cart/<int:id>', views.add_to_cart, name = "add_to_cart")
]
