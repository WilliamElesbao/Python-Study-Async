from django.shortcuts import render, redirect
from .models import Book, ViewBook, Tags
from django.contrib.messages import constants
from django.contrib import messages


def add_books(request):
    if request.method == 'GET':
        books = Book.objects.filter(user=request.user)
        total_views = ViewBook.objects.filter(book__user=request.user).count()

        return render(request, 'add_books.html', {'books': books, 'total_views': total_views})
    elif request.method == 'POST':
        title = request.POST.get('title')
        tags = request.POST.get('tags')
        file = request.FILES.get('file')

        # Verifica se os campos obrigatórios foram preenchidos
        if not title or not tags or not file:
            messages.add_message(request, constants.ERROR, 'Please fill in all the required fields.')
            return redirect('/books/add_books')

        book = Book(
            user=request.user,
            title=title,
            file=file,
        )

        # Verifica se o arquivo é um PDF (exemplo, ajuste conforme necessário)
        if not file.name.endswith('.pdf'):
            messages.add_message(request, constants.ERROR, 'Please upload a valid PDF file.')
            return redirect('/books/add_books')

        book.save()

        list_tags = tags.split(',')

        for tag in list_tags:
            new_tag = Tags(
                name=tag
            )
            new_tag.save()
            book.tags.add(new_tag)

        book.save()

        messages.add_message(request, constants.SUCCESS, 'Saved successfully!')
        return redirect('/books/add_books')
    

def book(request, id):
    book = Book.objects.get(id=id)
    total_views = ViewBook.objects.filter(book=book).count()
    unique_views = ViewBook.objects.filter(book=book).values('ip').distinct().count()
    print(unique_views)

    view = ViewBook(
        ip = request.META['REMOTE_ADDR'],
        book = book,
    )
    view.save()
    return render(request, 'book.html', {'book':book, 'total_views':total_views, 'unique_views':unique_views})