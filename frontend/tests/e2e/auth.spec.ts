import { test, expect } from '@playwright/test';

test.describe('認証フロー', () => {
  test.beforeEach(async ({ page }) => {
    // 各テスト前にログインページへ
    await page.goto('/login');
  });

  test('ログイン成功 - 正しい認証情報で/itemsにリダイレクト', async ({ page }) => {
    // ユーザー名入力
    await page.getByLabel('ユーザー名').fill('root');

    // パスワード入力
    await page.getByLabel('パスワード').fill('pass');

    // ログインボタンをクリック
    await page.getByRole('button', { name: 'ログインする' }).click();

    // /itemsページへのリダイレクトを確認
    await expect(page).toHaveURL('/items');

    // 商品一覧画面のタイトルを確認
    await expect(page.getByRole('heading', { name: 'Items管理アプリ' })).toBeVisible();
  });

  test('ログイン失敗 - 間違った認証情報でエラーメッセージ表示', async ({ page }) => {
    // 間違ったユーザー名入力
    await page.getByLabel('ユーザー名').fill('wronguser');

    // 間違ったパスワード入力
    await page.getByLabel('パスワード').fill('wrongpass');

    // ログインボタンをクリック
    await page.getByRole('button', { name: 'ログインする' }).click();

    // エラーメッセージを確認
    await expect(page.getByText('ユーザー名かパスワードが間違っています')).toBeVisible();

    // ログインページに留まることを確認
    await expect(page).toHaveURL('/login');
  });

  test('未認証状態で/itemsにアクセス - エラー表示', async ({ page }) => {
    // ログインせずに/itemsに直接アクセス
    await page.goto('/items');

    // エラーメッセージが表示されることを確認（React Queryのリトライを考慮して待機時間を延長）
    await expect(page.getByText('エラーが発生しました')).toBeVisible({ timeout: 10000 });
  });

  test('必須フィールドの検証 - required属性の確認', async ({ page }) => {
    // HTML5バリデーションにより、空欄ではsubmitできないことを確認
    await expect(page.getByLabel('ユーザー名')).toHaveAttribute('required');
    await expect(page.getByLabel('パスワード')).toHaveAttribute('required');
  });
});
