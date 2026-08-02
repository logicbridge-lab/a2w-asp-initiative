# A2W/ASP Technical Specification — Implementation Phases

## Phase I — Crawler and Capture

### Objective
Build a polite, robots-aware crawler that captures HTML, text, metadata, and optional screenshots from target domains. Output is organized as a versioned archive per domain per release.

### Technical Requirements
The crawler must respect robots.txt, throttle to a configurable requests-per-second limit with burst allowance, honor crawl-delay directives, and avoid re-crawling unchanged pages. It should support per-domain session isolation to prevent cookie and state leakage.

The crawler captures HTML body bytes, the rendered text extracted from the HTML, HTTP metadata including status, content type, and last-modified headers, DOM metadata such as title, meta tags, and link structure, and optional viewport screenshots using a headless browser. The raw capture output is stored per domain with timestamped release folders.

### Implementation Details
Use Python with Scrapy or a similar framework for the crawl loop. Headless screenshots use Playwright or Puppeteer via a Python wrapper. Raw HTML is stored as compressed WARC-style blobs. Extracted text and metadata are stored as JSON sidecars indexed by URL. A SQLite or DuckDB catalog tracks crawl state, URL frontier, and deduplication fingerprints.

### Deliverables
Crawl module with configuration file containing allowed domains, rate limit, and screenshot toggle. Archive format specification. Basic CLI to run a release crawl against a target list.

## Phase II — Structural Extraction

### Objective
Infer page purpose, navigation structure, form semantics, candidate actions, and evidence from the raw crawl artifacts. Generate ASP Drafts with confidence scores for every populated field.

### Technical Requirements
First, heuristic extraction classifies page type by analyzing URL structure, heading patterns, form presence, and link counts. Known patterns include homepage, listing, detail, search, checkout, account, and documentation. Then, a small quantized model fine-tuned on web pages and ASP schema labels performs the model-assisted classification with confidence scores. Evidence is attached to each classified element.

Each field in an ASP Draft is either populated from extracted evidence with an attached confidence, or marked as unknown if no evidence reached the confidence threshold.

### Implementation Details
The extraction pipeline runs as a batch job over the Phase I archive. Heuristics run first and produce a lightweight feature vector per page. The model refines the feature vector into structured predictions. Results are merged into an ASP Draft JSON document per domain. A SQLite catalog tracks per-field confidence and evidence references for the traceability requirement.

### Deliverables
Extraction pipeline, ASP Draft generator, confidence threshold configuration, evidence trace format, example Draft outputs.

## Phase III — Benchmarking

### Objective
Build a task harness comparing raw web versus ASP-guided navigation. Measure task success rate, step count, latency, ambiguity events, and policy violations.

### Technical Requirements
The benchmark harness defines tasks in JSON with a domain, a natural language goal, and a verification predicate. Each task is executed under two conditions. The raw web condition has no ASP available. The ASP-guided condition loads the inferred Draft for the domain and exposes resources, actions, policies, and workflows.

A reference agent implementation performs browser actions in both conditions. The harness logs every action, navigation step, ambiguity event, and policy violation. Results are serialized as JSONL for analysis.

### Implementation Details
The reference agent can be Myra or any lightweight Playwright-based browser agent. The harness loads the ASP Draft as context injected into the agent's planning step. The verification predicate checks whether the goal was achieved. Metrics are computed across a task set for aggregate comparison.

### Deliverables
Benchmark task definitions for pilot sites, harness runner, metrics computation, baseline report template, reproducible experiment configuration.

## Phase IV — Open Release

### Objective
Package crawl artifacts, ASP Drafts, and benchmark results into a monthly public release with a public repository for schema, issues, and community contributions.

### Technical Requirements
Each monthly release is a versioned directory containing the raw crawl archive, the generated ASP Drafts, the benchmark results, and a release manifest listing included domains, schema version, model versions, and dates. Release artifacts are compressed and checksummed. The public repository holds the schema specification, extraction code, benchmark harness, release tooling, and documentation.

### Implementation Details
Release builds run as a GitHub Actions workflow or equivalent CI pipeline. The workflow takes the Phase I archive and Phase II outputs, compresses them, generates the manifest, and publishes to GitHub Releases and an S3-compatible object store. The public repo uses semantic release or standard tags. Issue and PR templates enforce reproducible bug reports and data citations.

### Deliverables
Release packaging tooling, CI workflow, public repository scaffold, schema documentation, automation scripts.

## Phase V — Adoption and Registration

### Objective
Invite site owners to publish official ASPs, support well-known discovery and domain-verified manifests, and transition from inferred Drafts to authored profiles.

### Technical Requirements
Sites publishing an official ASP place a JSON document at /.well-known/asp on their domain. The A2W standard defines the discovery sequence. A verification service checks that the ASP at /.well-known/asp matches the domain's ownership claims. A public registry links domains to their published ASPs and their inferred Drafts for comparison.

### Implementation Details
The registry is a database-backed web application. The verification service downloads the ASP from /.well-known/asp and validates its domain and owner fields. Domain owners can claim their inferred Drafts, update them, and publish new versions. The registry exposes an API for agents to fetch the latest canonical ASP for a domain.

### Deliverables
Well-known discovery specification update, ASP verification service, registry frontend and API, domain owner onboarding flow.
