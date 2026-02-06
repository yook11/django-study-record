# Project Guidelines for Django Ninja + React + Playwright

## 🧠 Core Behavior Rules
1.  **Search First Strategy**:
    - For libraries that evolve quickly (Django Ninja v1+, TanStack Query v5, Playwright 1.40+), **ALWAYS search the web/documentation first** to verify the latest syntax.
    - Do not rely on training data older than 2025.
    - Use "1 Yes" to search prompts without asking for confirmation.

2.  **Context Awareness (IMPORTANT)**:
    - Detailed project rules (Architecture, Testing Strategy, DB) are located in the `.context/` directory.
    - **ALWAYS** refer to `.context/TESTING.md` before writing tests.
    - If unsure about the architecture, check `.context/ARCHITECTURE.md`.

3.  **Security First**:
    - **HttpOnly Cookies** are mandatory for authentication.
    - Never store sensitive tokens in LocalStorage.
    - Ensure CSRF protection is considered for API endpoints.

4.  **Modern Django Standards (Django 6.0+)**:
    - **Native Async ORM**: Use `acreate`, `asave`, `adelete`, `acount`, `aget_object_or_404`, and async iteration.
    - **Prohibited**: Do NOT use `sync_to_async` wrapper for DB operations; use native async APIs instead.
    - **Auth**: JWT authentication supports both Cookie (priority) and Bearer token.

## 🛠 Tech Stack & Coding Style

### Project Structure
- **Monorepo**:
    - `/myproject`: Backend (Django)
    - `/frontend`: Frontend (React + Vite)
    - `.context/`: Documentation & Rules
- **API Types**: Auto-generated via `openapi-typescript`.
    - Command: `npx openapi-typescript http://localhost:8000/api/openapi.json -o src/api/schema.d.ts` (Run in `/frontend`)

### Backend (Django Ninja)
- Use **Async** views by default (`async def`).
- Use `Schema` for all request/response models.
- Avoid DRF (Django REST Framework) patterns; stick to Ninja's patterns.
- Implement **Limit/Offset Pagination** for list endpoints using `acount()` and slicing.

### Frontend (React + TypeScript)
- Use **TanStack Query v5** for data fetching.
- Use `openapi-fetch` or generated clients for type safety.
- **Strict Mode**: No `any` types. Define interfaces properly.
- **Components**: Functional components with Hooks.

### Testing Standards (Strict Rules)
Ref: `.context/TESTING.md`

- **E2E (Playwright)**:
    - **Execution**: Use `fullyParallel: false` and `workers: 1` in config to avoid DB conflicts.
    - **DB Reset Strategy**: MUST call `POST /api/test/reset-db` in `test.beforeEach` to ensure a clean state.
    - **Deterministic Data**:
        - Since DB is reset, do NOT use timestamps/unique IDs for test data.
        - Verify counts using **absolute values** (e.g., `expect(count).toBe(1)`).
    - **No Flakiness**:
        - ❌ `page.waitForTimeout(5000)` is **STRICTLY PROHIBITED**.
        - ✅ Use `page.waitForResponse` or `expect().toBeVisible()` instead.
    - **Selectors**: Use `getByRole`, `getByLabel` (User-facing). Avoid CSS/XPath.
    - **Auth Optimization**: Use `storageState` (Global Setup) to avoid re-login.
        - Path: `playwright/.auth/user.json`
    - **Debugging Config (playwright.config.ts)**:
        - `trace: 'retain-on-failure'`
        - `screenshot: 'only-on-failure'`
    - **CI Parallelism**: Use `--shard=N/M` for large test suites.

- **Backend (Pytest)**:
    - Use `@pytest.mark.django_db(transaction=True)` for async tests.
    - Use `async_client` fixture from `conftest.py`.

### CI/CD Guidelines
- **Optimization**: Use **path filters** to run tests only when relevant files change.
- **Performance**: Separate lint/test jobs for parallel execution.
- **Caching**: Cache uv, npm, and Playwright browsers.
- **Integration**: Run E2E tests with the Django backend running in CI.

## 📝 General
- When fixing bugs, analyze the root cause first before suggesting code.
- If a file is long, output only the modified sections with clear context markers.

## 🛠️ Useful Commands
- **Load Context**: `cat .context/*.md`
- **Run Backend**: `uv run python manage.py runserver`
- **Run E2E**: `npx playwright test --ui` (in `frontend/`)
- **Reset DB**: `curl -X POST http://localhost:8000/api/test/reset-db`
