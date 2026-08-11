# Publishing an ASP

## What you publish

Publish one JSON document at `https://<your-domain>/.well-known/asp`. The document must validate against the A2W/ASP schema and must describe only resources, actions, policies, and access conditions you control.

## Minimal workflow

Copy a close example from `examples/`, replace the domain and owner fields, remove every capability you do not intend to support, then validate it locally.

```bash
python3 reference/asp_validator.py my-asp.json
mkdir -p public/.well-known
cp my-asp.json public/.well-known/asp
```

Serve the file with `Content-Type: application/json` over HTTPS. Confirm that `curl -i https://<your-domain>/.well-known/asp` returns `200` and the expected JSON body.

## Deployment checklist

Your `domain` must match the host that serves the profile. Every declared action must have clear preconditions. Declare authentication honestly; publishing an action never makes it public. Use `policies.prohibitions` for disallowed automation, `rate_limits` for measurable limits, and `evidence.source: domain_authored` with confidence `1.0` for an owner-published profile.

Only advertise stable paths. Review the ASP whenever an action, policy, or authentication flow changes. Increment the profile `version` for changes and follow the versioning policy for schema upgrades.

## Safety

Do not put credentials, user data, internal URLs, or hidden admin actions in an ASP. An ASP is public by design. It cannot override robots.txt, terms of use, consent, or authorization checks. Keep server-side authorization as the enforcement point.

## Verify before publishing

```bash
python3 reference/asp_validator.py my-asp.json
```

Then inspect `https://<your-domain>/.well-known/asp` from an unauthenticated browser session. If it is malformed or unavailable, an A2W client will fall back rather than assume access.
