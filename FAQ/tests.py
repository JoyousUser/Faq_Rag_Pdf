from django.test import TestCase
from django.contrib.auth.models import User
from .models import Faq, History

# Create your tests here.
class FaqTestCase(TestCase):
    """Test case for the Faq model."""
    # create user for testing

    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        Faq.objects.create(author=user, question="What is Django?", answer="Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.")

    def test_faq_creation(self):
        """Test that a Faq object can be created and retrieved."""
        print('FAQ Creation')
        faq = Faq.objects.get(question="What is Django?")
        self.assertEqual(faq.answer, "Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.")


class HistoryTestCase(TestCase):
    """Test case for the History model."""
    # create user for testing
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        faq = Faq.objects.create(author=user, question="What is Django?", answer="Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.")
        history = History.objects.create(visited_by=user, visited='http://testserver', faq_id=faq)

    def test_history_creation(self):
        """Test that a History object can be created and retrieved."""
        print('History Creation')
        history = History.objects.get(visited='http://testserver')
        self.assertEqual(history.visited_by.username, 'testuser')
        self.assertEqual(history.faq_id.question, 'What is Django?')
    
class UploadedFilesTestCase(TestCase):
    """Test case for the UploadedFiles model."""
    pass

class VisitLogTestCase(TestCase):
    """Test case for the VisitLog model."""
    pass