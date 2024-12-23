from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    # ログインページ
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='register.html'), name='logout'), 
    path('register/', views.register, name='register'),  
    # アカウント登録ページ
    path('', views.search_view, name='home'),
    path('search/', views.search_view, name='search_view'),
    path('product/new/', views.product_create, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete', views.product_delete, name='product_delete'),
    path('product/', views.product_list, name='product_list'),  

  ]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)