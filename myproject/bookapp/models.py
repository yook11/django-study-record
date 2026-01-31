from django.db import models

# Create your models here.


class Book(models.Model):
    title = models.CharField(verbose_name="タイトル", max_length=20)

    author = models.CharField(verbose_name="著者", max_length=10)

    publication_date = models.DateField(verbose_name="出版日")

    cover_image = models.ImageField(
        verbose_name="表紙画像", upload_to="book_covers", blank=True, null=True
    )

    def __str__(self):
        return self.title
