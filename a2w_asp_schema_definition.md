# A2W/ASP Schema Definition

## ASP Top-Level Structure

The schema defines the structure of an Agentic Site Profile document. Each field is optional unless explicitly marked required. Inferred Drafts may omit fields that could not be confidently extracted. Domain-authored profiles should populate all applicable fields.

domain is a required string identifying the fully qualified domain name the profile applies to, such as example.com. This field anchors the profile to a specific web property.

owner is a required object containing the profile maintainer's details. The object includes name, contact_email, and optionally a verification_url that points to a domain ownership verification document. The owner object is critical for establishing trust in the profile, especially for inferred Drafts where the agent operator may want to contact the maintainer.

version is a required string in semantic versioning format, such as 1.0.0. This field allows the profile to evolve without breaking consumers that depend on a specific schema version.

scope is an optional string or array describing which parts of the domain the profile covers. A value of / indicates the entire domain. A value of /docs indicates only the documentation subpath. When an array is provided, each entry describes a distinct covered region.

resources is an optional array of resource objects. Each resource object includes path, content_type, description, and optionally schema_ref. Resources describe the machine-usable surfaces of the site, providing discovery information that agents can use to identify data sources and interaction endpoints.

actions is an optional array of action objects. Each action object includes name, description, parameters, output, and preconditions. Actions are the core of the profile: they declare what operations the site supports and what an agent must provide to execute them safely.

policies is an optional object of policy arrays keyed by policy type. Supported types include rate_limits, authentication, data_usage, and prohibitions. Each policy entry includes a description, severity, and enforcement mechanism. Policies govern agent behavior at a granularity that no existing web standard addresses.

workflows is an optional array of workflow objects. Each workflow object includes name, description, steps, and branching. Steps reference actions by name and specify parameters, fallback behavior, and state requirements. Workflows enable complex tasks to be described as composable, reusable procedures.

auth is an optional object describing authentication requirements. The object includes required boolean, type enum with values none, api_key, oauth2, or custom, and parameters containing the fields needed for the agent to obtain credentials. When required is false, no authentication is needed.

evidence is an optional object describing the provenance of the profile. The object includes source enum with values domain_authored or inferred, confidence number between 0 and 1, and references array of strings linking to crawl artifacts or extraction evidence. For domain-authored profiles, references may be empty and confidence may be 1.0. For inferred Drafts, confidence reflects the model's certainty and references point to the bootstrap evidence.

observability is an optional object describing telemetry the site exposes for agent interactions. The object includes logs boolean indicating whether request logs are available, metrics array of strings naming available metrics such as latency or error_rate, status_endpoint string pointing to a health or status URL, and feedback_channel string providing a URL or email for agent operators to report issues.

## ASP JSON Example

The following example illustrates a realistic inferred ASP Draft for a small business website that offers appointment scheduling.

```json
{
  "domain": "example.com",
  "owner": {
    "name": "Example Studio",
    "contact_email": "hello@example.com",
    "verification_url": "https://example.com/.well-known/ownership"
  },
  "version": "1.0.0",
  "scope": "/",
  "resources": [
    {
      "path": "/",
      "content_type": "text/html",
      "description": "Homepage with service overview and contact information"
    },
    {
      "path": "/book",
      "content_type": "text/html",
      "description": "Appointment booking form"
    },
    {
      "path": "/api/availability",
      "content_type": "application/json",
      "description": "Availability data feed for date selection"
    }
  ],
  "actions": [
    {
      "name": "search_services",
      "description": "Return a list of available services",
      "parameters": {
        "query": "string, optional, free text search"
      },
      "output": "application/json",
      "preconditions": []
    },
    {
      "name": "book_appointment",
      "description": "Submit a booking request for a selected service and time slot",
      "parameters": {
        "service_id": "string, required",
        "date": "string, required, ISO 8601",
        "time": "string, required, HH:mm",
        "name": "string, required",
        "email": "string, required"
      },
      "output": "application/json",
      "preconditions": [
        "availability_check"
      ]
    }
  ],
  "policies": {
    "rate_limits": [
      {
        "description": "Maximum 10 booking requests per minute per client IP",
        "severity": "hard",
        "enforcement": "429 response"
      }
    ],
    "authentication": [
      {
        "description": "No authentication required for browsing and booking",
        "severity": "info",
        "enforcement": "none"
      }
    ],
    "data_usage": [
      {
        "description": "Email addresses collected are used only for appointment confirmation",
        "severity": "soft",
        "enforcement": "privacy policy"
      }
    ],
    "prohibitions": [
      {
        "description": "Automated bulk booking or scraping of availability data is prohibited",
        "severity": "hard",
        "enforcement": "IP ban"
      }
    ]
  },
  "workflows": [
    {
      "name": "standard_booking",
      "description": "Browse services, select time, and confirm booking",
      "steps": [
        {
          "action": "search_services",
          "parameters": {
            "query": ""
          }
        },
        {
          "action": "book_appointment",
          "parameters": {
            "service_id": "from_service_selection",
            "date": "from_user",
            "time": "from_user",
            "name": "from_user",
            "email": "from_user"
          }
        }
      ],
      "branching": []
    }
  ],
  "auth": {
    "required": false,
    "type": "none",
    "parameters": {}
  },
  "evidence": {
    "source": "inferred",
    "confidence": 0.87,
    "references": [
      "crawl/2026-08/example.com/index.html",
      "crawl/2026-08/example.com/book.html",
      "extract/2026-08/example.com/forms.json"
    ]
  },
  "observability": {
    "logs": false,
    "metrics": [],
    "status_endpoint": "",
    "feedback_channel": "hello@example.com"
  }
}
```

This example demonstrates how all sections combine into a usable profile. The evidence section clearly identifies it as an inferred Draft with a confidence score and artifact references. The policies section provides explicit guardrails for agents. The workflows section turns multiple actions into a coherent business process.
