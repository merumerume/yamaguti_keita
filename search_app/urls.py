from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from .views import delete_review,review_page
urlpatterns = [
    # ログインページ
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', views.register, name='register'),  # アカウント登録
    path('logout/', views.logout_view, name='logout'),  # ログアウト
    # アカウント登録ページ
    path('', views.search_view, name='home'),
    path('search/', views.search_view, name='search_view'),
    path('product/new/', views.product_create, name='product_create'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/edit/', views.product_update, name='product_update'),
    path('product/<int:pk>/delete', views.product_delete, name='product_delete'),
    path('product/', views.product_list, name='product_list'),  
    #カートURL
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    #レビュー
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    path('review/delete/<int:review_id>/', delete_review, name='delete_review'),
    path('product/<int:product_id>/reviews/', review_page, name='review_page'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)