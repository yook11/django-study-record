.PHONY: up down logs migrate shell test test-e2e reset-db rebuild

# 開発環境起動
up:
	docker compose up -d

# 停止
down:
	docker compose down

# ログ確認
logs:
	docker compose logs -f backend

# マイグレーション
migrate:
	docker compose exec backend uv run python manage.py migrate

# Django shell
shell:
	docker compose exec backend uv run python manage.py shell

# バックエンドテスト
test:
	docker compose exec backend uv run pytest

# E2Eテスト（フロントはローカル）
test-e2e:
	cd frontend && npx playwright test

# DB リセット
reset-db:
	curl -X POST http://localhost:8000/api/test/reset-db

# 全て再ビルド
rebuild:
	docker compose down -v
	docker compose build --no-cache
	docker compose up -d

# スーパーユーザー作成
createsuperuser:
	docker compose exec backend uv run python manage.py createsuperuser
