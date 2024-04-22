from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from orders.models import Order
from myShop import settings


@shared_task
def order_created(order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Заказ № {order.id}'
        message = f'Уважаемый {order.user.first_name},' \
                  f'Вы успешно сделали заказ в нашем магазине. ' \
                  f'Номер вашего заказа {order.id}.'
        mail_sent = send_mail(subject, message, "nikitanikitka2000@mail.ru", [order.user.email])
        return mail_sent
    except Exception as e:
        print(f"Error in order_created task: {e}")
