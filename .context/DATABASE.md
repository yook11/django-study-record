# Database & Fixture Management Guidelines

## 1. テストデータ管理の基本方針

E2Eテストの安定性を保証するため、**「テスト実行ごとにDBを完全リセットし、固定の初期データのみが存在する状態」** を作り出す戦略を採用する。

テストコード内でアドホックにデータを作成するのではなく、定義済みのFixture（`initial_data.json`）をロードすることを基本とする。

## 2. DBリセットAPIの仕様

テスト実行時（`beforeEach`）に呼び出すAPIの詳細は以下の通り。

| 項目 | 値 |
|:---|:---|
| **Endpoint** | `POST /api/test/reset-db` |
| **Method** | `POST` |
| **Auth** | 不要（ただし `DEBUG=True` 環境限定） |
| **実装ファイル** | `myproject/myproject/test_api.py` |

**処理フロー:**
1. `settings.DEBUG` チェック（Falseなら403エラー）
2. `call_command('flush', '--no-input')`: 全データの消去
3. `call_command('loaddata', 'initial_data.json')`: 初期データの投入

## 3. 初期データ (Fixtures) の管理

### 📂 ファイルの場所
- **パス**: `myproject/items/fixtures/initial_data.json`
- **現在の内容**: `auth.User` のデータ（管理者・テストユーザー）

### ⚠️ 禁止事項 (Strict Rules)

**JSONファイルの直接編集は禁止**:
- `initial_data.json` をエディタで開いて手動で修正してはならない
- ハッシュ化されたパスワードや外部キーの整合性が壊れる原因となる
- データの追加・変更が必要な場合は、以下の「更新手順」に従うこと

### 🔄 Fixtureの更新手順 (Workflow)

初期データに新しいパターン（例：新しい管理者、新しい商品など）を追加したい場合は、以下の手順を実行する。

#### 1. 開発サーバーを起動
```bash
cd myproject
uv run python manage.py runserver
```

#### 2. データの作成
- Django Admin (`http://localhost:8000/admin`) またはAPI経由で、必要なデータを登録する
- 不要なゴミデータは削除し、理想的な「初期状態」を作る

#### 3. Dumpdataコマンドで上書き保存

以下のコマンドを実行し、現状をスナップショットとして保存する。

```bash
cd myproject
uv run python manage.py dumpdata auth.user items \
  --natural-foreign --natural-primary \
  --indent 2 > items/fixtures/initial_data.json
```

**オプション説明:**
- `--natural-foreign`: 外部キーをPKではなく自然キー（usernameなど）で参照
- `--natural-primary`: 主キーも自然キーで出力（移植性向上）
- `--indent 2`: 読みやすいインデント付きJSON

#### 4. 確認とコミット
```bash
git diff items/fixtures/initial_data.json
```
差分を確認し、意図したデータが含まれているかチェック。問題なければコミットする。

## 4. マイグレーション (Migrations)

モデル定義 (`models.py`) を変更した際は、必ず以下を実行する。

```bash
cd myproject
uv run python manage.py makemigrations
uv run python manage.py migrate
```

**重要**: マイグレーション後は `initial_data.json` が古くなる（スキーマ不整合）可能性があるため、上記「更新手順」を実施してFixtureを再生成すること。

## 5. トラブルシューティング

### Fixture読み込みエラー
```
DeserializationError: Problem installing fixture
```

**原因**: スキーマ変更後にFixtureを更新していない

**対処**: 手順3の `dumpdata` コマンドを再実行してFixtureを再生成する
