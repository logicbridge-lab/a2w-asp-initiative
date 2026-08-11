# Security and Policy Requirements

**Draft 0.1.0**

## Threat model

An ASP is public, mutable, and may be malicious, stale, incomplete, or accidentally overbroad. Clients must therefore validate both syntax and origin, treat profile declarations as untrusted input, and retain server-side responses as the final enforcement point.

## Publisher requirements

Publishers MUST serve ASPs only over HTTPS. They MUST NOT include credentials, private user data, unadvertised administrative capabilities, internal network addresses, or secrets. They MUST enforce authentication and authorization on the action endpoint itself; an ASP is documentation, not an access-control mechanism.

Publishers SHOULD express measurable request limits, prohibited automation, authentication requirements, and intended data-use boundaries in `policies`. A publisher SHOULD return conventional HTTP status codes for denied, unauthorized, rate-limited, and malformed requests.

## Client requirements

Clients MUST validate JSON and schema before use, verify `domain` equality, and enforce hard prohibitions before taking an action. They MUST NOT rely on an inferred Draft for authorization. They MUST apply least privilege, send only data necessary for the action, and avoid credentials in URLs, logs, or profile artifacts.

Clients MUST request confirmation for material side effects unless they have task-scoped authority. They MUST stop on 401, 403, 429, or an explicit policy denial. They MUST honor robots.txt, applicable terms, and law independently of the ASP.

## Abuse handling

A client SHOULD log the profile URL, version, validation result, selected action, policy decision, and server response class. It SHOULD avoid logging user-provided sensitive values. A publisher SHOULD provide a feedback channel for profile errors and abuse reports.

## Disclosure

Security issues affecting the protocol, schema, reference utilities, or published examples should be reported privately to the maintainers rather than posted in public issues. Until a dedicated security contact is established, use the contact path in the project’s GitHub security advisory flow.
