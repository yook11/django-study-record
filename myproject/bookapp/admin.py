from django.contrib import admin

from .models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_date")
    search_fields = ("title", "author")
    list_filter = ("publication_date",)


admin.site.register(Book, BookAdmin)

# Register your models here.
