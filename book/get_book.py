import requests
from bs4 import BeautifulSoup
from .models import Book, Genres
import os


def get_description(url):
    r = requests.get(url)
    book = BeautifulSoup(r.text, 'html.parser')
    description = book.find('div', {'id': 'gioi-thieu'}).text.strip()
    return description


def addbook(item, gen):
    title = item.find('p', {'class': 'title'}).a.text.strip()
    book_url = item.find('p', {'class': 'title'}).a.get('href')
    author = item.find('p', {'class': 'author'}).text.strip()
    price = int(item.find('p', {'class': 'price-sale'})
                .text.strip().split()[0].replace('.', '').replace('đ', ''))
    img_src = item.find('img', {'class': 'img-responsive'}).get('src')
    extend = img_src.split('.')[-1]
    filename = '.'.join([title.replace(' ', '').split('(')[0], extend])
    filepath = os.path.join('/home/nndat/workspaces/python/web/Django/'
                            'bookstore/bookstore/media/bookcovers', filename)
    description = get_description(book_url)
    with open(filepath, 'wb') as f:
        img = requests.get(img_src)
        f.write(img.content)

    book = Book(
        title=title,
        author=author,
        price=price,
        img_cover=filename,
        description=description
    )
    book.save()
    book.genres.set([gen])


def get_books():
    url = 'https://tiki.vn/bestsellers/truyen-cuoi/c444'
    genres = 'Truyện Cười'
    gen = Genres.objects.filter(name=genres)
    if not gen:
        gen = Genres(name=genres)
        gen.save()
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all('div', {'class': 'bestseller-cat-item'})
    for item in items:
        addbook(item, gen)


if __name__ == '__main__':
    get_books()
