# ASP Schema Reference

The canonical schema is [`spec/schema.json`](../../spec/schema.json). It requires eleven top-level fields: `domain`, `owner`, `version`, `scope`, `resources`, `actions`, `policies`, `workflows`, `auth`, `evidence`, and `observability`.

`domain` binds a profile to one host. `owner` identifies its publisher. `resources` describe machine-usable surfaces; `actions` declare named capabilities and their preconditions. `policies` contain rate, authentication, data-use, and prohibition rules. `workflows` compose actions but do not replace action-level checks. `auth` documents required authentication, never credentials. `evidence` distinguishes owner-published from inferred profiles. `observability` identifies optional status and feedback surfaces.

Required fields ensure a profile has a predictable shape. An intentionally unsupported capability is represented by an empty array or object rather than by omitting a required field. A profile must not use an empty `domain`, fabricated owner, or speculative action.

See [examples](../../examples/) for complete profiles. The normative processing requirements are in the [protocol](../../spec/a2w-protocol.md), not this reference.
