# A2W/ASP Initiative — LogicBridge

Agent-to-Web (A2W) and Agentic Site Profile (ASP) are an open-standard and open-corpus initiative by LogicBridge to make the web more legible, safe, and efficient for autonomous agents.

## Vision

A2W is an open standard for structured interaction between autonomous agents and websites. ASP is a site-level profile that declares identity, resources, actions, policies, and evidence. Long term, domains publish an ASP alongside their human site, ideally under `/.well-known/`, so agents can use a domain-controlled, machine-readable interface instead of scraping human pages.

## What This Repository Contains

This repository currently contains the A2W/ASP research and strategy corpus, the machine-readable ASP JSON Schema, an example inferred ASP Draft, a Month One candidate domain list, benchmark and release specifications, and an asset-validation workflow. Crawler, extraction, benchmark-agent, and release implementations are planned but not yet present.

## Status

This is an early-stage initiative. The core artifacts are `a2w-asp-research-report.md`, `a2w_asp_scientific_paper_of_intent.md`, `a2w_asp_initiative_corpus.md`, `hermes_org_a2w_brief.md`, and `hermes_pmdev_a2w_brief.md`. The canonical schema is `spec/schema.json`; it validates `examples/example-asp-draft.json` in CI.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Do not crawl, publish, or submit data that violates a domain's robots.txt, terms of access, or applicable law.

## License

Apache-2.0 — see [LICENSE](LICENSE) for details.

This initiative is led by LogicBridge, a Toronto-based AI lab building small, quantized, domain-specific models and trusted workflow tools for Canadian SMEs.
