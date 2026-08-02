# A2W/ASP Release Packaging and Automation

## Release Cadence

A2W/ASP publishes a monthly public release. Each release is a versioned snapshot of the crawl archive, ASP Drafts, benchmark results, and supporting metadata for one calendar month. The release process runs automatically through CI after quality gates pass, and the release artifacts are published to GitHub Releases and to a public object storage location.

## Release Contents

Each release contains the crawl archive, the ASP Drafts, the benchmark results, the release manifest, and the schema version snapshot. The crawl archive is a compressed tarball organized per domain with raw HTML, extracted text, metadata JSON sidecars, and optional screenshots. The ASP Drafts are a compressed directory of one JSON file per domain. The benchmark results are a compressed JSONL file containing one record per trial. The release manifest is a JSON document describing the release number, release date, included domain count, schema version, model version, and digest checksums for each artifact. The schema version snapshot is a copy of the schema definition active at release time.

## Release Directory Layout

Within a release directory named release-YYYY-MM, the layout is structured as crawl/ containing per-domain raw artifacts, asp_drafts/ containing per-domain ASP Draft JSON, benchmark/ containing trial results and summary reports, manifest.json as the release descriptor, schema.json as the versioned schema snapshot, and README.md as a human-readable summary of the release contents and highlights.

## Automation Pipeline

The release automation is defined as a CI workflow with six stages. The first stage is crawl completion, which triggers when all target domain crawl jobs report success for the month. The second stage is extraction completion, which runs the structural extraction pipeline over the new crawl artifacts and writes ASP Drafts to the artifact store. The third stage is benchmark execution, which runs the benchmark tasks against the new crawl and ASP Drafts and records results. The fourth stage is artifact packaging, which compresses all release contents into artifacts and generates the manifest. The fifth stage is quality gates, which verify artifact checksums, schema conformance for a sample of ASP Drafts, and benchmark result completeness. The sixth stage is publication, which creates a GitHub Release with the packaged artifacts and publishes to the object store.

## Checksums and Provenance

Every artifact in a release is SHA-256 checksummed. The manifest contains the checksum for each artifact and the schema version used to generate it. The release tag follows the same version as the manifest release field. This structure allows any consumer to verify that artifacts were not tampered with after publication.

## Backfill and Correction Policy

If a release is found to contain errors after publication, a patch release is issued with a suffix such as release-YYYY-MM-patch-1. The patch release contains corrected artifacts for the affected domains and an updated changelog entry. Original defective artifacts are not removed but are marked deprecated in the manifest. This preserves reproducibility for any work that referenced the original release.
