from django.shortcuts import render

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

# from catalog.forms import ReviewForm
from django.urls import reverse
from django.shortcuts import render, redirect
from catalog.models import Product

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST,
                               initial={'city': request.user.profile.city,
                                        'address': request.user.profile.address})
        if form.is_valid():
            order = form.save(commit=False)
            if cart.promocode:
                order.promocode = cart.promocode
                order.discount = cart.promocode.discount
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            # # запуск асинхронной задачи
            # order_created.delay(order.id)
            # return render(request, 'orders/order/created.html',
            #               {'order': order})
            # запустить асинхронное задание
            order_created.delay(order.id)
            # задать заказ в сеансе
            request.session['order_id'] = order.id
            # перенаправить к платежу
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm(initial={'city': request.user.profile.city,
                                        'address': request.user.profile.address})
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})

# def order_detail(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     products = order.products.all()
#     if request.method == 'POST':
#         review_form = ReviewForm(request.POST)
#         if review_form.is_valid():
#             # Сохранение отзыва в базе данных
#             review = review_form.save(commit=False)
#             review.product = products.first()  # Привязка отзыва к первому товару в заказе
#             review.user = request.user
#             review.save()
#     else:
#         review_form = ReviewForm()
#
#     return render(request, 'orders/order_detail.html', {'order': order, 'products': products, 'review_form': review_form})