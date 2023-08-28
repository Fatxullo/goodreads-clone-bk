from django.urls import path
from books.views import BookView, BookDetailView, AddBookReview, EditReviewView, ConfirmDeleteReview, DeleteReviewView, CreateBookView


app_name = "books"
urlpatterns = [
    path("", BookView.as_view(), name='list'),
    path('create-book/', CreateBookView.as_view(), name='create-book'),
    path("<int:id>/", BookDetailView.as_view(), name="detail"),
    path("<int:id>/reviews/", AddBookReview.as_view(), name='reviews'),
    path("<int:book_id>/review/<int:review_id>/edit/", EditReviewView.as_view(), name='edit-review'),
    path("<int:book_id>/review/<int:review_id>/delete/confirm/", ConfirmDeleteReview.as_view(), name='confirm-delete-review'),
    path("<int:book_id>/review/<int:review_id>/delete/", DeleteReviewView.as_view(), name='delete-review'),
]
