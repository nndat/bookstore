from django.db import models
from book.models import Book
from django.contrib.auth.models import User


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
