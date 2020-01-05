from django.urls import reverse_lazy
from catalog.models import Author
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from catalog.forms import renew_book_ModelForm
from django.utils.translation import ugettext_lazy as _
from catalog.forms import RenewBookForm
import datetime
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404   # for the form handling
from django.http import HttpResponseRedirect    # for the form handling
from django.urls import reverse                 # for the form handling

# to make the view available for the only logged in users
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic
from django.shortcuts import render
from django.http import HttpResponse

from . models import Book, BookInstance, Author, Genre
# Create your views here.


def index(request):
    num_of_books = Book.objects.all().count()
    num_of_instances = BookInstance.objects.all().count()

    # available instances status== 'a'
    num_of_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    # number of authors
    num_of_authors = Author.objects.all().count()

    # number of geners:
    num_of_genres = Genre.objects.all().count()
    # number of books containing: word
    word = 'The'
    num_of_books_contains_w = Book.objects.filter(
        title__icontains=word).count()
    # toturial 7: sessions
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_books': num_of_books,
        'num_instances': num_of_instances,
        'num_instances_available': num_of_instances_available,
        'num_authors': num_of_authors,
        'num_genre': num_of_genres,
        'num_contains': num_of_books_contains_w,
        'word': word,
        'title': 'bookHub',
        # session calculation
        'num_visits': num_visits,
        'home_page': 'active',
    }
    return render(request, 'catalog/index.html', context=context)


# instead of going like this :
# def BookListView(request):
#          return HttpResponse('<h1> Bookss list </h1>')
# ===> we can use django generic class views


class BookListView(generic.ListView):
    model = Book
    paginate_by = 6
    # i can access this inside the template
    context_object_name = 'list_of_all_books'
    num = 0  # Book.objects.filter(title__icontains='t')[:5].count()
    template_name = 'top_5_books/book_list.html'

    def get_queryset(self):
        queryset = Book.objects.all()
        self.num = queryset.count()
        return queryset

    def get_context_data(self, **kwargs):
          # call the base implementation to first get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # add data to the context
        context['title'] = 'All Books -from get_context-'
        context['num_books'] = self.num
        context['books_page'] = 'active'
        return context


# stub = r'book/(?P<stub>[-\w]+)$'
# stub = r'book/(?P<stub>[-\w]+)-[\d]+$'  --> all year books
# stub = r'book/(?P<stub>[-\w]+)(-)[\d]+(-)(\d\d)$'  --> all mounth books
# stub = r'book/(?P<stub>[-\w]+)(-)[\d]+(-)(\d\d)(-)(\d\d)$'  --> all day books


class BookDetailView(generic.DetailView):
    model = Book
    context_object_name = 'detail_of_book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Book's Details"
        # context["instances"] = BookInstance.objects.filter(book__id__in=[1, 2, 3, 4, 5, 6])
        return context


"""def BookDetailViewFunc(request, primarykey):
    try:
        book = Book.objects.get(pk=primarykey)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')
    return render(request, 'catalog/book_detail.html', {'title': 'detail function', 'book_detail': book})

    from django.shortcuts import get_object_or_404
def book_detail_view(request, primary_key):
    book = get_object_or_404(Book, pk=primary_key)
    return render(request, 'catalog/book_detail.html', context={'book': book})
"""


class AuthorListView(generic.ListView):
    paginated_by = 5
    model = Author
    num_auth = 0

    context_object_name = 'list_all_authors'
    template_name = 'all_authors/author_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Authors'
        context['num_auth'] = self.num_auth
        context["authors_page"] = "active"
        # context['data'] = self.model.objects.all()
        return context

    def get_queryset(self):
        queryset = Author.objects.all()
        self.num_auth = queryset.count()
        return queryset


class AuthorDetailView(generic.DetailView):
    model = Author
    context_object_name = 'detail_of_author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Author's Details"
        return context


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    paginated_by = 5
    context_object_name = 'loanedBooks'
    template_name = 'catalog/bookinstance_list_borrowed_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Loaned Books'
        context['user_books'] = 'active'
        return context

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class AllLoanedBooksListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = 6
    context_object_name = 'allBooksOnLoan'
    template_name = 'catalog/bookinstance_list_borrowed_all_users.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Loaned Books'
        context['all_users_books'] = 'active'
        return context

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


"""
@permission_required('catalog.can_mark_returned')
@permission_required('catalog.can_edit')
def renew_book_librarian(request, primaryKey):
    book_instance = get_object_or_404(BookInstance, pk=primaryKey)
    print(book_instance)
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-brrowed'))
        else:
            return render(request, 'catalog/book_renew_librarian.html', {'form': form})

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

        context = {
            'form': form,
            'book_instance': book_instance,
            'all_users_books': 'active',
        }

        return render(request, 'catalog/book_renew_librarian.html', context)

"""


@permission_required('catalog.can_mark_returned')
@permission_required('catalog.can_edit')
def view_renew_book_ModelForm(request, primaryKey):
    book_instance = get_object_or_404(BookInstance, pk=primaryKey)
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = renew_book_ModelForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-brrowed'))
        else:
            return render(request, 'catalog/book_renew_librarian.html', {'form': form})

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = renew_book_ModelForm(
            initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
        'all_users_books': 'active',
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


# Generic editing views related to a model
class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {
        'date_of_death': '05/01/2018'
    }


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('catalog_authors')


def view_404(request, exception=None):
    return HttpResponseNotFound()
