from django.test import TestCase
from django.contrib.auth.models import User
from .models import Faq

# Create your tests here.
class FaqTestCase(TestCase):
    """Test case for the Faq model."""
    # create user for testing

    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        Faq.objects.create(author=user, question="What is Django?", answer="Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.")
        # user.delete()

    def test_faq_creation(self):
        """Test that a Faq object can be created and retrieved."""
        faq = Faq.objects.get(question="What is Django?")
        self.assertEqual(faq.answer, "Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.")
