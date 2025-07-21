from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import IntegrityError  # Add this import
from FAQ.models import Faq, History, UploadedFiles
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
import os
import shutil
from django.conf import settings
from FAQ.serializers import UploadedFilesSerializer


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
        expected = "What is Django? - Django is a high-level Python Web framework... (Manual)"
        self.assertEqual(str(self.faq), expected)

    def test_required_fields(self):
        with self.assertRaises(ValidationError):
            faq = Faq.objects.create(author=self.user)
            faq.full_clean()


class HistoryTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.faq = Faq.objects.create(
            author=cls.user,
            question="What is Python?",
            answer="A programming language..."
        )
        cls.history = History.objects.create(
            visited_by=cls.user,
            visited='http://testserver/about/',
            faq_id=cls.faq
        )

    def test_history_creation(self):
        history = History.objects.get(visited='http://testserver/about/')
        self.assertEqual(history.faq_id.question, 'What is Python?')


class FilesTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        test_file = SimpleUploadedFile(
            name='sample.pdf',
            content=b'PDF content',
            content_type='application/pdf'
        )
        cls.file = UploadedFiles.objects.create(
            file_name='sample.pdf',
            file_path=test_file,
            created_by=cls.user
        )

    def test_uploaded_file_creation(self):
        self.assertEqual(self.file.created_by.username, 'testuser')
        self.assertEqual(self.file.file_name, 'sample.pdf')


class UploadedFilesViewSetTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )

        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@test.com',
            password='testpass123'
        )

        self.client = APIClient()
        self.test_file_content = b'This is test file content'
        self.list_url = reverse('uploadedfiles-list')

        # Create test media directory
        self.test_media_dir = os.path.join(settings.BASE_DIR, 'test_media')
        if not os.path.exists(self.test_media_dir):
            os.makedirs(self.test_media_dir)

        # Override media root for tests
        self.original_media_root = settings.MEDIA_ROOT
        settings.MEDIA_ROOT = self.test_media_dir

    def tearDown(self):
        # Clean up test media directory
        if os.path.exists(self.test_media_dir):
            shutil.rmtree(self.test_media_dir)
        # Restore original media root
        settings.MEDIA_ROOT = self.original_media_root

    def test_create_file_success_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)

        test_file = SimpleUploadedFile(
            name='test.txt',
            content=self.test_file_content,
            content_type='text/plain'
        )

        response = self.client.post(
            self.list_url,
            data={'file_path': test_file},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UploadedFiles.objects.count(), 1)

        uploaded_file = UploadedFiles.objects.first()
        self.assertEqual(uploaded_file.file_name, 'test.txt')
        self.assertEqual(uploaded_file.created_by, self.admin_user)

    def test_create_file_no_authentication(self):
        test_file = SimpleUploadedFile(
            name='test.txt',
            content=self.test_file_content,
            content_type='text/plain'
        )

        response = self.client.post(
            self.list_url,
            data={'file_path': test_file},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(UploadedFiles.objects.count(), 0)

    def test_create_file_regular_user_forbidden(self):
        self.client.force_authenticate(user=self.regular_user)

        test_file = SimpleUploadedFile(
            name='test.txt',
            content=self.test_file_content,
            content_type='text/plain'
        )

        response = self.client.post(
            self.list_url,
            data={'file_path': test_file},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(UploadedFiles.objects.count(), 0)

    def test_create_file_no_file_provided(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(
            self.list_url,
            data={},
            format='multipart'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(UploadedFiles.objects.count(), 0)



class UploadedFilesSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

    def test_serializer_create(self):
        test_file = SimpleUploadedFile(
            name='test.txt',
            content=b'Test content',
            content_type='text/plain'
        )

        # Data without required fields that should be set during save
        data = {
            'file_path': test_file,
            'file_name': 'test.txt'
        }

        serializer = UploadedFilesSerializer(data=data)

        # Check if the serializer requires created_by and faqs in data
        if not serializer.is_valid():
            # If created_by is required in serializer validation, include it
            if 'created_by' in serializer.errors:
                data['created_by'] = self.user.id
            # If faqs is required, provide empty list or appropriate value
            if 'faqs' in serializer.errors:
                data['faqs'] = []

            serializer = UploadedFilesSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        # Pass created_by during save if it's not in the data
        if 'created_by' not in data:
            instance = serializer.save(created_by=self.user)
        else:
            instance = serializer.save()

        self.assertEqual(instance.file_name, 'test.txt')
        self.assertEqual(instance.created_by, self.user)


class MockedFileSystemTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        self.client = APIClient()
        self.list_url = reverse('uploadedfiles-list')