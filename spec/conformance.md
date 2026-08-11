# A2W/ASP Conformance

**Draft 0.1.0**

## Levels

A **Profile Publisher** passes when it serves a valid, domain-matching ASP at `/.well-known/asp` with HTTPS and `application/json` content type.

A **Profile Consumer** passes when it discovers the well-known path, validates JSON and schema, rejects domain mismatch and unsupported major schema versions, applies scope, and treats all discovery or validation failures as no profile.

An **Action-Aware Consumer** passes Profile Consumer requirements and additionally enforces hard policies, checks preconditions, and requires confirmation for material side effects without prior task-scoped authority.

## Required test cases

Every implementation claiming a level must pass the fixtures in `tests/fixtures/`:

- a valid owner-published profile;
- a valid profile with an empty status endpoint;
- malformed JSON;
- a profile whose `domain` does not match its origin;
- a profile that declares a hard prohibition;
- a profile that declares authenticated access.

A conformant implementation returns a deterministic pass or fail for each case. A schema-valid document alone does not establish protocol conformance.

## Result format

A test runner SHOULD emit JSON containing the implementation name, claimed level, protocol version, test identifier, result (`pass` or `fail`), and a short reason. A runner MUST fail its process if any required case fails.

## Non-goals

This draft does not score browser automation skill, site usability, model quality, crawling behavior, or task completion. Those are benchmark concerns and must not be represented as protocol conformance.
