from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.TodoListView.as_view(), name='todo_list')
]