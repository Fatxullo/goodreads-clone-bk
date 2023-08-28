from django.contrib import admin
from django.template.defaultfilters import truncatewords
from .models import Book, Author, BookAuthor, BookReview




@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'isbn']
    search_fields = ('title', 'description', 'isbn')



@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email']
    search_fields = ('first_name', 'last_name', 'email')



@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ['book', 'author']
    search_fields = ('book', 'author')



@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'comment', 'stars_given']
    search_fields = ('user', 'book', 'comment')
    list_filter = ('user', 'book', 'stars_given')


