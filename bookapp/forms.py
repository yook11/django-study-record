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

        widgets = {
            'publication_date': forms.DateInput(attrs={'type': 'date'})
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if '盗作' in title:
            raise forms.ValidationError(
                "タイトルに盗作を含めることはできません。"
            )
        return title
    
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')

        if title == author:
            raise forms.ValidationError(
                'タイトルと著者名は同じにはできません。'
            )
        return cleaned_data