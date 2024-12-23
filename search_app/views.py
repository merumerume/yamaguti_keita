from django.shortcuts import render, get_object_or_404, redirect
from .models import Product,  Category# P モデルをインポート 
from .forms import ProductForm, SearchForm # フォームのインポート
from django.contrib.auth.forms import UserCreationForm  # 正しいインポート
from django.core.paginator import Paginator
#ここから追加したfrom
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseNotAllowed
from .forms import SignUpForm
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
    return render(request, 'product_detail.html', {'product': product})
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

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # 画像を受け取る
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})
