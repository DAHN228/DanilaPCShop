from cart.forms import CartAddProductForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .filters import ProductFilter
from .models import Product, Type, Review, Backlight, Brand
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import ReviewForm


def marks_filter(request):
    type_slug = request.GET.get('type_slug')
    backlight = request.GET.get('backlight')
    brand = request.GET.get('brand')
    o = request.GET.get('o')
    marks = []

    if type_slug:
        type = get_object_or_404(Type, slug=type_slug)
        products = Product.objects.filter(type=type, backlight=backlight, brand=brand, o=o)
        marks = list(products.values_list('mark', flat=True).distinct())

    return JsonResponse({'marks': marks}, safe=False)

def product_list(request, type_slug=None):
    type = None
    types = Type.objects.all()
    products = Product.objects.filter(available=True)
    if type_slug:
        type = get_object_or_404(Type, slug=type_slug)
        products = products.filter(type=type)

    f = ProductFilter(request.GET, queryset=Product.objects.all())
    has_filter = any(field in request.GET for field in set(f.get_fields()))

    context = {
        'type': type,
        'types': types,
        'products': products,
        'filter': f,
        'has_filter': has_filter
    }

    return render(request,
                  'catalog/product/list.html',
                  context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    context = {
        'product': product,
        'cart_product_form': cart_product_form,
    }

    return render(request, 'catalog/product/detail.html', context)


def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            product_id = form.cleaned_data['product_id']
            text = form.cleaned_data['review_text']

            # Получаем продукт и текущего пользователя
            product = Product.objects.get(id=product_id)
            user = request.user

            # Создаем и сохраняем отзыв
            review = Review.objects.create(product=product, user=user, text=text)

            # Дополнительные действия, если необходимо
            messages.success(request, 'Отзыв успешно добавлен.')
            # Очистка формы
    else:
        messages.error(request, 'Ошибка при добавлении отзыва.')
    return redirect('cart_detail')

