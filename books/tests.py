from django.test import TestCase
from django.urls import reverse
from books.models import Book, Author, BookAuthor
from users.models import CustomUser




class BooksTestCase(TestCase):
    
    def test_no_boosk(self):
        response = self.client.get(reverse("books:list"))
        self.assertContains(response, 'No books found.')
    
    
    
    def test_books_list(self):
        book1 = Book.objects.create(title="first book", description="cmsdmcsmms")
        book2 = Book.objects.create(title="second book", description="dndnvjdnvjds")
        book3 = Book.objects.create(title="third book", description="mdksnfndsfjndnf")
        
        response = self.client.get(reverse("books:list"))
        
        for book in [book1, book2]:
            self.assertContains(response, book.title)

        response = self.client.get(reverse("books:list") + "?page=2")
        
        self.assertContains(response, book3.title)
    
    
    def test_detail_page(self):
        book = Book.objects.create(title="first book", description="cmsdmcsmms")
        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))
        
        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
    
    
    
    def test_search_book(self):
        book1 = Book.objects.create(title="Sport", description="cmsdmcsmms", isbn="12345")
        book2 = Book.objects.create(title="Travel", description="dndnvjdnvjds", isbn="123456")
        book3 = Book.objects.create(title="Judo", description="mdksnfndsfjndnf", isbn="123457")
        
        response = self.client.get(reverse('books:list') + "?q=travel")
        
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)






class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="first book", description="this is very good book")
        user = CustomUser.objects.create(username='fathullo', first_name='fathullo', last_name='zayniddinov', email='fathullo@gamil.com')
        user.set_password('somepass')
        user.save()
        self.client.login(username='fathullo', password='somepass')
        
        self.client.post(reverse('books:reviews', kwargs={'id': book.id}), data={
            "stars_given": 3,
            "comment": 'nice book'
        })
        
        book_reviews = book.bookreview_set.all()
        
        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, 'nice book')
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)




class BookAuthorTestCase(TestCase):
    def test_book_author(self):
        book = Book.objects.create(title="first book", description="this is very good book")
        author = Author.objects.create(first_name='test', last_name='testlast', bio='one two')
        book_author = BookAuthor.objects.create(book=book, author=author)
        
        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))
        
        self.assertContains(response, book.title)
        self.assertContains(response, author.first_name)
        self.assertContains(response, author.last_name)
        self.assertContains(response, book_author.book)
        