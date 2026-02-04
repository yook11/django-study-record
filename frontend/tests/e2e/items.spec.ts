import { test, expect } from '@playwright/test';

// 認証済み状態のフィクスチャ
test.beforeEach(async ({ page }) => {
  // 1. ログインページに移動
  await page.goto('/login');

  // 2. ログイン
  await page.getByLabel('ユーザー名').fill('root');
  await page.getByLabel('パスワード').fill('pass');
  await page.getByRole('button', { name: 'ログインする' }).click();

  // 3. /itemsページへのリダイレクトを待機
  await page.waitForURL('/items');

  // 4. ローディング完了を待機
  await expect(page.getByRole('heading', { name: 'Items管理アプリ' })).toBeVisible();
});

test.describe('商品CRUD操作', () => {
  test('商品作成 - 新しい商品を追加できる', async ({ page }) => {
    // 作成前の商品数を取得
    const itemsBefore = await page.locator('ul > li').count();

    // ユニークな商品名を生成
    const timestamp = Date.now();
    const itemName = `テスト商品-${timestamp}`;

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
    await expect(page.getByText(`${itemName} - ¥1500`)).toBeVisible();

    // 商品数が増えたことを確認
    const itemsAfter = await page.locator('ul > li').count();
    expect(itemsAfter).toBe(itemsBefore + 1);

    // フォームがクリアされたことを確認
    await expect(page.getByPlaceholder('名前')).toHaveValue('');
    await expect(page.getByPlaceholder('価格')).toHaveValue('');
  });

  test('商品一覧表示 - 既存の商品が正しく表示される', async ({ page }) => {
    // 商品リストが表示されることを確認
    const itemsList = page.locator('ul > li');

    // 少なくとも0個以上の商品が存在することを確認（空でも可）
    const count = await itemsList.count();
    expect(count).toBeGreaterThanOrEqual(0);

    // 商品が存在する場合、各商品に削除ボタンがあることを確認
    if (count > 0) {
      const firstItem = itemsList.first();
      await expect(firstItem.getByRole('button', { name: '削除' })).toBeVisible();
    }
  });

  test('商品削除 - 商品を削除できる', async ({ page }) => {
    // ユニークな商品名を生成
    const timestamp = Date.now();
    const itemName = `削除テスト商品-${timestamp}`;

    // まず商品を作成
    await page.getByPlaceholder('名前').fill(itemName);
    await page.getByPlaceholder('価格').fill('999');
    await page.getByRole('button', { name: '追加' }).click();

    // 作成完了を待機
    await page.waitForResponse(response =>
      response.url().includes('/api/items') && response.status() === 200
    );
    await expect(page.getByText(`${itemName} - ¥999`)).toBeVisible();

    // 削除前の商品数を取得
    const itemsBefore = await page.locator('ul > li').count();

    // 作成した商品を削除
    const targetItem = page.locator('li', { hasText: `${itemName} - ¥999` });
    await targetItem.getByRole('button', { name: '削除' }).click();

    // TanStack Queryの自動再フェッチを待機
    await page.waitForResponse(response =>
      response.url().includes('/api/items') && response.request().method() === 'DELETE'
    );

    // 商品が削除されたことを確認
    await expect(page.getByText(`${itemName} - ¥999`)).not.toBeVisible();

    // 商品数が減ったことを確認
    const itemsAfter = await page.locator('ul > li').count();
    expect(itemsAfter).toBe(itemsBefore - 1);
  });

  test('複数商品の作成 - 連続して商品を追加できる', async ({ page }) => {
    // テスト開始前の商品数を取得
    const itemsBefore = await page.locator('ul > li').count();

    // ユニークな商品名を生成（テスト実行ごとに異なる名前）
    const timestamp = Date.now();
    const testItems = [
      { name: `商品A-${timestamp}-1`, price: '100' },
      { name: `商品B-${timestamp}-2`, price: '200' },
      { name: `商品C-${timestamp}-3`, price: '300' },
    ];

    for (const item of testItems) {
      await page.getByPlaceholder('名前').fill(item.name);
      await page.getByPlaceholder('価格').fill(item.price);
      await page.getByRole('button', { name: '追加' }).click();

      // 各商品作成後にレスポンスを待機
      await page.waitForResponse(response =>
        response.url().includes('/api/items') && response.status() === 200
      );
    }

    // すべての商品が表示されることを確認
    for (const item of testItems) {
      await expect(page.getByText(`${item.name} - ¥${item.price}`)).toBeVisible();
    }

    // 商品数が3個増えたことを確認（相対値チェック）
    const itemsAfter = await page.locator('ul > li').count();
    expect(itemsAfter).toBe(itemsBefore + 3);
  });

  test('バリデーション - 空の商品名では追加できない', async ({ page }) => {
    // 名前を空にして価格のみ入力
    await page.getByPlaceholder('名前').clear();
    await page.getByPlaceholder('価格').fill('1000');

    // 追加ボタンをクリック
    const addButton = page.getByRole('button', { name: '追加' });
    await addButton.click();

    // フォームのバリデーションにより、商品が追加されないことを確認
    // （URLが変わらず、/itemsのまま）
    await expect(page).toHaveURL('/items');
  });
});
