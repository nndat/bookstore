from django.db.models import Sum
from .models import OrderList


def update_total(request):
    order_id = request.session.get('order_id')
    if order_id:
        order = OrderList.objects.filter(id=order_id).first()
        request.session['total'] = order.items.all().aggregate(
                                    Sum('amount'))['amount__sum']
