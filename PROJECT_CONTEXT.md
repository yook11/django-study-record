# プロジェクト定義書: Django × React モダンWebアプリケーション移行計画 (2025 ver)

## 1. プロジェクトの目的
書籍で作成した従来のDjangoアプリケーション（MVT構成）を、2025年の業界標準である**「ヘッドレスアーキテクチャ（分離構成）」**へと作り変える。これにより、「チュートリアル卒業」レベルから「実務で通用するフルスタックエンジニア」へのスキルアップを目指す。

## 2. 技術スタック (Target Stack 2025)
本プロジェクトでは、以下のモダンな技術選定に基づき実装を行う。

### Backend (Python/Django)
- **API Framework**: `Django Ninja` (Django REST Frameworkではなく、Pydanticベースの高速・型安全なFWを採用)
- **Package Manager**: `uv` (pip/Poetryからの移行)
- **Linter/Formatter**: `Ruff` (Flake8/Blackからの移行)
- **Async Strategy**: ASGI対応、非同期ビュー (`async def`) の積極採用
- **Async ORM**: `acreate()`, `asave()`, `adelete()`, `aget_object_or_404()`, `async for` を使用
- **ASGI Server**: `uvicorn` または `granian` (Rustベース)
- **Doc**: OpenAPI (Swagger UI) による自動生成

### Frontend (TypeScript/React)
- **Build Tool**: `Vite` (Next.jsではなく、まずは純粋なSPA構成を採用)
- **Language**: TypeScript (Strict Mode必須)
- **State Management**: `TanStack Query` (サーバー状態管理)、`Zustand` (クライアント状態管理)
- **Form**: React Hook Form + Zod
- **API Client**: OpenAPIスキーマからの型定義自動生成 (`openapi-typescript` 等)

### Infrastructure & DevOps
- **Environment**: Docker & Docker Compose
- **Testing**: Pytest (Backend), Playwright (E2E)
- **CI/CD**: GitHub Actions

## 3. 開発ロードマップ

### フェーズ 1: 開発基盤の刷新 (Environment Modernization)
**ゴール**: ストレスのない爆速開発環境の構築
- [ ] **Docker化**: 開発環境（Django + DB）を `docker-compose.yml` で定義し、環境依存を排除する。
- [ ] **uv 導入**: パッケージ管理を `uv` に切り替え、依存解決の高速化を図る。
- [ ] **Ruff 導入**: リント・フォーマット設定を `pyproject.toml` に集約し、保存時自動整形を有効化する。

### フェーズ 2: バックエンドのAPI化 (Backend Modernization)
**ゴール**: Django Ninjaを用いた型安全なAPIの実装
- [ ] **Django Ninja導入**: `api.py` を作成し、Pydanticスキーマ (`Schema`) を設計する。
- [ ] **CRUD実装**: 既存の書籍アプリのデータを返すエンドポイントを実装する（DRFではなくNinjaを使用）。
- [ ] **非同期化**: I/Oバウンドな処理（DBアクセス等）を `async def` 化する。
- [ ] **OpenAPI確認**: 自動生成されたSwagger UIでAPIの動作確認を行う。

### フェーズ 3: フロントエンド構築 (Frontend Construction)
**ゴール**: Vite + ReactによるSPAの実装とAPI連携
- [ ] **Viteプロジェクト作成**: React + TypeScriptテンプレートで構築。
- [ ] **TanStack Query導入**: `useEffect` ではなく、推奨ライブラリでのデータ取得を実装。
- [ ] **クライアント生成**: バックエンドの `openapi.json` からTypeScriptの型定義を自動生成するワークフローを確立。
- [ ] **UI実装**: 書籍一覧・詳細・登録画面をコンポーネント指向で実装する。

### フェーズ 4: 認証とセキュリティ (Security & Auth)
**ゴール**: セキュアなSPA認証の実装
- [ ] **JWT認証**: Simple JWT等をカスタマイズし、HttpOnly Cookie にトークンを保存する方式を実装（LocalStorageは禁止）。
- [ ] **CORS/CSRF設定**: フロントエンド・バックエンド間の通信許可と、SPAにおけるCSRF対策を実装。

### フェーズ 5: 品質保証と運用 (QA & DevOps)
**ゴール**: テスト自動化とCI/CD
- [ ] **Pytest移行**: `unittest` からPytestへ移行し、非同期テストを記述。
- [ ] **Playwright導入**: ユーザーの操作（ログイン〜データ登録）を自動化するE2Eテストを作成。
- [ ] **GitHub Actions**: Push時に自動でLint/Testが走るパイプラインを構築。

## 4. コーディング指針 (AIへの指示)
1. **「動く」より「堅牢」を優先**: `any` 型の使用を禁止し、PydanticやZodによるスキーマ定義を徹底すること。
2. **分離の原則**: バックエンドはJSONの返却のみに集中し、HTML生成（Template）は行わないこと。
3. **最新のベストプラクティス**: 2024-2025年時点のドキュメントに基づき、非推奨なメソッド（`useEffect`でのデータフェッチ等）は提案しないこと。

## 5. バージョン要件
| 領域 | 技術 | バージョン |
|------|------|------------|
| Runtime | Python | >=3.13 |
| Backend | Django | >=6.0 |
| Backend | Django Ninja | >=1.5 |
| Frontend | Node.js | >=20 LTS |

## 6. 禁止事項（アンチパターン）
以下の実装パターンは禁止とする：
- **Django REST Framework**の使用（Django Ninjaを使用すること）
- **`sync_to_async`**による同期ORMのラップ（Django 6.0ネイティブ非同期APIを使用すること）
- **LocalStorage**へのJWTトークン保存（HttpOnly Cookieを使用すること）
- **`useEffect`**でのデータフェッチ（TanStack Queryを使用すること）
- **TypeScriptの`any`型**（厳密な型定義を使用すること）

## 7. 移行方針
既存MVTアプリのDjango Ninja API移行優先順位：
1. **bookapp**（書籍アプリ）- 主要機能、最優先
2. **todoapp**（Todoアプリ）- CRUD練習として活用
3. **その他**（educationapp, appendixapp, helloapp）- 必要に応じて段階的に移行

## 8. テスト戦略
| レイヤー | ツール | 用途 |
|----------|--------|------|
| Unit | pytest + pytest-asyncio | 非同期関数のユニットテスト |
| API | pytest + httpx (AsyncClient) | APIエンドポイントの統合テスト |
| E2E | Playwright + pytest-playwright | ブラウザ操作の自動化テスト |