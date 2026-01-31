from django.test import TestCase
from django.urls import reverse

from .models import Sample


class SampleTests(TestCase):
    def setUp(self):
        self.sample1 = Sample.objects.create(name="テスト1")
        self.sample2 = Sample.objects.create(name="テスト2")

    def test_sample_model(self):
        self.assertEqual(Sample.objects.count(), 2)
        sample = Sample.objects.get(name="テスト1")
        self.assertEqual(sample.name, "テスト1")

    def test_urls(self):
        response = self.client.get("/exe05/samples/")
        self.assertEqual(response.status_code, 200)

    def test_sample_list_view(self):
        response = self.client.get(reverse("sample_list"))
        self.assertEqual(response.status_code, 200)

    def test_sample_detail_view(self):
        response = self.client.get(reverse("sample_detail", args=[self.sample1.id]))
        self.assertEqual(response.status_code, 200)

    def test_sample_create_view(self):
        data = {"name": "新しいテスト"}
        self.client.post(reverse("sample_create"), data)
        self.assertTrue(Sample.objects.filter(name="新しいテスト").exists())
