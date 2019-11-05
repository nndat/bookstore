from django.db import models
from book.models import Book
from django.contrib.auth.models import User

from datetime import datetime
import secrets


ORDER_STATUS = [
    ('checking', 'Đang kiểm tra'),
    ('shipping', 'Đang giao hàng'),
    ('finished', 'Giao hàng thành công'),
]


class Item(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.book.title} - amount: {self.amount}"


class OrderList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             blank=True, null=True)
    items = models.ManyToManyField(Item)

    def add_item(self, book_id):
        book = Book.objects.filter(id=book_id).first()
        item = self.items.filter(book=book).first()
        if item:
            print(item)
            item.amount += 1
            item.save()
        else:
            item = Item(book=book)
            item.save()
            self.items.add(item)

    def decrease_item(self, book_id):
        book = Book.objects.filter(id=book_id).first()
        item = self.items.filter(book=book).first()
        if item:
            item.amount = item.amount - 1 if item.amount > 1 else 1
            item.save()

    def update(self, order):
        for item in order.items.all():
            book = self.items.filter(book=item.book).first()
            if book:
                book.amount += item.amount
                book.save()
            else:
                self.items.add(item)
        self.save()
        order.delete()

    def remove_item(self, book_id):
        book = Book.objects.filter(id=book_id).first()
        item = self.items.filter(book=book).first()
        if item:
            item.delete()


class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    total = models.IntegerField(default=0)
    date = models.DateTimeField(default=datetime.now, blank=True)
    status = models.CharField(choices=ORDER_STATUS,
                              max_length=10, default='checking')
    code = models.CharField(default=secrets.token_urlsafe(12), max_length=20)


class BillItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField()
    amount = models.IntegerField()
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
