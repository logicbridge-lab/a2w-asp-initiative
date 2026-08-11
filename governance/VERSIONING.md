# Versioning and Releases

A2W/ASP uses semantic versioning for the protocol, schema, and reference utilities. `0.x` releases are drafts and may introduce breaking changes with explicit migration notes. `1.0.0` is reserved for the first stable standard release.

A patch release corrects errors without changing meaning. A minor release adds backward-compatible fields or guidance. A major release changes or removes a normative requirement.

A profile’s own `version` is independent of the schema version. Consumers must reject unsupported schema major versions, may accept newer compatible minor versions, and must not silently reinterpret removed fields.

Each release must tag the repository, update `CHANGELOG.md`, identify normative versus advisory changes, and include passing schema/example/conformance checks.
