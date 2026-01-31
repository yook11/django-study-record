import base64
import io

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.timezone import localtime
from django.views import View, generic
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from . import models
from .forms import TodoForm


# ==========================================
# 共通のベースView：ログイン必須 ＋ メッセージ対応
# ==========================================
class TodoBaseView(LoginRequiredMixin, SuccessMessageMixin):
    model = models.Todo
    success_url = reverse_lazy("todo_list")

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # ここに共通の設定をまとめておくことができます


# ==========================================
# 各画面のView：TodoBaseViewを継承する
# ==========================================


class TodoListView(TodoBaseView, ListView):  # 一覧もログイン必須にする場合
    template_name = "todoapp/todo_list.html"
    context_object_name = "todos"
    paginate_by = 2


class TodoDetailView(TodoBaseView, DetailView):
    template_name = "todoapp/todo_detail.html"
    context_object_name = "todo"


class TodoCreateView(TodoBaseView, CreateView):
    template_name = "todoapp/todo_create.html"
    form_class = TodoForm
    success_message = "ToDoが登録されました"


class TodoUpdateView(TodoBaseView, UpdateView):  # クラス名のタイポ(Todoupdate)も修正しました
    template_name = "todoapp/todo_update.html"
    form_class = TodoForm
    success_message = "ToDoが更新されました"

    def form_valid(self, form):  # メソッド名のタイポ(vaild)も修正しました
        todo = form.save()
        print(f"タイトル: '{todo.title}' 更新時間: {localtime(todo.updated)}")
        return super().form_valid(form)


class TodoDeleteView(TodoBaseView, DeleteView):
    template_name = "todoapp/todo_confirm_delete.html"
    success_message = "ToDoが削除されました"


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "todoapp/signup.html"


class TodoAnalyticsView(View):
    template_name = "todoapp/todo_analytics.html"

    # GETリクエスト(ページの表示が来たときに実行されるメソッド)
    def get(self, request, *args, **kwargs):
        # todoモデルから完了、未完了の統計データを取得
        stats = models.Todo.get_completion_stats()
        # グラフの枠組みを生成(1,2行、サイズは横12✖︎縦5インチ)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        # ------- 左側、円グラフの作成 --------
        # グラフのラベル設定
        labels = ["Completed", "Incomplete"]
        # グラフの値(完了タスク数と未完了タスク数)
        sizes = [stats["completed"], stats["not_completed"]]
        # グラフの色設定(完了は緑、未完了はピンク)
        colors = ["#66FF99", "#FF3399"]
        # 円グラフを描写
        ax1.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90)
        # 円グラフを真円に保つ設定
        ax1.axis("equal")
        # グラフのタイトル設定
        ax1.set_title("Completion Rate")

        # ------- 右側、棒グラフの作成 --------
        # Todo モデルからデータをDataFrame形式で取得
        df = models.Todo.get_todos_dataframe()
        # データが存在する場合のみグラフ作成
        if not df.empty:
            # 日付
            df["created_date"] = df["created"].dt.date
            # 作成びごとにタスク数をカウント
            daily_counts = df.groupby("created_date").size()

            # 最新の7件のみ取得
            recent_counts = daily_counts.tail(7)

            # Y軸の最大値を5に設定
            ax2.set_ylim(0, 5)

            # 棒グラフを描写
            recent_counts.plot(kind="bar", ax=ax2, color="#4e73df")

            # X軸のラベルを回転させて重なりを防ぐ
            plt.xticks(rotation=20)

            # タイトルと軸ラベルを英語で設定
            ax2.set_title("Recent Task Creation")
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Number of Tasks")

        # ---------- ③ グラフをイメージデータに変換 ----------
        # メモリ上に一時的なバッファを作成
        buffer = io.BytesIO()
        # グラフのレイアウトを調整（グラフ同士が重ならないように）
        plt.tight_layout()
        # グラフをPNG形式で一時バッファに保存
        plt.savefig(buffer, format="png")
        # バッファの読み取り位置を先頭に戻す
        buffer.seek(0)
        # バッファからイメージデータを取得
        image_png = buffer.getvalue()
        # バッファを閉じる
        buffer.close()

        # イメージデータをBase64形式（テキスト形式）に変換
        # これによりHTMLに直接埋め込めるようになる
        graph = base64.b64encode(image_png).decode("utf-8")

        # ---------- ④ テンプレートにデータを渡す ----------

        # テンプレートに渡すデータを辞書で準備
        context = {
            "stats": stats,
            "graph": graph,
        }
        # テンプレートをレンダリングしてHTMLを生成し、レスポンスとして返す
        return render(request, self.template_name, context)
