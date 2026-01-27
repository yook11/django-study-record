from django import forms

from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title", "memo", "completed"]
        labels = {
            "title": "タスク名",
            "memo": "詳細メモ",
            "completed": "完了済み",
        }
