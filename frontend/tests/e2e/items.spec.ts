import { test, expect } from '@playwright/test';

// 各テスト前にDBをリセット（認証はGlobal Setupで完了済み）
test.beforeEach(async ({ page, request }) => {
  // DBリセット（Fixtureの初期データ: 3件の商品が存在する状態）
  const resetResponse = await request.post('http://localhost:8000/api/test/reset-db');
  expect(resetResponse.status()).toBe(200);

  // /itemsページに移動
  await page.goto('/items');

  // ローディング完了を待機
  await expect(page.getByRole('heading', { name: 'Items管理アプリ' })).toBeVisible();
});

test.describe('商品CRUD操作', () => {
  test('商品作成 - 新しい商品を追加できる', async ({ page }) => {
    // 決定論的な商品名を使用
    const itemName = 'テスト新商品';

    // 商品名を入力
    await page.getByPlaceholder('名前').fill(itemName);

    // 価格を入力
    await page.getByPlaceholder('価格').fill('1500');

    // 追加ボタンをクリック
    await page.getByRole('button', { name: '追加' }).click();

    // TanStack Queryの自動再フェッチを待機
    await page.waitForResponse(response =>
      response.url().includes('/api/items') && response.status() === 200
    );

    // 新しい商品が一覧に追加されたことを確認
    const itemRow = page.getByRole('listitem').filter({ hasText: itemName });
    await expect(itemRow).toBeVisible();
    await expect(itemRow).toContainText('¥1500');

    // フォームがクリアされたことを確認
    await expect(page.getByPlaceholder('名前')).toHaveValue('');
    await expect(page.getByPlaceholder('価格')).toHaveValue('');
  });

  test('商品一覧表示 - 初期データが正しく表示される', async ({ page }) => {
    // Fixtureからロードされた3件の商品を確認
    const itemsList = page.getByRole('listitem');

    // 絶対値で検証（Fixture由来の3件）
    await expect(itemsList).toHaveCount(3);

    // 各商品に削除ボタンがあることを確認
    const firstItem = itemsList.first();
    await expect(firstItem.getByRole('button', { name: '削除' })).toBeVisible();

    // Fixtureの商品名が表示されていることを確認
    await expect(page.getByText('サンプル商品A')).toBeVisible();
    await expect(page.getByText('サンプル商品B')).toBeVisible();
    await expect(page.getByText('サンプル商品C')).toBeVisible();
  });

  test('商品削除 - 商品を削除できる', async ({ page }) => {
    // Fixtureから存在する商品を削除（UI作成不要）
    const targetItem = page.getByRole('listitem').filter({ hasText: 'サンプル商品A' });
    await expect(targetItem).toBeVisible();

    // 削除確認ダイアログを承認
    page.once('dialog', dialog => dialog.accept());
    await targetItem.getByRole('button', { name: '削除' }).click();

    // TanStack Queryの自動再フェッチを待機
    await page.waitForResponse(response =>
      response.url().includes('/api/items') && response.request().method() === 'DELETE'
    );

    // 商品が削除されたことを確認
    await expect(targetItem).not.toBeVisible();

    // 残り2件になったことを確認
    await expect(page.getByRole('listitem')).toHaveCount(2);
  });

  test('複数商品の作成 - 連続して商品を追加できる', async ({ page, request }) => {
    // API経由でテストデータを作成（UI操作ではなくAPIを使用）
    const testItems = [
      { name: '追加商品X', price: 100 },
      { name: '追加商品Y', price: 200 },
      { name: '追加商品Z', price: 300 },
    ];

    for (const item of testItems) {
      await request.post('http://localhost:8000/api/items', {
        data: item,
      });
    }

    // ページをリロードして最新データを取得
    await page.reload();
    await expect(page.getByRole('heading', { name: 'Items管理アプリ' })).toBeVisible();

    // Fixture(3件) + 新規(3件) = 6件
    await expect(page.getByRole('listitem')).toHaveCount(6);

    // 追加した商品が表示されることを確認
    for (const item of testItems) {
      const itemRow = page.getByRole('listitem').filter({ hasText: item.name });
      await expect(itemRow).toBeVisible();
      await expect(itemRow).toContainText(`¥${item.price}`);
    }
  });

  test('バリデーション - 空の商品名では追加できない', async ({ page }) => {
    // 名前を空にして価格のみ入力
    await page.getByPlaceholder('名前').clear();
    await page.getByPlaceholder('価格').fill('1000');

    // 追加ボタンをクリック
    const addButton = page.getByRole('button', { name: '追加' });
    await addButton.click();

    // フォームのバリデーションにより、商品が追加されないことを確認
    await expect(page).toHaveURL('/items');

    // 商品数が変わっていないことを確認（Fixture由来の3件のまま）
    await expect(page.getByRole('listitem')).toHaveCount(3);
  });
});

test.describe('商品一覧ページネーション', () => {
  test('複数ページの表示とナビゲーション', async ({ page, request }) => {
    // API経由で追加の12件を作成（Fixture3件 + 12件 = 15件で2ページ分）
    for (let i = 1; i <= 12; i++) {
      await request.post('http://localhost:8000/api/items', {
        data: { name: `ページテスト商品${i}`, price: i * 100 },
      });
    }

    // ページをリロード
    await page.reload();
    await expect(page.getByRole('heading', { name: 'Items管理アプリ' })).toBeVisible();

    // 1ページ目の確認（最新10件が表示）
    await expect(page.getByText(/Page 1 \/ /)).toBeVisible();
    await expect(page.getByRole('button', { name: '前のページ' })).toBeDisabled();

    // 「次へ」ボタンをクリック
    const nextButton = page.getByRole('button', { name: '次のページ' });
    await expect(nextButton).toBeEnabled();
    await nextButton.click();

    // 2ページ目のデータ読み込みを待機
    await page.waitForResponse(response =>
      response.url().includes('/api/items?limit=10&offset=10') &&
      response.status() === 200
    );

    // 2ページ目の確認
    await expect(page.getByText(/Page 2 \/ /)).toBeVisible();

    // 「前へ」ボタンで1ページ目に戻る
    const prevButton = page.getByRole('button', { name: '前のページ' });
    await expect(prevButton).toBeEnabled();
    await prevButton.click();

    await expect(page.getByText(/Page 1 \/ /)).toBeVisible();
  });

  test('空ページの処理 - 最終ページで最後の商品を削除', async ({ page, request }) => {
    // API経由で8件追加（Fixture3件 + 8件 = 11件で2ページ: 10 + 1）
    for (let i = 1; i <= 8; i++) {
      await request.post('http://localhost:8000/api/items', {
        data: { name: `削除テスト商品${i}`, price: i * 100 },
      });
    }

    // ページをリロード
    await page.reload();
    await expect(page.getByRole('heading', { name: 'Items管理アプリ' })).toBeVisible();

    // 2ページ目へ移動
    await page.getByRole('button', { name: '次のページ' }).click();
    await page.waitForResponse(r => r.url().includes('offset=10'));

    // 2ページ目に1件あることを確認
    await expect(page.getByText(/Page 2 \/ 2/)).toBeVisible();
    const itemsOnPage2 = page.getByRole('listitem');
    await expect(itemsOnPage2).toHaveCount(1);

    // 2ページ目の唯一の商品を削除
    const itemOnPage2 = itemsOnPage2.first();
    page.once('dialog', dialog => dialog.accept());
    await itemOnPage2.getByRole('button', { name: '削除' }).click();
    await page.waitForResponse(r =>
      r.url().includes('/api/items') && r.request().method() === 'DELETE'
    );

    // TanStack Queryの自動再フェッチ完了を待機
    await page.waitForResponse(r =>
      r.url().includes('/api/items') && r.request().method() === 'GET'
    );

    // 自動的に1ページ目に戻ることを確認
    await expect(page.getByText(/Page 1 \/ 1/)).toBeVisible();
  });

  test('1ページのみの場合 - ページネーションボタンの状態', async ({ page }) => {
    // Fixture由来の3件のみ（10件未満なので1ページ）

    // 両方のボタンが無効であることを確認
    await expect(page.getByRole('button', { name: '前のページ' })).toBeDisabled();
    await expect(page.getByRole('button', { name: '次のページ' })).toBeDisabled();

    // "Page 1 / 1"が表示されることを確認
    await expect(page.getByText(/Page 1 \/ 1/)).toBeVisible();
  });
});
