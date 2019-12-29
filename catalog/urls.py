from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.index, name='catalog_index'),
    path('books/', views.BookListView.as_view(), name='catalog_books'),
    path('book/<int:pk>',  # id_or_pk in case of my own view function i can name it to whatever i want
         views.BookDetailView.as_view(), name='book-detail'),
    #re_path(r'book/(?P<stub>[-\w]+)$', views.BookDetailViewFunc, name='book-detail1'),
    path('authors/', views.AuthorListView.as_view(), name='catalog_authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='user-books'),
    path('borrowed/', views.AllLoanedBooksListView.as_view(), name='all-brrowed')
]
