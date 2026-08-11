# A2W Protocol Specification

**Draft 0.1.0**

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

## 1. Scope

A2W defines discovery and consumption of an Agentic Site Profile (ASP). It does not define an authorization protocol, replace an API, permit scraping, or create an obligation for a domain to support automated actions.

## 2. Terminology

An **ASP** is a JSON document conforming to the canonical schema. A **publisher** is the domain owner or authorized operator serving an ASP. A **client** is software retrieving and evaluating an ASP. An **action** is a declared, named capability; its declaration is not authorization to execute it.

## 3. Discovery

For an HTTPS origin `https://host/path`, a client MUST attempt discovery at `https://host/.well-known/asp`. The request SHOULD send `Accept: application/json`. A publisher MUST serve a valid profile with `Content-Type: application/json` and HTTPS.

A client MUST reject a profile when its `domain` does not equal the requested host, when the response is not valid JSON, when it fails schema validation, or when its schema major version is unsupported. A client MUST treat HTTP 404, 410, malformed response, network failure, and rejected validation as **no profile**.

A client MAY cache a successfully validated profile according to normal HTTP cache semantics. It MUST NOT cache a profile beyond explicit cache-control limits. It MUST revalidate before executing an action after a material policy change is detected.

## 4. Profile interpretation

Clients MUST evaluate `scope` before using a resource or action. Clients MUST treat unrecognized fields as advisory and MUST preserve the meaning of recognized fields. Clients MUST enforce a `hard` policy locally before attempting a matching action and SHOULD enforce `soft` policies unless they conflict with explicit user direction or applicable law.

`evidence.source: domain_authored` identifies profile provenance only. It does not authenticate a user, approve an action, or supersede server-side authorization. `evidence.source: inferred` MUST NOT be treated as an owner-controlled contract.

## 5. Actions and side effects

A client MUST verify an action's preconditions and declared authentication requirements before attempting it. For actions with financial, legal, privacy, publication, deletion, or other material side effects, the client MUST obtain user confirmation unless it possesses prior task-scoped authority that explicitly covers that action.

A client MUST NOT attempt an action declared in `policies.prohibitions`. It MUST respect rate limits and server responses. A client MUST treat authentication failures, HTTP 403, HTTP 429, and malformed outputs as failures rather than attempts to discover alternate undisclosed paths.

## 6. Fallback

When no usable ASP exists, a client MAY use ordinary web or API behavior only under its existing permissions and policies. It MUST NOT claim an A2W guarantee, infer a policy from absence, or bypass an access restriction.

## 7. Versioning

The profile `version` is a semantic version for that profile. The A2W protocol and schema follow the release policy in `governance/VERSIONING.md`. Clients MUST reject unsupported major schema versions and SHOULD warn on newer minor versions.
