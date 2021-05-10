from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.index, name='catalog_index'),
    path('books/', views.BookListView.as_view(), name='catalog_books'),
    path('book/<int:pk>/',  # id_or_pk in case of my own view function i can name it to whatever i want
         views.BookDetailView.as_view(), name='book-detail'),
    #re_path(r'book/(?P<stub>[-\w]+)$', views.BookDetailViewFunc, name='book-detail1'),
    path('authors/', views.AuthorListView.as_view(), name='catalog_authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='user-books'),
    path('borrowed/', views.AllLoanedBooksListView.as_view(), name='all-brrowed'),
    #path('404/', views.view_404, name='not_found'),
    # path('book/<uuid:primaryKey>/renew/',
    #     views.renew_book_librarian, name='renew-book-librarian'),
    path('book/<uuid:primaryKey>/renew/',
         views.view_renew_book_ModelForm, name='renew-book-librarian'),
    # generic editing views related to an author
    path('authors/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/',
         views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/',
         views.AuthorDelete.as_view(), name='author_delete'),

    # generic editing views related to a Book
    path('books/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
    path('404/', views.error_404),
    path('500/', views.error_500),
]
