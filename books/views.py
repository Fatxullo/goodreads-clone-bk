from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from books.models import Book, BookReview
from books.forms import BookReviewForm, CreateBookForm




# class BookView(ListView):
#     template_name = 'books/list.html'
#     queryset = Book.objects.all()
#     context_object_name = "books"
#     paginate_by = 2


class BookView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)
        
        page_size = request.GET.get('page_size', 6)
        paginator = Paginator(books, page_size)
        
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)
        
        
        return render(request, 'books/list.html', {"page_obj": page_obj, "search_query": search_query})







# class BookDetailView(DetailView):
#     template_name = 'books/book_detail.html'
#     pk_url_kwarg = 'id'
#     model = Book
#     context_object_name = 'book'
    


class BookDetailView(View):
    def get(self, request, id): 
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()
        
        
        return render(request, "books/book_detail.html", {"book": book, "review_form": review_form})




class AddBookReview(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)
        
        if review_form.is_valid():
            BookReview.objects.create(
                book = book,
                user = request.user,
                stars_given = review_form.cleaned_data['stars_given'],
                comment = review_form.cleaned_data['comment']
            )
            
            return redirect(reverse('books:detail', kwargs={"id":book.id}))
        
        return render(request, 'books/book_detail.html', {"book":book, "review_form":review_form})







# edit review class
class EditReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review)
        
        return render(request, 'books/edit_review.html', {'book':book, 'review':review, 'review_form':review_form})
    
    
    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = BookReviewForm(instance=review, data=request.POST)
        
        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('books:detail', kwargs={"id":book.id}))
        
        return render(request, 'books/edit_review.html', {'book':book, 'review':review, 'review_form':review_form})





class ConfirmDeleteReview(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        return render(request, 'books/confirm_delete_review.html', {'book':book, 'review':review})





class DeleteReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        
        review.delete()
        messages .success(request, 'You have successfly deleted this review')
        return redirect(reverse('books:detail', kwargs={"id":book.id}))








class CreateBookView(View):
    
    def get(self, request):
        create_book_form = CreateBookForm()
        
        return render(request, 'books/create_book.html', {'create_book': create_book_form})
    
    
    
    def post(self, request):
        create_book_form = CreateBookForm(data=request.POST, files=request.FILES)
        
        if create_book_form.is_valid():
            create_book_form.save()
            messages.success(request, "You have successfully created book.")
            return redirect('books:list')

        return render(request, 'books/create_book.html', {'create_book': create_book_form})
            
