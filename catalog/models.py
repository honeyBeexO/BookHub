from django.urls import reverse
import uuid
from django.db import models
from django.contrib.auth.models import User

from datetime import date
# Create your models here.


class Genre(models.Model):
    name = models.CharField(
        max_length=100, help_text='Enter a book genre (e.g. Science Fiction)',
        verbose_name='Genre name')

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(
        max_length=50, help_text="Enter the book's natural language(e.g. English, Arabic, Japanese etc.)")

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(
        max_length=150,
        help_text='Enter title',
        blank=False, null=False)
    summary = models.TextField(
        help_text='Enter summary',
        default='summary of the book',
        verbose_name='Summary')
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', null=True, on_delete=models.SET_NULL)
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Character <a href="https: // www.isbn-international.org/content/what-isbn">ISBN number</a>')
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    genre = models.ManyToManyField(Genre)
    language = models.ForeignKey(
        'Language', blank=True, null=True, on_delete=models.SET_NULL)

    # cover = models.ImageField(
    # upload_to=None, height_field=None, width_field=None, max_length=None)

    def get_absolute_url(slef):
        return reverse('book-detail', args=[str(slef.id)])

    def __str__(self):
        return f'{self.title}, {self.author}'
    # Added to work with it on the BookAdmin  ---> model

    def display_genre(self):
        #g = ''
        # for genre in self.genre.all():
            #g.join(genre.name).join(', ')
        return ', '.join(genre.name for genre in self.genre.all()[:3])
        print(g)

    display_genre.short_description = 'Genre'


class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4,
        help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=100)
    due_back = models.DateField('Due back', null=True, blank=True)
    LOAN_STATUS = (
        ('m', 'Maintainance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(
        max_length=1, choices=LOAN_STATUS,
        blank=True, default='m',
        help_text='Book availability'
    )
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ['-due_back']
        permissions = (('can_mark_returned', 'Set Book as returned'),)

    def __str__(self):
        return f' {self.id} ({self.book.title})'


class Author(models.Model):
    first_name = models.CharField('First name', max_length=100)
    last_name = models.CharField(verbose_name="Last name", max_length=100)
    date_of_birth = models.DateField('Birth date', blank=True, null=True)
    date_of_death = models.DateField('Death date', blank=True, null=True)
    #image = models.ImageField(upload_to='/images/authors/', height_field=100, width_field=150, max_length=150)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    def get_absolute_url(self):
        return reverse('author-detail', args=[str(self.id)])
