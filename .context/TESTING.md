# テスト戦略ガイドライン (Testing Strategy 2025)

本プロジェクトでは「テスティングトロフィー」モデルを採用し、ROI（投資対効果）を最大化する。

## 1. テストレイヤーと役割 (The Testing Trophy)

| レイヤー | ツール | カバレッジ方針 |
| :--- | :--- | :--- |
| **Static Analysis** | **Ruff / ESLint** | **100% (必須)**。実行前に構文エラーや型不整合を排除する。 |
| **Integration** | **Pytest / Vitest** | **最大ボリューム**。コンポーネント間の連携、API通信(MSW)、DB操作を検証する。 |
| **E2E** | **Playwright** | **クリティカルパスのみ**。認証、決済、主要CRUDなど、ビジネス価値の高いフローを保証する。 |
| **Unit** | **Pytest / Vitest** | **最小限**。純粋なロジック関数やエッジケースのみ対象。UI描画テストは避ける。 |

## 2. E2Eテスト実装ルール (Playwright)

### 🛑 絶対禁止事項 (Strictly Prohibited)
- **固定待機 (`waitForTimeout`, `sleep`)**:
  - テストが不安定(Flaky)になる主原因。絶対に使用しない。
- **実装詳細への依存**:
  - CSSクラス (`.btn-primary`) や XPath (`div > span`) で要素を探さない。
- **UI経由でのデータ準備**:
  - テストの前準備で「画面ポチポチ」でデータを作らない。必ずAPIかFixtureを使う。

### ✅ 推奨実装パターン (Best Practices)

#### DBリセット戦略
`test.beforeEach` で必ずリセットAPIを呼び出す。

```typescript
test.beforeEach(async ({ page, request }) => {
  // フルパス指定が必要（Viteプロキシがないため）
  await request.post('http://localhost:8000/api/test/reset-db');
});
```

#### 待機戦略 (Auto-waiting)
- `page.waitForResponse` を使用し、通信の完了を待つ。
- `expect(locator).toBeVisible()` の自動リトライを活用する。

```typescript
// ✅ 良い例: APIレスポンスを待つ
const responsePromise = page.waitForResponse(resp =>
  resp.url().includes('/api/items') && resp.status() === 200
);
await page.getByRole('button', { name: '保存' }).click();
await responsePromise;

// ✅ 良い例: 要素の表示を待つ（自動リトライ）
await expect(page.getByText('保存しました')).toBeVisible();
```

#### セレクター優先順位 (User-facing Locators)
1. `getByRole` (button, link, heading...) - 最優先
2. `getByLabel` (form inputs)
3. `getByPlaceholder`
4. `getByText` (content)
5. `getByTestId` - 最終手段

### 🔐 認証の最適化 (Global Setup)

ログイン処理は時間がかかるため、`storageState` を使用して認証情報を再利用する。

**playwright.config.ts 設定例:**
```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  projects: [
    // 認証用のセットアッププロジェクト
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: {
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
});
```

**auth.setup.ts 例:**
```typescript
import { test as setup } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('http://localhost:5173/login');
  await page.getByLabel('ユーザー名').fill('testuser');
  await page.getByLabel('パスワード').fill('password123');
  await page.getByRole('button', { name: 'ログイン' }).click();
  await page.waitForURL('http://localhost:5173/');
  await page.context().storageState({ path: authFile });
});
```

### 📂 プロジェクト構成

現在のディレクトリ構成:
```
frontend/
  ├── tests/
  │   └── e2e/           # E2Eテスト (playwright.config.tsのtestDir)
  │       ├── items.spec.ts
  │       └── auth.spec.ts
  └── playwright.config.ts
```

POM導入後の推奨構成:
```
frontend/
  ├── tests/
  │   └── e2e/
  │       ├── fixtures/      # カスタムフィクスチャ
  │       ├── pages/         # Page Objects
  │       │   ├── LoginPage.ts
  │       │   └── ItemsPage.ts
  │       └── specs/         # テスト仕様書
  │           └── items.spec.ts
  └── playwright.config.ts
```

### 🔧 playwright.config.ts 推奨設定

```typescript
use: {
  baseURL: 'http://localhost:5173',
  // 失敗時のみトレースとスクリーンショットを保存
  trace: 'retain-on-failure',
  screenshot: 'only-on-failure',
},
```

## 3. バックエンドテスト (Pytest)

### DBアクセス
- SQLiteは使用せず、Docker上のPostgres等、本番に近い環境を使用する。

### 非同期テスト
- `pytest-asyncio` を使用し、`async def test_...` で記述する。
- ORM操作には `acreate`, `aget` 等の非同期メソッドを使用する。

```python
@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_create_item(async_client):
    response = await async_client.post('/api/items', json={'name': 'Test'})
    assert response.status_code == 200
```

## 4. CI/CD 最適化

### シャーディング (Sharding)
テスト数が増えた場合、`--shard` オプションで分割実行する。

```bash
# 4並列の例
npx playwright test --shard=1/4
npx playwright test --shard=2/4
npx playwright test --shard=3/4
npx playwright test --shard=4/4
```

### GitHub Actions 設定例
```yaml
jobs:
  test:
    strategy:
      matrix:
        shardIndex: [1, 2, 3, 4]
        shardTotal: [4]
    steps:
      - run: npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
```

### デバッグアーティファクト
失敗時のみトレースとスクリーンショットを保存する設定を推奨。
