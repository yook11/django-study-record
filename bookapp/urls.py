from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("<int:pk>/", views.book_detail, name="book_detail"),
    path("new/", views.book_create, name="book_create"),
    path("<int:pk>/edit/", views.book_update, name="book_update"),
    path("<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("messages/", views.add_messages, name="add_messages"),
    path("display/", views.show_display_messages, name="display_messages"),
    path("educationapp/", include("educationapp.urls")),
]
