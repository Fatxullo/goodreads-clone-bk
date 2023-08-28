from django.test import TestCase
from django.urls import reverse
from books.models import Book, BookReview
from users.models import CustomUser



class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title="first book", description="this is very good book")
        user = CustomUser.objects.create(username='fathullo', first_name='fathullo', last_name='zayniddinov', email='fathullo@gamil.com')
        user.set_password('somepass')
        user.save()
        
        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment='very good book')
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment='very bad book')
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment='very cute book')
        
        
        response = self.client.get(reverse('home_page') + '?page_size=2')
        
        self.assertContains(response, review2.comment)
        self.assertContains(response, review3.comment)
        self.assertNotContains(response, review1.comment)