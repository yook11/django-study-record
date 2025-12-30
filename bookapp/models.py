from django.db import models

# Create your models here.

class Book(models.Model):

    title = models.CharField(max_length=20)

    author = models.CharField(max_length=10)

    publication_date = models.DateField()

    cover_image = models.ImageField(upload_to='book_covers', blank=True, null=True)


    def __str__(self):
        return self.title

