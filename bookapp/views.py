from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import BookForm
from django.contrib import messages
import os
from django .conf import settings

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookapp/book_list.html', {'book_list': books})


def book_detail(request, pk):
    target = get_object_or_404(Book, pk=pk)
    return render(request, 'bookapp/book_detail.html', {'book':target})


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '書籍が正常に登録されました。')
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'bookapp/book_form.html', {'form': form, 'title': '書籍登録'})


def book_update(request, pk):
    target = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=target)
        if 'cover_image-clear' in request.POST:
            cover_image_delete(target)
        if form.is_valid():
            form.save()
            messages.success(request, '書籍が正常に更新されました。')
            return redirect('book_list')
    else:
        form = BookForm(instance=target)
    
    return render(request, 'bookapp/book_form.html', {'form': form, 'title':'書籍編集'})


def book_delete(request, pk):
    target = get_object_or_404(Book, pk=pk)
    if request.method =='POST':
        cover_image_delete(target)
        target.delete()
        messages.success(request, '書籍が正常に削除されました。')
        return redirect('book_list')
    return render(request, 'bookapp/book_confirm_delete.html', {'book': target})


#メッセージフレームワークのサンプル
#メッセージの追加
def add_messages(request):
    messages.success(request, 'これは成功メッセージです。')
    messages.error(request, 'これはエラーメッセージです。')
    messages.info(request, 'これは情報メッセージです。')
    messages.warning(request, 'これは警告メッセージです。')
    messages.debug(request, 'これはデバッグメッセージです。')
    return redirect('display_messages')

#メッセージの表示
def show_display_messages(request):
    return render(request, 'bookapp/show_all_messages.html')

#画像ファイルの削除
def cover_image_delete(target):
    if target.cover_image:
        image_path = settings.MEDIA_ROOT / target.cover_image.name

        if image_path.exists():
            image_path.unlink()


