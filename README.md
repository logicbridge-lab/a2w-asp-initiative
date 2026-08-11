# A2W/ASP

**Agent-to-Web (A2W)** is a draft protocol for agents to discover a domain-controlled description of a website. An **Agentic Site Profile (ASP)** is that description: a JSON document declaring resources, actions, policies, authentication, evidence, and observability.

> **Status: Draft 0.1.0.** The schema, protocol, and conformance rules are public working drafts. They are not yet a stable standard and must not be represented as one.

## Start here

| I am… | Read… |
|---|---|
| A site owner | [Publish an ASP](docs/getting-started/site-owners.md) |
| An agent builder | [Consume an ASP](docs/getting-started/agent-builders.md) |
| An evaluator | [Conformance](spec/conformance.md) |
| A contributor | [Governance](governance/GOVERNANCE.md) and [contributing](CONTRIBUTING.md) |

## What A2W does

A2W defines a discovery convention for an ASP at `https://<domain>/.well-known/asp`. It does not grant access, bypass authentication, override robots.txt, replace an API, or authorize actions. The domain owner remains in control of what is published and what an agent may do.

## Core artifacts

- [Protocol specification](spec/a2w-protocol.md) — normative discovery and consumption behavior.
- [ASP JSON Schema](spec/schema.json) — canonical machine-readable Draft 0.1 schema.
- [Schema reference](docs/reference/schema.md) — field-level explanation.
- [Security and policy](spec/security.md) — mandatory safety expectations.
- [Conformance](spec/conformance.md) — implementation levels and pass/fail rules.
- [Examples](examples/) — profile fixtures for a public information site, a booking site, and an authenticated API.
- [Reference utilities](reference/) — local publisher and validator.
- [Status](docs/STATUS.md) — stable, draft, and planned material.

## Quick local check

```bash
python3 reference/asp_validator.py examples/public-information-site.json
python3 -m unittest discover -s tests -v
```

## Scope

A2W is an additive, domain-controlled web convention. Existing human-facing pages, APIs, robots.txt, authentication, and legal terms remain authoritative. If an ASP is absent, malformed, unavailable, or disallows a requested action, agents must follow the protocol fallback rules rather than infer permission.

## Research context

The original research and implementation planning corpus remains available in this repository for transparency. It is background material, not normative specification: [research report](a2w-asp-research-report.md), [paper of intent](a2w_asp_scientific_paper_of_intent.md), and [initiative corpus](a2w_asp_initiative_corpus.md).

## Contributing and releases

See [CONTRIBUTING.md](CONTRIBUTING.md), [versioning](governance/VERSIONING.md), [governance](governance/GOVERNANCE.md), and [the changelog](CHANGELOG.md). Contributions are Apache-2.0 licensed.

## License

Apache-2.0 — see [LICENSE](LICENSE).

A2W/ASP is initiated by LogicBridge, a Toronto-based AI lab building trusted workflow tools and domain-specific AI infrastructure.
