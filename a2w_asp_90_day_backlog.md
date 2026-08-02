# A2W/ASP — 90-Day Development Backlog

## Backlog Overview

This backlog covers the first 90 days of active development on the A2W/ASP initiative. It is organized into five epics aligned with the implementation phases: Foundation, Crawler, Extraction, Benchmarking, and Release Infrastructure. Each epic contains stories with acceptance criteria and rough effort sizing. The backlog is ordered by dependency, not priority: Foundation must precede Crawler, Crawler must precede Extraction, and Extraction must precede Benchmarking.

## Effort Key

XS is a few hours to half a day. S is one to two days. M is three to five days. L is a week or more.

## Epic 1 — Foundation and Repository Setup

The Foundation epic establishes the public repository, development environment conventions, CI baseline, and core shared utilities. Nothing else can proceed until this epic is complete.

The first story sets up the public repository. Create the GitHub repository with the planned directory structure, populate initial files including README, CODE_OF_CONDUCT, CONTRIBUTING, and LICENSE placeholders, and protect the main branch with required status checks. Acceptance criteria are a public repo with matching structure, branch protection enabled, and all initial documentation placeholders in place. Effort is S.

The second story defines the core package and tooling. Set up Python project packaging with pyproject.toml, configure linting with ruff or equivalent, set up type checking with mypy or pyright, and define pre-commit hooks for formatting and static analysis. Acceptance criteria are a clean install, lint and type check passing locally, and pre-commit hooks active. Effort is S.

The third story builds shared artifact utilities. Implement an artifact store module that handles reading, writing, and checksumming crawl artifacts and ASP Drafts, and a catalog module that wraps the SQLite or DuckDB metadata database. Acceptance criteria are unit tests covering basic read, write, and checksum verification, and successful local demo of the modules. Effort is M.

The fourth story sets up CI baseline. Configure GitHub Actions to run lint, type checks, and unit tests on every push and PR, and add a status badge to the README. Acceptance criteria are green checks on the main branch and badge displaying correctly. Effort is S.

Epic 1 total effort is approximately two to three weeks with one full-time engineer.

## Epic 2 — Crawler and Capture

The Crawler epic delivers the Phase I crawler with robots-aware polite fetching, raw artifact storage, and a working CLI.

The first story implements the crawl loop. Build the crawler module using Scrapy or equivalent, implement robots.txt parsing and enforcement, implement domain-specific rate limiting, and support configurable target lists from the catalog. Acceptance criteria are a successful crawl of a small allowlist of domains under rate limit, robots.txt enforced, and no duplicate fetches on rerun. Effort is L.

The second story adds headless screenshot capture. Integrate Playwright for optional screenshot capture, add a toggle to the crawl configuration to enable or disable screenshots, and store screenshots alongside HTML artifacts per URL. Acceptance criteria are screenshots captured and stored correctly for a sample domain, and the toggle disabling capture without affecting crawl operation. Effort is M.

The third story implements artifact storage and catalog integration. Write crawl artifacts to the artifact store with compression, write metadata sidecars for each fetched URL, and update the catalog with crawl status for each target domain. Acceptance criteria are all artifacts findable by URL and domain, catalog status accurate for successful, failed, and skipped fetches, and idempotent rerun. Effort is M.

The fourth story builds the crawl CLI. Wrap the crawler in a command-line interface with subcommands for running a crawl, checking status, and listing completed domains for a release. Acceptance criteria are a working CLI help text, successful run against a test target list, and status command showing accurate counts. Effort is S.

Epic 2 total effort is approximately three to four weeks with one full-time engineer, assuming Epic 1 is complete.

## Epic 3 — Structural Extraction and ASP Draft Generation

The Extraction epic delivers the Phase II extraction pipeline, model-assisted classification, and ASP Draft generation with confidence and evidence.

The first story implements heuristic page classification. Build a module that classifies crawled pages as homepage, listing, detail, search, checkout, account, or documentation based on URL structure, heading patterns, form presence, and link density. Acceptance criteria are classification assignments for a sample of crawled pages, with output saved to a feature file per page. Effort is M.

The second story integrates model-assisted classification. Connect the quantized small model to the pipeline, load page feature vectors from the heuristic stage, produce structured predictions for page purpose, candidate actions, and form semantics, and attach confidence scores to each prediction. Acceptance criteria are model predictions for a sample domain, confidence scores populated, and predictions saved to a structured output file per page. Effort is L.

The third story builds the ASP Draft generator. Compile the classified evidence into an ASP Draft per domain, apply confidence thresholds to decide whether to populate or mark unknown for each ASP field, link every populated field to its evidence references, and write the Draft to the artifact store. Acceptance criteria are one complete ASP Draft per sample domain, unknown fields visibly marked, evidence references resolvable to crawl artifacts, and Draft valid against the ASP schema. Effort is M.

The fourth story adds extraction regression tests. Build a test fixture with a small set of known crawled pages and expected ASP Drafts, run the pipeline end to end over the fixture, and assert that Drafts match expected values within tolerance. Acceptance criteria are tests passing on every push to main, and the fixture covering at least one page of each classified type. Effort is M.

Epic 3 total effort is approximately four to five weeks with one full-time engineer, assuming Epic 2 is complete and crawl artifacts are available.

## Epic 4 — Benchmarking and Agent Harness

The Benchmarking epic delivers the Phase III benchmark harness, a pilot task set, and baseline raw web versus ASP-guided results.

The first story defines the pilot task set. Write six benchmark task definitions covering restaurant, government, e-commerce, clinic, documentation, and university site categories, each with a domain, goal, verification predicate, category, difficulty, and step budget. Acceptance criteria are six valid task JSON files, each with a passing verification predicate tested against a known end state. Effort is M.

The second story implements the sandboxed agent harness. Build a harness that loads a task, instantiates a Playwright browser session, runs a Myra or lightweight reference agent under raw web or ASP-guided configuration, logs every agent decision and browser action, and evaluates the verification predicate at task completion. Acceptance criteria are a successful raw web run on at least one pilot task, and a successful ASP-guided run on the same task, with complete event logs. Effort is L.

The third story implements metrics computation. Write a metrics module that consumes the harness event logs and computes task success rate, mean and median step count, mean and median latency, ambiguity event count, and policy violation count. Acceptance criteria are metrics computed correctly for a known run, with an aggregate summary matching manual calculation. Effort is M.

The fourth story runs the pilot benchmark. Execute the full pilot task set across the sample domains under both raw web and ASP-guided conditions, generate the baseline benchmark report, and publish results internally. Acceptance criteria are a completed benchmark report with aggregate metrics, individual task results, and raw event logs. Effort is M.

Epic 4 total effort is approximately four to five weeks with one full-time engineer, assuming Epic 3 is complete and ASP Drafts are available for pilot domains.

## Epic 5 — Release Infrastructure and Month One Release

The Release Infrastructure epic delivers the Phase IV packaging and automation tooling needed to produce the first monthly release.

The first story implements release packaging. Build a tool that collects crawl artifacts, ASP Drafts, benchmark results, and catalog snapshot into a release directory, compresses each artifact with gzip, computes SHA-256 checksums, and writes the manifest JSON. Acceptance criteria are a complete release directory for a sample month, all artifacts checksummed, manifest listing all artifacts and digest values, and reproducible unpack and re-checksum. Effort is M.

The second story configures CI release automation. Write a GitHub Actions workflow that triggers on a monthly schedule or manual dispatch, runs the packaging tool, creates a GitHub Release with the packaged artifacts, and publishes to object storage. Acceptance criteria are a successfully triggered test release, artifacts present on GitHub Releases, and workflow logs clean. Effort is L.

The third story builds the release verification gate. Add a CI job that validates ASP Draft conformance against the current schema, verifies benchmark result completeness, and checks release directory layout against the specification. Acceptance criteria are a failing CI build when provided with a deliberately malformed Draft or incomplete benchmark, and a passing build on the corrected sample release. Effort is M.

The fourth story packages the Month One release. Run the full pipeline end to end for the first monthly release, tag the repository with the release version, publish the release artifacts, update the README with release notes, and announce internally. Acceptance criteria are a tagged release on GitHub, downloadable release artifacts, README updated, and release notes summarizing contents. Effort is L.

Epic 5 total effort is approximately three to four weeks with one full-time engineer, assuming Epics 2 through 4 are complete.

## Cross-Cutting Stories

Schema Review and JSON Schema Document. Author a machine-readable JSON Schema document for the ASP schema, validate it against the example Draft, and publish it under spec/schema.json. Include a changelog section in the schema document. Acceptance criteria are a JSON Schema document that validates the example Draft, schema validation failing on a Draft with a missing required field, and changelog listing initial version. Effort is M.

Documentation and Onboarding. Write README updates for each phase, a contributor guide, a runbook for running the pipeline locally, and a schema guide for reading and writing ASP Drafts. Acceptance criteria are documentation files in the docs directory, contributor guide linked from the main README, and runbook verified by a new engineer following it to produce a local release. Effort is M.

Community Setup. Create GitHub issue and PR templates, label taxonomy, good first issues list, and a community calendar placeholder for monthly working group calls. Acceptance criteria are templates and labels visible in the repository, and good first issues list populated with at least three items. Effort is S.

## 90-Day Allocation

The following table maps epics and cross-cutting stories to calendar weeks for a single-engineer paced plan.

Weeks one through three cover Epic 1 Foundation and Epic 2 Story one Crawl Loop. Weeks four and five cover Epic 2 Story two Screenshots, Epic 2 Story three Storage and Catalog, and Epic 2 Story four CLI. Weeks six and seven cover Epic 3 Story one Heuristic Classification and Epic 3 Story two Model-Assisted Classification. Week eight covers Epic 3 Story three ASP Draft Generator and Epic 3 Story four Regression Tests. Week nine covers Epic 4 Story one Task Set and Epic 4 Story two Agent Harness. Week ten covers Epic 4 Story three Metrics and Epic 4 Story four Pilot Benchmark Run. Weeks eleven and twelve cover Epic 5 Story one Packaging, Epic 5 Story two CI Automation, and Epic 5 Story three Verification Gate. Week thirteen covers Epic 5 Story four Month One Release and the cross-cutting Schema Review, Documentation, and Community Setup stories.

## Risks and Mitigations

Crawl scope or target list delays can block extraction and benchmarking. Mitigation is to fix a minimum viable crawl target list of twenty to fifty domains in week one and treat expansion as a week two task rather than a blocking dependency.

Model selection or integration delays can block extraction. Mitigation is to begin with a pure heuristic extraction baseline and treat model integration as an upgrade in week six, keeping extraction functional throughout.

Benchmark design complexity can extend the harness build. Mitigation is to lock the six pilot tasks in week eight and treat additional tasks or categories as follow-on work.

Release tooling polish can delay publication. Mitigation is to accept a minimal viable release in week thirteen and treat packaging and automation improvements as ongoing refinements after the first release.

## Definition of Done for 90 Days

By day ninety, the initiative should have a public repository with passing CI, a working crawler that can fetch and archive a target domain list, an extraction pipeline that produces ASP Drafts with confidence and evidence for those domains, a benchmark harness with a pilot task set and baseline results, and a published Month One release with crawl artifacts, ASP Drafts, benchmark results, and schema documentation. The work should be demonstrated to internal stakeholders and announced to the community as a working open-source project.
