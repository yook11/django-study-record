from django import forms
from .models import Book

class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_date', 'cover_image']

        labels = {
            'title': 'タイトル',
            'author': '著者',
            'publication_date': '出版日',
            'cover_image': '表紙画像'
        }