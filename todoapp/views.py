from django.shortcuts import render
from . import models
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.utils.timezone import localtime
from django.urls import reverse_lazy
from .forms import TodoForm

class TodoListView(ListView):
    model = models.Todo
    template_name = 'todoapp/todo_list.html'
    context_object_name = 'todos'

class TodoDetailView(DetailView):
    model = models.Todo
    template_name = 'todoapp/todo_detail.html'
    context_object_name = 'todo'

class TodoCreateView(CreateView):
    model = models.Todo
    template_name = 'todoapp/todo_create.html'
    form_class = TodoForm
    success_url = reverse_lazy('todo_list')


class TodoupdateView(UpdateView):
    model = models.Todo
    template_name = 'todoapp/todo_update.html'
    form_class = TodoForm
    success_url = reverse_lazy('todo_list')

    def form_vaild(self, form):
        todo = form.save()
        print(f"タイトル: '{todo.title}' 更新時間: {localtime(todo.updated)}")
        return super().form_vaild(form)

class TodoDeleteView(DeleteView):
    model = models.Todo
    template_name = 'todoapp/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')


