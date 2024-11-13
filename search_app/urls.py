from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    # ログインページ
    path('login/', auth_views.LoginView.as_view(), name='login'),
    # ログアウトページ
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),  
    # アカウント登録ページ
    path('', views.search_view, name='home'),
    path('search/', views.search_view, name='search_view'),
    path('product/new/', views.product_create, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete', views.product_delete, name='product_delete'),
    path('product/', views.product_list, name='product_list'),  
    path('bookmarks/', views.bookmark_list, name='bookmark_list'),
    path('add-bookmark/', views.add_bookmark, name='add_bookmark'),
    path('remove-bookmark/<int:bookmark_id>/', views.remove_bookmark, name='remove_bookmark'),

  ]