from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate

from orders.models import OrderList
from orders.untils import update_total


def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Bạn đã tạo tài khoản thành công. '
                         'Vui lòng đăng nhập để tiếp tục sử dụng dịch vụ')
        return redirect('login')
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        order_id = request.session.get('order_id')
        if order_id:
            order = OrderList.objects.get(id=order_id)
            if not user.orderlist_set.first():
                order.user = user
                order.save()
                request.session['order_id'] = order.id
            else:
                user.orderlist_set.first().update(order)
                request.session['order_id'] = user.orderlist_set.first().id
        else:
            if not user.orderlist_set.first():
                order = OrderList(user=user)
                order.save()
                request.session['order_id'] = order.id
            else:
                request.session['order_id'] = user.orderlist_set.first().id
        update_total(request)
        messages.success(request, 'Đăng nhập thành công.')
        next = request.GET.get('next')
        return redirect(next) if next else redirect('homepage')
    elif request.method == 'POST':
        messages.warning(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'Bạn đã đăng xuất')
    return redirect('homepage')
