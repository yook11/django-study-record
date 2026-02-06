FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係を先にコピー（高速化のため）
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache

# アプリのコードをコピー
COPY . .

# エントリポイントスクリプトに実行権限付与
RUN chmod +x docker-entrypoint.sh

# ポート開放
EXPOSE 8000

# エントリポイント（マイグレーション自動実行）
ENTRYPOINT ["./docker-entrypoint.sh"]

# サーバー起動コマンド
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
