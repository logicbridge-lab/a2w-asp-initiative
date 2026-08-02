# A2W/ASP Public Repository Structure

## Repository Layout

The public repository is organized around the five implementation phases and the supporting infrastructure for releases and community contribution.

The top-level directories are spec for schema and standard documents, crawler for the polite crawl implementation, extractor for the structural extraction pipeline and ASP Draft generator, benchmark for task definitions, agent harness, and metric computation, releases for release packaging scripts and historical release metadata, examples for example ASP drafts and sample task sets, docs for user-facing documentation and guides, and tools for shared utilities used across phases.

Within spec, the directory contains schema.json as the master ASP schema definition in JSON Schema format, standard.md as the human-readable A2W standard document, and changelog.md tracking schema version changes and breaking modifications.

Within crawler, the directory contains src/ with the crawl implementation, policies/ with robots.txt handling and rate limit defaults, config/ with a sample target list and configuration examples, and tests/ with crawl behavior tests.

Within extractor, the directory contains src/ with the extraction pipeline and ASP Draft generator, model/ with model configuration and quantized model artifacts where applicable, templates/ with JSON templates for ASP Drafts, confidence/ with threshold configuration and calibration tests, and tests/ with extraction regression tests.

Within benchmark, the directory contains src/ with the harness and metrics modules, tasks/ with JSONL task definitions, agents/ with reference agent integrations, reports/ with benchmark report templates, and tests/ with benchmark reproducibility tests.

Within releases, the directory contains packaging/ with compression, manifest, and checksum tooling, schema/ with schema snapshots included in each release, and ci/ with CI workflow definitions for automated release builds.

Within examples, the directory contains asp_drafts/ with example inferred Drafts and authored profiles, target_lists/ with example domain lists for crawl jobs, and sample_tasks/ with example benchmark task definitions.

Within docs, the directory contains contributing.md with contribution guidelines, runbook.md with operational instructions for running the pipeline locally, release_guide.md with instructions for preparing and publishing a release, schema_guide.md with instructions for reading and writing ASP documents, and governance.md describing decision-making, issue triage, and maintainer responsibilities.

Within tools, the directory contains shared Python modules for logging, catalog access, artifact management, and JSON Schema validation used across crawler, extractor, benchmark, and releases.

## Branching and Tagging Strategy

The main branch holds the current stable schema, reference code, and documentation. Phase branches, such as phase1-crawler and phase2-extractor, hold in-progress work for each implementation phase and are merged to main when the phase is complete. Release tags follow the pattern vYYYY-MM.N where N is the patch number within a monthly release series. The first release in a month is suffixed .0 and subsequent patch releases increment the suffix.

## Issue and PR Workflow

Issues are categorized with labels for schema, crawler, extractor, benchmark, release, docs, and community. Schema changes require a proposal document posted as a GitHub issue and a minimum one-week community comment period before merge. Code changes require tests that reproduce the reported behavior or feature. Release issues track release readiness and must pass a checklist before merging. Bug reports must include a minimal reproducible example, the affected release version, and the expected versus actual behavior. Feature requests must include a use case description and an example of the desired ASP or behavior.

## Community Contribution Path

New contributors are directed to the documentation, beginning with an overview of A2W/ASP, then to good first issues labeled for small self-contained improvements, and then to the contributor guide for larger contributions. Contributions to the schema require discussion before implementation to avoid divergent drafts. Contributions to crawler or extractor require tests and a sample of affected ASP output. Contributions to benchmark tasks require verification predicates and a sample run showing pass or fail under both conditions.

## Code of Conduct and Governance

The repository follows a standard contributor code of conduct. Maintainers are nominated from active contributors and confirmed by existing maintainers. Schema changes require maintainer approval after the community comment period. Release approval requires at least one maintainer sign-off on the release manifest and benchmark summary. Disputes about direction or inclusion are escalated to a council of three maintainers elected annually by the contributor community.
