# Consuming an ASP

## Discovery

Given `https://example.com/path`, an A2W client requests `https://example.com/.well-known/asp` over HTTPS. It must use the final origin after redirects only when the redirect remains within the same registrable domain or the user has explicitly authorized the new origin.

## Required client behavior

A client must treat a missing profile, invalid JSON, invalid schema, domain mismatch, unsupported major version, or unavailable profile as **no profile**. It must not infer permission from page content or from a partially valid profile.

After validation, the client must filter resources and actions to the current URL scope, enforce declared hard policies before executing an action, and satisfy declared authentication and preconditions. A client must not execute an action with material side effects without the authorizing user's confirmation unless the client already holds explicit task-scoped authority.

## Minimal client

```python
from reference.asp_client import discover

profile = discover("https://example.com/products")
if profile is None:
    print("No usable ASP: use ordinary, permission-aware fallback behavior.")
else:
    print(profile["domain"], profile["version"])
```

## Failure behavior

A client should record why discovery failed without storing profile contents unnecessarily. It should respect server rate limits and retry guidance. It must never treat an inferred ASP Draft as owner authorization; `evidence.source` controls provenance, not permission.

Read the full requirements in the [protocol specification](../../spec/a2w-protocol.md) and [security specification](../../spec/security.md).
