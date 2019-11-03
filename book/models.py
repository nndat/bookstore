from django.db import models
from django.contrib.auth.models import User


class Genres(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    img_cover = models.ImageField(default='bookcover.jpg',
                                  upload_to='bookcovers')
    genres = models.ManyToManyField(Genres)
    amount = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.IntegerField()
    title = models.CharField(max_length=100, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.rating} - {self.title}'
