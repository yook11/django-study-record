from django.shortcuts import render
from . import models
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.utils.timezone import localtime
from django.urls import reverse_lazy
from .forms import TodoForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# ==========================================
# 共通のベースView：ログイン必須 ＋ メッセージ対応
# ==========================================
class TodoBaseView(LoginRequiredMixin, SuccessMessageMixin):
    model = models.Todo
    success_url = reverse_lazy('todo_list')
    # ここに共通の設定をまとめておくことができます

# ==========================================
# 各画面のView：TodoBaseViewを継承する
# ==========================================

class TodoListView(TodoBaseView, ListView): # 一覧もログイン必須にする場合
    template_name = 'todoapp/todo_list.html'
    context_object_name = 'todos'

class TodoDetailView(TodoBaseView, DetailView):
    template_name = 'todoapp/todo_detail.html'
    context_object_name = 'todo'

class TodoCreateView(TodoBaseView, CreateView):
    template_name = 'todoapp/todo_create.html'
    form_class = TodoForm
    success_message = 'ToDoが登録されました'

class TodoUpdateView(TodoBaseView, UpdateView): # クラス名のタイポ(Todoupdate)も修正しました
    template_name = 'todoapp/todo_update.html'
    form_class = TodoForm
    success_message = 'ToDoが更新されました'

    def form_valid(self, form): # メソッド名のタイポ(vaild)も修正しました
        todo = form.save()
        print(f"タイトル: '{todo.title}' 更新時間: {localtime(todo.updated)}")
        return super().form_valid(form)

class TodoDeleteView(TodoBaseView, DeleteView):
    template_name = 'todoapp/todo_confirm_delete.html'
    success_message = 'ToDoが削除されました'