# プロジェクト定義書: Architecture & Roadmap

## 1. プロジェクトの目的
Django (MVT) から モダンなヘッドレス構成 (Django Ninja + React) への完全移行。
「チュートリアル卒業」レベルから「実務で通用するフルスタックエンジニア」へのスキルアップを目指す。

## 2. アーキテクチャ構成 (Project Structure)

本プロジェクトはモノレポ構成を採用する。

```
root/
├── .context/          # プロジェクト定義・ルール（このファイル群）
├── CLAUDE.md          # AIへの指示（メイン設定）
│
├── frontend/          # React + Vite (SPA)
│   ├── src/
│   │   ├── api/       # OpenAPI生成クライアント
│   │   ├── components/# UIコンポーネント
│   │   └── pages/     # ページコンポーネント
│   ├── tests/
│   │   └── e2e/       # Playwrightテスト
│   └── playwright.config.ts
│
└── myproject/         # Django Backend
    ├── manage.py
    ├── myproject/     # プロジェクト設定
    │   ├── settings.py
    │   ├── urls.py
    │   └── test_api.py  # テスト用API (reset-db)
    └── items/         # アプリケーション
        ├── api.py     # Django Ninja エンドポイント
        ├── models.py
        ├── schemas.py # Pydanticスキーマ
        └── fixtures/  # テスト用初期データ
```

## 3. 技術スタック (Target Stack 2025)

### Backend
- **Framework**: Django 6.0 + Django Ninja (Pydanticベース)
- **Async**: 完全非同期対応 (`async def`, `acreate`, `aget_object_or_404`)
- **Tooling**: `uv` (Package Manager), `Ruff` (Linter)
- **Auth**: JWT (HttpOnly Cookie優先)

### Frontend
- **Framework**: React + Vite (SPA)
- **State**: TanStack Query (Server), Zustand (Client)
- **Type**: TypeScript (Strict), OpenAPIによる型自動生成
- **Form**: React Hook Form + Zod
- **Routing**: React Router v7

## 4. コーディング指針 (Coding Guidelines)

1. **型安全性**: `any` 型の使用禁止。Pydantic/Zod/OpenAPIを活用する。
2. **分離の原則**: バックエンドはJSONAPIに徹する。Templateは使用しない。
3. **モダンスタンダード**:
   - `useEffect` でのデータ取得禁止 -> `useQuery` を使用。
   - `sync_to_async` ラッパーの使用禁止 -> ネイティブ非同期APIを使用。

## 5. 禁止事項 (Anti-Patterns)

- Django REST Framework (DRF) の使用
- LocalStorage へのトークン保存 (HttpOnly Cookie必須)
- 古いDjangoの同期的な書き方 (例: `Model.objects.get()`)
- `page.waitForTimeout()` の使用（E2Eテスト）

## 6. 開発ロードマップ (Progress)

### フェーズ 1: 開発基盤の刷新
- [x] uv / Ruff の導入
- [x] Docker化（開発環境の統一）

### フェーズ 2: バックエンドのAPI化
- [x] Django Ninja導入とスキーマ設計
- [x] CRUD実装と非同期化
- [x] OpenAPI (Swagger) での動作確認
- [x] Limit/Offset ページネーション

### フェーズ 3: フロントエンド構築
- [x] Vite + React プロジェクト作成
- [x] TanStack Query導入とAPIクライアント生成
- [x] React Router導入
- [x] UIコンポーネント実装（ItemManager等）

### フェーズ 4: 認証とセキュリティ
- [x] JWT認証 (HttpOnly Cookie)
- [x] ログイン機能の実装
- [x] CORS / CSRF 対策の強化

### フェーズ 5: 品質保証と運用
- [x] Pytest移行 (Async対応)
- [x] Playwright導入 (E2E)
- [x] DBリセットAPI (`/api/test/reset-db`)
- [x] CI/CD (GitHub Actions)
- [ ] Visual Regression Testing
