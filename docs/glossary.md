# Glossary

Mealie's domain vocabulary, and where each term lives in the code. **Scope** says which tenant boundary filters the data (see [architecture.md §3](architecture.md#3-multi-tenancy)).

| Term | Meaning | Scope | Code |
|------|---------|-------|------|
| **Group** | The top-level tenant, e.g. "Home". It owns shared vocabulary (foods, units, tags…) and contains households | — | `db/models/group/group.py`, `routes/groups/` |
| **Household** | A sub-tenant inside a group. It owns recipes, meal plans and shopping lists. Every user belongs to exactly one | group | `db/models/household/household.py`, `routes/households/` |
| **User** | A login identity. Has a `group_id` and a `household_id`, plus per-user ratings and favorites | group | `db/models/users/`, `routes/users/` |
| **Admin** | A server-wide superuser. Admin controllers bypass tenant scoping | — | `routes/admin/`, `BaseAdminController` |
| **Recipe** | The core entity. It belongs to a household but other households in the same group can read it. Looked up by **slug** or id | household (write) / group (read) | `db/models/recipe/recipe.py`, `routes/recipe/`, `services/recipe/` |
| **Slug** | The URL-safe unique name of a recipe within a group | — | `PK_SLUG` in `repos/repository_factory.py` |
| **Organizers** | The umbrella term for **Categories**, **Tags** and **Tools** used to classify recipes | group | `routes/organizers/`, `db/models/recipe/{category,tag,tool}.py` |
| **Food / Unit** | Normalised ingredient vocabulary (e.g. "flour", "cup"), used by the parser and for scaling and shopping lists | group | `repos/repository_foods.py`, `repository_units.py`, `routes/unit_and_foods/` |
| **Ingredient parser** | Turns "2 cups flour" into quantity, unit and food. Options are NLP, brute force or OpenAI | — | `services/parser_services/`, `routes/parser/` |
| **Labels (multi-purpose)** | Colour-coded labels that group foods into shopping-list sections | group | `routes/groups/controller_labels.py` |
| **Cookbook** | A saved, filtered view of recipes (a query filter with a name) | household | `routes/households/controller_cookbooks.py` |
| **Meal plan** | Recipes or notes assigned to dates | household | `routes/households/controller_mealplan.py` |
| **Meal plan rules** | Rules that drive random meal-plan suggestions (by day, type, tags or categories) | household | `controller_mealplan_rules.py`, `repos/repository_meal_plan_rules.py` |
| **Shopping list** | A checklist of items, optionally built from recipes, and grouped by label | household | `controller_shopping_lists.py`, `repos/repository_shopping_list.py` |
| **Recipe actions** | User-defined links or POSTs triggered from a recipe page | household | `controller_group_recipe_actions.py` |
| **Timeline events** | A per-recipe activity log (made, edited, commented…) | group | `routes/recipe/timeline_events.py` |
| **Share token** | A public, expiring link to a single recipe | group | `routes/recipe/shared_routes.py` |
| **Explore** | Public, unauthenticated browsing of a group or household that has been made public | public | `routes/explore/`, `BasePublicGroupExploreController` |
| **Notifiers / Webhooks** | Outbound notifications (Apprise URLs or webhooks) driven by the event bus | household | `services/event_bus_service/`, `controller_group_notifications.py`, `controller_webhooks.py` |
| **Migrations (data)** | Importers from other apps (Paprika, Tandoor, Nextcloud…). These are **not** DB migrations | group | `services/migrations/`, `routes/groups/controller_migrations.py` |
| **Alembic migration** | A DB schema migration | — | `mealie/alembic/`, `task py:migrate` |
| **Seeder** | Loads the default foods, units and labels for a locale | group | `services/seeder/`, `repos/seed/` |
| **Query filter** | The filter language behind the `queryFilter=` param, used by cookbooks and search | — | `services/query_filter/` |
| **AI providers** | Per-group OpenAI-compatible configuration for parsing and recipe creation | group | `routes/groups/controller_group_ai_providers.py`, `services/openai/` |
