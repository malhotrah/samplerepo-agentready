# Frontend (frontend/) — Agent Rules

Supplements the root `AGENTS.md`. Full picture: `docs/architecture.md#frontend`.

## Component Organization (strict naming conventions)

Source of truth: `frontend/app/components/README.md`.

- **Domain Components** (`components/Domain/`): Feature-specific, prefix with domain (e.g., `AdminDashboard`)
- **Global Components** (`components/global/`): Reusable primitives, prefix with `Base` (e.g., `BaseButton`)
- **Layout Components** (`components/Layout/`): Layout-only, prefix with `App` if props or `The` if singleton
- **Page Components** (`components/` with page prefix): Last resort for breaking up complex pages

## API Client Pattern

- API clients in `frontend/app/lib/api/` extend `BaseAPI`, `BaseCRUDAPI`, or `BaseCRUDAPIReadOnly` (`lib/api/base/base-clients.ts`)
- Clients are aggregated in `lib/api/client-user.ts`, `client-admin.ts`, `client-public.ts`
- Types imported from auto-generated `frontend/app/lib/api/types/` (DO NOT EDIT MANUALLY — run `task dev:generate`)
- Composables in `frontend/app/composables/` for shared state and API logic (e.g., `use-mealie-auth.ts`)
- Use `useAuthBackend()` for authentication state, `useMealieAuth()` for user management

```typescript
const api = useUserApi();
const recipe = await api.recipes.getOne(recipeId);
```

## State Management

- Nuxt 4 composables for state (no Vuex)
- Auth state via `use-mealie-auth.ts` composable
- Prefer composables over global state stores and over inline duplication

## Rules

1. **Run code generation after backend schema changes:** `task dev:generate`
2. **TypeScript strict mode:** All code must pass type checking; no new `any`
3. **Translations:** Only modify `en-US` files under `frontend/app/lang/` when adding new strings - other locales are managed via Crowdin and **must never be modified** (PRs modifying non-English locales will be rejected)
4. **Verify:** `task ui:test` (fast) or `task ui:check` (lint + test)
