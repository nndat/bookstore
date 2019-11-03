from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from .models import Book, Genres, BookReview


BOOK_PER_PAGE = 12


# Create your views here.
def get_genres():
    return Genres.objects.all()


def index(request):
    orders = request.session.get('order_list')
    if orders:
        print('*' * 80)
        print(orders)

    all_books = Book.objects.all()
    paginator = Paginator(all_books, BOOK_PER_PAGE)
    page = request.GET.get('page')
    books = paginator.get_page(page)
    context = {
        'books': books,
        'genres': get_genres(),
        'page_range': paginator.page_range
    }
    return render(request, 'index.html', context)


def detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    reviews = book.bookreview_set.all()
    rating = reviews.aggregate(Avg('rating'))
    context = {
        'book': book,
        'genres': get_genres(),
        'reviews': reviews,
        'rating': rating['rating__avg']
    }
    return render(request, 'detail.html', context)


def genres(request, gen):
    books = Genres.objects.filter(name__exact=gen).first()
    if books:
        books = books.book_set.all()
    paginator = Paginator(books, BOOK_PER_PAGE)
    page = request.GET.get('page')
    context = {
        'books': paginator.get_page(page),
        'genres': get_genres(),
        'page_range': paginator.page_range
    }
    return render(request, 'index.html', context)


def search(request):
    q = request.GET["q"]
    books = Book.objects.filter(Q(title__icontains=q) |
                                Q(author__icontains=q)).all()
    if not books:
        messages.info(request, f'Không tìm thấy sách: {q}.'
                      ' Bạn vui lòng thử lại.')
    context = {
        'books': books,
        'genres': get_genres()
    }
    return render(request, 'index.html', context)


@login_required
def reviewbook(request, book_id):
    if request.method == 'POST':
        rating = int(request.POST.get('rating')) % 5
        rating = rating if rating > 0 else 5
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        book = Book.objects.get(id=book_id)
        if not book:
            messages.warning(request, 'Không thể nhận xét cho sách này')
            return redirect('book-detail', book_id=book.id)
        if BookReview.objects.filter(Q(user=request.user) &
                                     Q(book=book)).all():
            messages.info(request, 'Bạn đã có nhận xét cho sách này')
            return redirect('book-detail', book_id=book.id)
        reviews = BookReview(
            rating=rating,
            book=book,
            user=request.user,
            title=title,
            comment=comment
        )
        reviews.save()
        messages.success(request, 'Cảm ơn nhận xét của bạn về cuốn sách:'
                         ' {}'.format(book.title))
    return redirect('book-detail', book_id=book_id)
