from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import Bookform

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookapp/book_list.html', {'book_list': books})
