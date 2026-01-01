from django.shortcuts import render
from . import models
from django.views.generic import ListView

class TodoListView(ListView):
    model = models.Todo
    template_name = 'todoapp/todo_list.html'
    context_object_name = 'todos'

# Create your views here.
