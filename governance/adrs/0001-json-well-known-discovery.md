# ADR 0001: JSON at `/.well-known/asp`

## Status
Accepted for Draft 0.1.

## Decision
A2W discovery uses HTTPS `GET /.well-known/asp` and a JSON ASP document.

## Rationale
A well-known path is easy for site owners to host and for clients to discover. JSON is directly consumable by browsers, agents, and existing tooling. Draft 0.1 avoids defining a new action transport or identity protocol.

## Consequences
A2W remains an additive discovery layer. Sites retain their existing APIs and authorization systems. Future formats or discovery locations require a versioned protocol proposal.
