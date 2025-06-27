from django.test import TestCase
from django.contrib.auth.models import User
from .models import Faq, History, UploadedFiles

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
        history = History.objects.get(visited='http://testserver')
        self.assertEqual(history.visited_by.username, 'testuser')
        self.assertEqual(history.faq_id.question, 'What is Django?')

class FilesTestCase(TestCase):
    """ Test case for UploadedFiles model"""
    # create user for testing
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        file = UploadedFiles.objects.create(file_path='/static/uploaded/pdf_files/', created_by=user)
    
    def test_uploaded_file_creation(self):
        """Test that a UploadedFiles object can be created and retrieved."""
        file = UploadedFiles.objects.get(file_path='/static/uploaded/pdf_files/')
        self.assertEqual(file.created_by.username, 'testuser')
        