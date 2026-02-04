# Project Guidelines for Django Ninja + React + Playwright

## 🧠 Core Behavior Rules
1.  **Search First Strategy**:
    - For libraries that evolve quickly (Django Ninja v1+, TanStack Query v5, Playwright 1.40+), **ALWAYS search the web/documentation first** to verify the latest syntax.
    - Do not rely on training data older than 2025.
    - Use "1 Yes" to search prompts without asking for confirmation.

2.  **Security First**:
    - **HttpOnly Cookies** are mandatory for authentication.
    - Never store sensitive tokens in LocalStorage.
    - Ensure CSRF protection is considered for API endpoints.

3.  **Modern Django Standards (Django 6.0+)**:
    - **Native Async ORM**: Use `acreate`, `asave`, `adelete`, `acount`, `aget_object_or_404`, and async iteration.
    - **Prohibited**: Do NOT use `sync_to_async` wrapper for DB operations; use native async APIs instead.
    - **Auth**: JWT authentication supports both Cookie (priority) and Bearer token.

## 🛠 Tech Stack & Coding Style

### Project Structure
- **Monorepo**:
    - `/myproject`: Backend (Django)
    - `/frontend`: Frontend (React + Vite)
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

### Testing Standards
- **E2E (Playwright)**:
    - Use `fullyParallel: false` and `workers: 1` in config to avoid DB conflicts.
    - **Isolation**: Use unique test data (e.g., timestamps) for every test run.
    - **Verification**: Verify counts using **relative values** (e.g., `countBefore + 1`).
    - Use `beforeEach` for setup and unique identifiers for cleanup.
- **Backend (Pytest)**:
    - Use `@pytest.mark.django_db(transaction=True)` for async tests.
    - Use `async_client` fixture from `conftest.py`.

### CI/CD Guidelines
- **Optimization**: Use **path filters** to run tests only when relevant files change.
- **Performance**: Separate lint/test jobs for parallel execution.
- **Caching**: Cache uv, npm, and Playwright browsers.
- **Integration**: Run E2E tests with the Django backend running in the CI environment.

## 📝 General
- When fixing bugs, analyze the root cause first before suggesting code.
- If a file is long, output only the modified sections with clear context markers.