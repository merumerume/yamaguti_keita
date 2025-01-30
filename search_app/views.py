from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,  Category, Cart, CartItem, Review# P モデルをインポート 
from .forms import ProductForm, SearchForm, ReviewForm # フォームのインポート
from django.contrib.auth.forms import UserCreationForm  # 正しいインポート
from django.core.paginator import Paginator
#ここから追加したfrom
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from .forms import SignUpForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
#ここで終わり


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all()  # 関連するレビューを取得
    form = None

    # レビューの投稿を処理
    if request.method == "POST" and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product) # product オブジェクトをテンプレートに渡す
    return render(request, 'product_form.html', {'form': form, 'product': product})



def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
        return render(request, 'product_confirm_delete.html', {'product': product})
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})




def search_view(request):
    form = SearchForm(request.GET or None)
    results = Product.objects.all() # クエリセットの初期化 
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = results.filter(name__icontains=query) 
        # カテゴリフィルタリング
    category_name = request.GET.get('category')
    if category_name:
        try:
            # カテゴリ名に基づいてカテゴリ ID を取得
            category = Category.objects.get(name=category_name) 
            results = results.filter(category_id=category.id)
        except Category.DoesNotExist:
            results = results.none() # 存在しないカテゴリの場合、結果を空にする 
            category = None
    # 価格のフィルタリング(最低価格・最高価格) 
    min_price = request.GET.get('min_price') 
    max_price = request.GET.get('max_price')
    if min_price:
        results = results.filter(price__gte=min_price)
    if max_price:
        results = results.filter(price__lte=max_price)
    # 並び替え処理
    sort_by = request.GET.get('sort', 'name') 
    if sort_by == 'price_asc':
        results = results.order_by('price')
    elif sort_by == 'price_desc':
        results = results.order_by('-price')
    # クエリセットをリストに変換せず、直接 Paginator に渡す 
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'search.html', {'form': form, 'page_obj': page_obj, 'results': results})





#追加した関数
@login_required
def home(request):
    return render(request, 'search.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # 新しいユーザーを作成
            login(request, user)  # 作成したユーザーで自動的にログイン
        return redirect('home')  # ログイン後にホーム画面へリダイレクト
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
#レビュー
def review_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    return render(request, 'review_page.html', {'product': product, 'reviews': reviews})
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=product.id)
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'product': product})

def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    messages.success(request, "レビューを削除しました。")
    return redirect('product_detail', product_id=review.product.id)

def cart_view(request):
    # ログイン済みのユーザーのカートを取得または作成
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def logout_view(request):
    logout(request)  # ユーザーをログアウト
    return redirect('home')  # ログアウト後にホーム画面にリダイレクト


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # 画像を受け取る
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})


#カート機能

# **新規追加: カートに商品を追加する**
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # もし新規作成されたら、数量を1に設定
    if created:
        cart_item.quantity = 1
    else:
        # 既存のアイテムなら数量を増やす（10個まで）
        if cart_item.quantity < 10:
            cart_item.quantity += 1
        else:
            messages.error(request, 'この商品の数量は最大10個までです。')

    cart_item.save()
    return redirect('cart_detail')


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)  # カートアイテムをIDで取得
    cart_item.delete()  # カートアイテムを削除
    return redirect('cart_detail')  # カートの詳細ページにリダイレクト


# **新規追加: カートから商品を削除する**
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    return redirect('cart_detail')

# **新規追加: カートの詳細を表示する**
def cart_detail(request):
    cart = Cart.objects.filter(user=request.user).first()
    
    if not cart:
        return render(request, 'cart_empty.html')  # カートが空の場合の処理
    
    # 商品ごとの合計金額とカートの合計金額を計算
    cart_items = cart.items.all()  # `related_name='items'` なので `cart.items.all()` で取得
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    return render(request, 'cart_detail.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price,
    })
    
    # カートの合計金額を計算
    total_price = sum(item.product.price * item.quantity for item in cart.items.all())
    
    return render(request, 'cart_detail.html', {'cart': cart, 'total_price': total_price})