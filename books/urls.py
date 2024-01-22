from django.urls import path
from . import views

urlpatterns = [
    path( 'add_books/', views.add_books, name='add_books'),
    path('book/<int:id>', views.book, name='book'),
]