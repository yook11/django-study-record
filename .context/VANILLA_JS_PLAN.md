# Phase 1.5: Vanilla JS ItemManager 学習プラン

## 目的
React が裏で何をしてくれているかを体感するため、同じ Items API を **HTML 1枚 + vanilla JS** で再現する。

## 進捗チェックリスト

### Step 0: セットアップ（15分） -- DONE
- [x] `items_vanilla.html` スケルトン作成
- [x] `urls.py` に `/vanilla/` ルート追加
- [ ] ブラウザで `http://localhost:8000/vanilla/` 表示確認

### Step 1: ログインフォーム（25分） -- DONE
- [x] State: `isLoggedIn` 変数
- [x] API: `apiLogin(username, password)` — fetch POST + credentials
- [x] Render: `renderLoginForm()` — innerHTML でフォーム描画
- [x] Events: `attachLoginEvents()` — submit リスナー
- [x] `renderApp()` でログイン/メイン画面切り替え
- [ ] **比較体験**: `setError()` vs 手動 DOM 書き換え

### Step 2: アイテム一覧の取得・表示（30分） -- DONE
- [x] State: `items`, `totalCount`, `currentPage`, `isLoading`, `errorMessage`
- [x] API: `apiFetchItems(limit, offset)` — fetch GET
- [x] Render: `renderItemManager()` — Loading/Error/List 切り替え
- [x] `items.map().join('')` でリスト HTML 生成
- [x] `loadItems()`: render 2回呼び（Loading → 結果）
- [ ] **比較体験**: innerHTML 全破壊 → イベントリスナー再設置の手間

### Step 3: アイテム新規作成（25分） -- DONE
- [x] API: `apiCreateItem(name, price)` — fetch POST + JSON body
- [x] Render: 作成フォーム（name, price 入力）追加
- [x] Events: submit → API → `await loadItems()`（手動 invalidateQueries）
- [ ] **比較体験**: `invalidateQueries` 1行 vs 手動 re-fetch

### Step 4: 編集・削除（30分） -- DONE
- [x] API: `apiUpdateItem(id, name, price)` — fetch PUT
- [x] API: `apiDeleteItem(id)` — fetch DELETE
- [x] Events: **イベント委譲** — 親要素に1つの click リスナー + `e.target.classList.contains()`
- [x] State: `editingItem` で作成/編集フォーム切り替え
- [x] 削除時の最終ページ処理（`currentPage--`）
- [ ] **比較体験**: クロージャ vs `data-id` 属性 + 配列検索

### Step 5: ページネーション（20分） -- DONE
- [x] Render: `renderPagination()` — totalPages 算出、前へ/次へボタン
- [x] Events: ページ切り替え → `loadItems()`
- [x] disabled 属性の動的制御

### Step 6: 振り返り（15分） -- DONE
- [x] 手動ステップの多さ（作成1つに7ステップ vs React 2ステップ、render 15箇所呼出）
- [x] innerHTML の問題（フォーカス喪失、スクロールリセット、リスナー再設置）
- [x] 状態同期のバグリスク（render 呼び忘れ = UI古いまま。React は setState で自動）
- [x] XSS リスク（escapeHtml 忘れ = スクリプト実行。React JSX は自動エスケープ）
- [x] コード構成（5セクション = React コンポーネントの分解形。Render+Events = コンポーネント）
- [x] CSRF 保護（Ninja csrf=False / Django テンプレートは {% csrf_token %} 必須）

---

## コード構成ルール（5セクション）

```
1. State（状態管理）     — let state = { isLoggedIn, items, currentPage, ... }
2. API Clients（通信）   — apiLogin(), apiFetchItems(), apiCreateItem(), ...
3. Render Functions（描画）— renderApp(), renderLoginForm(), renderItemManager(), ...
4. Event Handlers（操作） — attachLoginEvents(), attachManagerEvents(), ...
5. Init（初期化）         — renderApp() を呼んで起動
```

> **気づきポイント**: React のコンポーネント = Render Functions + Event Handlers をセットにしたもの

---

## 技術メモ

### CSRF（対応不要）
- `NinjaExtraAPI()` のデフォルトは `csrf=False` → CsrfViewMiddleware をバイパス
- CSRFトークン送信は不要

### 同一オリジン
- `/vanilla/` も API も `localhost:8000` → CORS 問題なし
- `credentials: 'include'` は React版と揃えるため記述（同一オリジンでは厳密には不要）

---

## 参考ファイル
| ファイル | 用途 |
|---|---|
| `myproject/items/api.py` | API エンドポイント定義 |
| `myproject/myproject/auth_api.py` | ログイン/ログアウト API |
| `frontend/src/components/ItemManager.tsx` | React版（比較対象） |
| `frontend/src/api/hooks.ts` | TanStack Query フック |

## 検証方法
1. `uv run python manage.py runserver`
2. `http://localhost:8000/vanilla/` にアクセス
3. ログイン → 一覧 → 作成 → 編集 → 削除 → ページ送り
4. React 版（`http://localhost:5173/items`）と比較
