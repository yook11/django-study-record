import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page, request }) => {
  // DBリセット（初期Fixtureをロード）
  const resetResponse = await request.post('http://localhost:8000/api/test/reset-db');
  expect(resetResponse.status()).toBe(200);

  // ログインページに移動
  await page.goto('http://localhost:5173/login');

  // ログイン
  await page.getByLabel('ユーザー名').fill('root');
  await page.getByLabel('パスワード').fill('pass');
  await page.getByRole('button', { name: 'ログインする' }).click();

  // リダイレクト完了を待機
  await page.waitForURL('http://localhost:5173/items');

  // ページ読み込み完了を確認
  await expect(page.getByRole('heading', { name: 'Items管理アプリ' })).toBeVisible();

  // 認証状態を保存
  await page.context().storageState({ path: authFile });
});
