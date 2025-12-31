# HttpResponseクラスをインポート
from django.http import HttpResponse

# ------------------------------------------------------------------
# ビュー関数を定義
# "ハロー、Django!"というテキストを含むHTTPレスポンスを返す
# ------------------------------------------------------------------
def show_hello(request):
    # ▽▽▽▽▽ 7.6 ▽▽▽▽▽
    html_content = """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>Hello Django</title>
    </head>
    <body>
        <p>ハロー、Django！</p>
        <a href="/menu/">メニューに戻る</a>
    </body>
    </html>
    """
    return HttpResponse(html_content)
    # △△△△△ 7.6 △△△△△