# セキュリティアーキテクチャ

## CSRF 防御方針: SameSite Cookie + CORS

本プロジェクトでは **CSRF トークンフローを使用しない**。代わりに以下の組み合わせで防御する。

### なぜ CSRF トークンを使わないのか
1. **Django Ninja は全 API ビューを `csrf_exempt` にする**（フレームワークの設計方針）
2. `NinjaExtraAPI(csrf=True)` は **非推奨**（将来削除予定）
3. SPA + Cookie 認証で CSRF トークンフローを実装するには、専用エンドポイント (`/csrf-token`) とフロントエンドの全リクエストへの `X-CSRFToken` ヘッダー追加が必要で、複雑さに対してセキュリティ上の利点がない

### 防御の仕組み
| 層 | 設定 | 防御内容 |
|---|---|---|
| **SameSite=Lax** | `AUTH_COOKIE_SAMESITE: "Lax"` | 外部サイトからの POST/PUT/DELETE で Cookie を送信しない |
| **CORS** | `CORS_ALLOWED_ORIGINS` | 許可されたオリジン以外からのリクエストをブロック |
| **HttpOnly** | `AUTH_COOKIE_HTTP_ONLY: True` | JavaScript から Cookie を読み取れない（XSS 対策） |
| **Secure** | `AUTH_COOKIE_SECURE: IS_PRODUCTION` | 本番では HTTPS 経由のみ Cookie を送信 |

### 前提条件
- 全ての状態変更 API は POST/PUT/DELETE を使用（GET は状態変更しない）
- `SameSite=Lax` は GET のみ外部サイトからの Cookie 送信を許可する

## Cookie ドメイン設定

### AUTH_COOKIE_DOMAIN の挙動
| 設定値 | Cookie 送信範囲 |
|---|---|
| `None`（デフォルト） | Cookie を設定したホストのみ。最も安全 |
| `example.com` または `.example.com` | `example.com` とそのサブドメイン全て（先頭ドットは現在のブラウザでは無視されるため同じ挙動） |

**推奨**: サブドメイン間で Cookie を共有する必要がなければ `None` のまま。

## リバースプロキシ使用時の注意

本番で Nginx / Cloudflare 等のリバースプロキシの背後に Django を配置する場合:

1. **`SECURE_PROXY_SSL_HEADER`** の設定が必須
   - プロキシが `X-Forwarded-Proto: https` ヘッダーを付与することを前提
   - これがないと `SECURE_SSL_REDIRECT` が無限リダイレクトを起こす
2. プロキシ側で `X-Forwarded-Proto` ヘッダーを正しく設定する必要がある
3. 信頼できないプロキシが `X-Forwarded-Proto` を偽装すると、Django が HTTPS と誤認する危険があるため、プロキシの設定を確認すること

## 本番環境変数

| 変数名 | 必須 | 例 | 説明 |
|---|---|---|---|
| `DJANGO_ENV` | Yes | `production` | `production` で本番モード有効化 |
| `DJANGO_SECRET_KEY` | Yes | `<ランダム文字列>` | 未設定で即 `KeyError` |
| `DJANGO_ALLOWED_HOSTS` | Yes | `myapp.example.com` | カンマ区切りで複数可 |
| `CORS_ORIGINS` | Yes | `https://myapp.example.com` | カンマ区切りで複数可 |
| `CSRF_TRUSTED_ORIGINS` | Yes | `https://myapp.example.com` | Django admin に必須 |
| `AUTH_COOKIE_DOMAIN` | No | `None` 推奨 | サブドメイン共有時のみ設定 |
| `DATABASE_URL` | Yes | `postgres://user:pass@db/mydb` | `dj-database-url` 形式 |

## セキュリティチェックリスト

- [x] HttpOnly Cookie で JWT を保存（LocalStorage 禁止）
- [x] SameSite=Lax で CSRF 防御
- [x] CORS を許可オリジンのみに制限
- [x] 本番で SECRET_KEY を環境変数から取得（ハードコード禁止）
- [x] 本番で DEBUG=False
- [x] 本番で Secure Cookie（HTTPS のみ）
- [x] HSTS 有効化（1年、サブドメイン含む、preload）
- [x] X-Frame-Options: DENY
- [x] SSL リダイレクト + プロキシヘッダー対応
- [x] ALLOWED_HOSTS を明示的に設定
- [x] set_cookie と delete_cookie で domain を統一
