# mundane-cards

*No dragons. No spells. Just Tuesday.*

The card library for [Mundane](https://github.com/letsbuilda/mundane). Cards are **data**: they are
published here as JSON **sets** under [`sets/`](./sets), curated by pull request. Card **behavior**
(effects) lives in the engine ([`mundane-backend`](https://github.com/letsbuilda/mundane-backend)),
not here — a card names an effect from the engine's fixed vocabulary; it cannot define new behavior.

## Sets

Each file in [`sets/`](./sets) is one set. The current set is [`sets/core.json`](./sets/core.json).

A set file looks like this:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "set_id": "core",
  "name": "Core Set",
  "version": "1.0.0",
  "cards": [
    {
      "id": "throw_a_house_party",
      "name": "Throw a House Party",
      "cost": 3,
      "type": "task",
      "effect": "damage_composure",
      "params": { "amount": 3 },
      "text": "Deal 3 chaos to your opponent's Composure."
    }
  ]
}
```

| Field     | Meaning |
|-----------|---------|
| `set_id`  | Namespace for the set (`^[a-z0-9_]+$`). |
| `name`    | Human-readable set name. |
| `version` | Semver (`1.0.0`) or an ISO-8601 date (`2026-05-31`). |
| `cards`   | The cards (non-empty). |

Each card has `id` (`^[a-z0-9_]+$`), `name`, `cost` (≥ 0), `type` (`person` · `appliance` · `habit` ·
`task` · `instant`), `effect`, optional `params` (default `{}`), `text`, and optional `flavor`. No
other fields are allowed, so a typo like `txet` fails CI loudly.

The full, normative format is documented in the meta repo:
[specs/card-sets.md](https://github.com/letsbuilda/mundane/blob/main/specs/card-sets.md), and the
machine-checkable contract is
[schemas/card-set.schema.json](https://github.com/letsbuilda/mundane/blob/main/schemas/card-set.schema.json)
(a pinned copy is vendored here at [`schema/card-set.schema.json`](./schema/card-set.schema.json)).

### Effects are names, not code

`effect` is a **string** naming an effect from the engine's vocabulary; `params` is passed to it. The
engine resolves the name to code at load time and rejects unknown names or invalid params. Permanents
(`person`, `appliance`, `habit`) have no on-resolve effect — use `"effect": "none"`. The current
vocabulary includes:

| Effect             | Params              | What it does                                  |
|--------------------|---------------------|-----------------------------------------------|
| `damage_composure` | `{ "amount": int }` | Deal `amount` to the opponent's Composure.    |
| `counter_task`     | `{}`                | Counter the targeted task on the stack.       |
| `none`             | `{}`                | No effect (used by permanents).               |

The vocabulary is defined in the engine and grows there; this list mirrors it.

### Id namespacing

Cards carry **bare** ids. The backend composes the runtime id as `set_id:id` — e.g.
`throw_a_house_party` in set `core` becomes `core:throw_a_house_party`. Composed ids must be unique
across all sets; CI enforces this ([`scripts/check_unique_ids.py`](./scripts/check_unique_ids.py)).

## Adding a card (PR flow)

PRs are the curation and moderation layer — there is no registry service. To add or change a card:

1. Edit the appropriate file in [`sets/`](./sets) (or add a new set file). Give the card a unique
   bare `id` and an `effect` from the engine's vocabulary above.
2. Make sure it validates locally:

   ```sh
   uvx check-jsonschema --schemafile schema/card-set.schema.json sets/*.json
   python scripts/check_unique_ids.py
   ```

3. Open a pull request. CI re-runs both checks; a reviewer merges. The card's flavor is the fun part —
   keep `text`/`flavor` in character.

Adding a brand-new `effect` (new behavior) is a change to the **engine**, not this repo — open a PR
against [`mundane-backend`](https://github.com/letsbuilda/mundane-backend) first.

## Continuous integration

[`ci.yaml`](./.github/workflows/ci.yaml) validates every file in `sets/` against the vendored schema
and checks composed-id uniqueness on every push and pull request.

## License

Released under the [MIT License](./LICENSE).
