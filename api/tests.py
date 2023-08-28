from rest_framework.test import APITestCase
from rest_framework.reverse import reverse

from books.models import Book, BookReview
from users.models import CustomUser




class BookReviewAPITestCse(APITestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create(username='fathullo', first_name='fathullo')
        self.user.set_password('somepass')
        self.user.save()
        self.client.login(username='fathullo', password='somepass')
    
    
    
    def test_book_review_detail(self):
        book = Book.objects.create(title="first book", description="not bad", isbn='123121')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='good book')
        
        response = self.client.get(reverse('api:review-detail', kwargs={'id': book_review.id}))
        
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], book_review.id)
        self.assertEqual(response.data['stars_given'], 5)
        self.assertEqual(response.data['comment'], 'good book')
        
        self.assertEqual(response.data['book']['id'], book_review.id)
        self.assertEqual(response.data['book']['title'], 'first book')
        self.assertEqual(response.data['book']['description'], 'not bad')
        self.assertEqual(response.data['book']['isbn'], '123121')
        
        self.assertEqual(response.data['user']['id'], self.user.id)
        self.assertEqual(response.data['user']['first_name'], 'fathullo')
        self.assertEqual(response.data['user']['username'], 'fathullo')


    
    
    
    def test_book_reviews_list(self):
        user_two = CustomUser.objects.create(username='user2', first_name='user2')
        book = Book.objects.create(title="second book", description="fant book", isbn='123121')
        br1 = BookReview.objects.create(book=book, user=self.user, stars_given=2, comment='good book')
        br2 = BookReview.objects.create(book=book, user=user_two, stars_given=3, comment='bad book')
        
        response = self.client.get(reverse('api:review-list'))
        
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['count'], 2)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        
        
        self.assertEqual(response.data['results'][1]['id'], br1.id)
        self.assertEqual(response.data['results'][1]['stars_given'], br1.stars_given)
        self.assertEqual(response.data['results'][1]['comment'], br1.comment)
        
        self.assertEqual(response.data['results'][0]['id'], br2.id)
        self.assertEqual(response.data['results'][0]['stars_given'], br2.stars_given)
        self.assertEqual(response.data['results'][0]['comment'], br2.comment)
    
    
    
    
    def test_review_delete(self):
        book = Book.objects.create(title="first book", description="not bad", isbn='123121')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='good book')
        
        response = self.client.delete(reverse('api:review-detail', kwargs={'id': book_review.id}))
        
        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=book_review.id).exists())
    
    
    
    def test_review_patch(self):
        book = Book.objects.create(title="first book", description="not bad", isbn='123121')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='good book')
        
        response = self.client.patch(reverse('api:review-detail', kwargs={'id': book_review.id}), data={'stars_given': 1})
        book_review.refresh_from_db()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.stars_given, 1)
    
    
    
    def test_review_put(self):
        book = Book.objects.create(title="first book", description="not bad", isbn='123121')
        book_review = BookReview.objects.create(book=book, user=self.user, stars_given=5, comment='good book')

        response = self.client.put(reverse('api:review-detail', kwargs={'id': book_review.id}), data={ 'stars_given': 3, 'comment': 'lol book', 'user_id': self.user.id, 'book_id': book.id })
        book_review.refresh_from_db()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(book_review.stars_given, 3)
        self.assertEqual(book_review.comment, 'lol book')
    
    
    
    def test_review_post(self):
        book = Book.objects.create(title="first book", description="not bad", isbn='123121')
        
        data = {
            'stars_given': 1,
            'comment': 'bad book',
            'user_id': self.user.id,
            'book_id': book.id
        }
        response = self.client.post(reverse('api:review-list'), data=data)
        book_review = BookReview.objects.get(book=book)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(book_review.stars_given, 1)
        self.assertEqual(book_review.comment, 'bad book')
        self.assertEqual(book_review.user_id, self.user.id)
        
    
    
    
    def test_review_bad_request(self):
        book = Book.objects.create(title="first book", description="not bad", isbn='123121')
        
        data = {
            'stars_given': 4,
            'comment': 'bad book',
            'user_id': self.user.id,
            'book_id': ''
        }
        response = self.client.post(reverse('api:review-list'), data=data)
        
        