from django import forms
from books.models import BookReview, Book



class BookReviewForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)
    
    class Meta:
        model = BookReview
        fields = ('comment', 'stars_given')


class CreateBookForm(forms.ModelForm):
    isbn = forms.CharField(max_length=17)
    
    class Meta:
        model = Book
        fields = ('title', 'description', 'isbn', 'cover_picture')