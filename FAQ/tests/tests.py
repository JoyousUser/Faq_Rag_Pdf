from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from FAQ.models import Faq, History, UploadedFiles


class FaqTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        cls.faq = Faq.objects.create(
            author=cls.user,
            question="What is Django?",
            answer="Django is a high-level Python Web framework..."
        )

    def test_faq_creation(self):
        self.assertEqual(self.faq.answer, "Django is a high-level Python Web framework...")
        self.assertEqual(self.faq.author.username, 'testuser')

    def test_str_representation(self):
        expected = "What is Django? - Django is a high-level Python Web framework... (AI)"
        self.assertEqual(str(self.faq), expected)

    def test_required_fields(self):
        with self.assertRaises(ValidationError):
            faq = Faq.objects.create(author=self.user)
            faq.full_clean()


class HistoryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        cls.faq = Faq.objects.create(
            author=cls.user,
            question="What is Python?",
            answer="A programming language..."
        )
        cls.history = History.objects.create(
            visited_by=cls.user,
            visited='http://testserver/about/',
            faq_id=cls.faq  # Use faq_id instead of faq
        )

    def test_history_creation(self):
        self.assertEqual(self.history.visited_by.username, 'testuser')
        self.assertEqual(self.history.faq.question, 'What is Python?')

    def test_faq_cascade_delete(self):
        self.faq.delete()
        with self.assertRaises(History.DoesNotExist):
            History.objects.get(id=self.history.id)


class FilesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        cls.file = UploadedFiles.objects.create(
            file_path='/static/uploaded/pdf_files/sample.pdf',
            created_by=cls.user
        )

    def test_uploaded_file_creation(self):
        self.assertEqual(self.file.created_by.username, 'testuser')
        self.assertEqual(self.file.file_path, '/static/uploaded/pdf_files/sample.pdf')

    def test_file_path_unique(self):
        with self.assertRaises(ValidationError):
            duplicate = UploadedFiles(
                file_path='/static/uploaded/pdf_files/sample.pdf',
                created_by=self.user
            )
            duplicate.full_clean()