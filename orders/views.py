from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from orders.models import OrderList, Bill
from orders.untils import update_total


def add_item(request, book_id):
    order_id = request.session.get('order_id')
    if order_id:
        order_list = OrderList.objects.get(id=order_id)
        order_list.add_item(book_id)
    else:
        order_list = OrderList()
        order_list.save()
        request.session['order_id'] = order_list.id
        order_list.add_item(book_id)
    update_total(request)
    return redirect('book-detail', book_id=book_id)


def remove_item(request, book_id):
    order_id = request.session.get('order_id')
    if not order_id:
        messages.info(request, 'Cố lỗi hệ thống, Bạn vui lòng thử lại')
        return redirect('book-detail', book_id=book_id)
    order_list = OrderList.objects.get(id=order_id)
    order_list.remove_item(book_id)
    update_total(request)
    return redirect('show-order')


def show_order(request):
    order_id = request.session.get('order_id')
    if order_id is None:
        order_list = OrderList()
        order_list.save()
    else:
        order_list = OrderList.objects.filter(id=order_id).first()
        if not order_list:
            order_list = OrderList()
            order_list.save()
    if not order_list:
        messages.info(request, 'Bạn chưa có sản phẩm nào trong giỏ')
    order = order_list.items.all()
    total = 0
    for item in order:
        total += item.amount * item.book.price

    return render(request, 'orders/show-order.html',
                  {'order_list': order, 'total': total})


def increase(request, book_id):
    order_id = request.session.get('order_id')
    if not order_id:
        messages.info(request, 'Cố lỗi hệ thống, Bạn vui lòng thử lại')
        return redirect('book-detail', book_id=book_id)
    order = OrderList.objects.filter(id=order_id).first()
    if order:
        order.add_item(book_id)
    update_total(request)
    return redirect('show-order')


def decrease(request, book_id):
    order_id = request.session.get('order_id')
    if not order_id:
        messages.info(request, 'Cố lỗi hệ thống, Bạn vui lòng thử lại')
        return redirect('book-detail', book_id=book_id)
    order = OrderList.objects.filter(id=order_id).first()
    if order:
        order.decrease_item(book_id)
    update_total(request)
    return redirect('show-order')


@login_required
def checkout(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if not (fullname and address and phone):
            messages.info(request, 'Thông tin nhận hàng chưa chính xác. '
                                   'Bạn vui lòng kiểm tra lại')
            return redirect('checkout')
        bill = Bill(
            fullname=fullname,
            address=address,
            phone=phone,
            status='checking',
            user=request.user
        )
        order_id = request.session.get('order_id')
        order_list = OrderList.objects.filter(id=order_id).first()
        order = order_list.items.all()
        total = 0
        for item in order:
            total += item.amount * item.book.price
        bill.total = total
        bill.save()
        for item in order:
            bill.billitem_set.create(
                title=item.book.title,
                price=item.book.price,
                amount=item.amount
            )
            item.delete()
        bill.save()
        messages.success(request, 'Bạn đã đặt hàng thành công')
        update_total(request)
        return redirect('homepage')
    order_id = request.session.get('order_id')
    order_list = OrderList.objects.filter(id=order_id).first()
    order = order_list.items.all()
    total = 0
    if not order:
        messages.info(request, 'Bạn chưa có sản phẩm nào trong giỏ.')
        return redirect('show-order')
    for item in order:
        total += item.amount * item.book.price

    return render(request, 'orders/checkout.html',
                  {'order_list': order, 'total': total})


@login_required
def show_bill(request, bill_id):
    bill = request.user.bill_set.filter(id=bill_id).first()
    context = {
        'bill': bill,
        'code': bill.get_status_display(),
        'books': bill.billitem_set.all()
    }
    return render(request, 'orders/bill.html', context)
