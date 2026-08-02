# A2W/ASP Architecture and Data Flow

## Overview

The A2W/ASP system is composed of four major subsystems: the Crawl subsystem, the Extraction subsystem, the ASP Registry, and the Benchmark and Release subsystem. These are connected by a shared artifact store and metadata catalog. The system is designed to run as a pipeline from raw web pages to published releases, with clear handoffs between phases and full reproducibility.

## System Components

### Crawl Subsystem
The Crawl subsystem is responsible for fetching pages from target domains and storing raw artifacts. It runs as a controlled batch job that reads a target domain list from the metadata catalog, applies domain-specific rate limits and robots.txt constraints, fetches HTML and optional screenshots, extracts lightweight metadata, and writes both into durable artifact storage. The crawl job emits status events back to the catalog: queued, in progress, completed, or failed. The crawl job is idempotent: rerunning against the same target list produces the same archive content without duplicate work.

### Extraction Subsystem
The Extraction subsystem reads raw crawl artifacts from the artifact store and performs structural classification. It runs heuristic-based page classification first to produce a feature vector for each page, then passes those features through a small quantized model to infer structured labels: page purpose, navigation elements, form semantics, candidate actions, and workflow hints. For each inferred element, the extraction job records a confidence score and an evidence reference pointing back to the original crawl artifact. The output of this subsystem is an ASP Draft for each domain, stored as a structured JSON document.

### Metadata Catalog
The Metadata Catalog is a single instance of DuckDB or SQLite that serves as the source of truth for all jobs and artifacts. It stores crawl targets and their statuses, domain mappings, release manifests, ASP Draft versions, confidence and evidence traces, benchmark task definitions, and benchmark results. Every other subsystem reads from and writes to this catalog. The catalog is committed to the repository as a versioned artifact at each release boundary so the full state of any historical release is recoverable.

### ASP Registry
The ASP Registry is a public-facing service that serves three functions: discovery, hosting, and verification. Discovery allows agents to query the latest canonical ASP for a domain by name or URL. Hosting provides storage and API access for domain-authored official ASPs. Verification checks that the ASP at a domain's /.well-known/asp path is authentic and matches the claimed owner. The registry also compares inferred Drafts with authored profiles and flags discrepancies for review.

### Benchmark Subsystem
The Benchmark subsystem defines tasks, runs agent trials under raw web and ASP-guided conditions, and records metrics. It loads task definitions from the catalog, executes each task twice per domain in a sandboxed browser environment, logs every action and state transition, computes metrics, and writes results back to the catalog. Results are summarized into aggregate reports for each release.

### Release Subsystem
The Release subsystem packages the crawl archive, ASP Drafts, benchmark results, and catalog snapshot into a versioned release directory, compresses and checksums the artifacts, generates a manifest, and publishes to the public repository and object storage. The release job runs on a fixed monthly cadence and is triggered automatically by the CI pipeline.

## Data Flow

The pipeline begins when the Crawl subsystem fetches pages from target domains and writes raw HTML, text, metadata, and optional screenshots to the artifact store. The catalog is updated with crawl completion events for each domain. Once all target domains have been crawled, the Extraction subsystem reads the catalog for completed crawl events, loads the raw artifacts, and produces ASP Drafts with confidence scores and evidence. Each ASP Draft is stored in the artifact store and registered in the catalog.

In parallel with extraction, the Benchmark subsystem reads task definitions from the catalog and executes agent trials against a sample of crawled domains under both conditions. Results are written back to the catalog as JSONL event logs and summarized metrics.

At the end of a release cycle, the Release subsystem reads the catalog snapshot, fetches the compiled crawl archive and ASP Drafts, retrieves benchmark results, generates the manifest, and publishes the release artifacts to public storage. The public repository is updated with the new release tag, schema documentation, and benchmark summary. The registry is updated with inferred Draft versions for each newly crawled domain.
