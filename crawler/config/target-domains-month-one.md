# A2W/ASP Target Domain List — Month One Crawl

## Purpose

This document lists the initial target domains for the Month One crawl. Domains are selected to cover the six benchmark categories defined in `a2w_asp_benchmark_tasks.md`, with 3-5 domains per category for a total of 20-30 domains. All domains are publicly accessible, Canadian or globally relevant, and suitable for polite crawling.

## Selection Criteria

- Publicly accessible without authentication for core content
- Relevant to the benchmark task category
- robots.txt permits crawling of relevant paths
- Stable, well-structured HTML (prefers semantic markup)
- Represents a realistic agent use case

## Category 1: Restaurant / Food Service (Booking & Availability)

| Domain | Region | Notes |
|--------|--------|-------|
| opentable.ca | CA | Major reservation platform; structured availability data |
| resy.com | Global | High-end restaurant bookings; modern web app |
| sevenrooms.com | Global | Restaurant CRM with booking widgets |
| touchbistro.com | CA/Global | POS + online ordering for restaurants |
| localchain.ca | CA | Canadian chain with online ordering (e.g., timhortons.ca, freshii.com) |

## Category 2: Government Services (Forms & Permits)

| Domain | Region | Notes |
|--------|--------|-------|
| canada.ca | CA | Federal government; comprehensive service directory |
| ontario.ca | CA (ON) | Provincial services; business permits, licenses |
| toronto.ca | CA (ON) | Municipal services; building permits, business licenses |
| bc.gov.ca | CA (BC) | Provincial services; BizPaL integration |
| calgary.ca | CA (AB) | Municipal services; development permits |

## Category 3: E-Commerce (Product → Cart → Checkout)

| Domain | Region | Notes |
|--------|--------|-------|
| shopify.com | Global | Platform; many merchant stores to choose from |
| well.ca | CA | Canadian health/beauty retailer; clean structure |
| indigo.ca | CA | Books/gifts; standard e-commerce patterns |
| mec.ca | CA | Outdoor gear co-op; member checkout flow |
| ecoset.ca | CA | Sustainable goods; simpler catalog |

## Category 4: Healthcare Clinic (Contact & Hours)

| Domain | Region | Notes |
|--------|--------|-------|
| clevelandclinic.ca | CA | Major clinic network; location finder |
| lifelabs.com | CA | Lab services; appointment booking |
| dentsplysirona.com | Global | Dental equipment; clinic locator |
| telushealth.com | CA | Virtual care + clinic network |
| acuityscheduling.com | Global | Appointment scheduling SaaS used by clinics |

## Category 5: SaaS / Technical Documentation (API Auth)

| Domain | Region | Notes |
|--------|--------|-------|
| stripe.com/docs | Global | Gold-standard API docs; clear auth section |
| twilio.com/docs | Global | Comprehensive; multiple auth patterns |
| github.com/docs | Global | Developer platform; OAuth + PAT docs |
| supabase.com/docs | Global | Modern Postgres platform; JWT auth |
| vercel.com/docs | Global | Deployment platform; API token docs |

## Category 6: University / Education (Admissions Deadlines)

| Domain | Region | Notes |
|--------|--------|-------|
| uwaterloo.ca | CA (ON) | Engineering/CS focus; clear admissions pages |
| utoronto.ca | CA (ON) | Large research university; program finder |
| mcgill.ca | CA (QC) | Bilingual; international admissions |
| ubc.ca | CA (BC) | West coast; CS/engineering deadlines |
| senecacollege.ca | CA (ON) | College; applied programs, clear dates |

## Crawl Configuration Notes

### Rate Limits
- Default: 1 request/second per domain with 5-request burst
- Government domains: 0.5 req/s (more conservative)
- Platform domains (shopify, stripe, github): respect their published limits

### robots.txt Handling
- robots.txt handling must be validated per domain before a crawl; do not assume a site permits crawling based on this draft list
- Disallow patterns must be respected automatically
- If robots.txt is unavailable, contradictory, or blocks the required paths, exclude the domain from the release and record the decision in the catalog

### Scope
- Crawl depth: 3 levels from homepage
- Max pages per domain: 200 (configurable)
- Focus paths: those relevant to benchmark tasks (booking, forms, products, contact, docs, admissions)

### Screenshots
- Enable for first 5 domains (one per category) to validate extraction
- Disable for remaining to save storage and time

## Validation Checklist (Pre-Crawl)

- [ ] robots.txt fetched and parsed for each domain
- [ ] At least one target path returns 200 OK
- [ ] Target path contains expected content type (form, product grid, doc nav, etc.)
- [ ] No login wall blocking core task content
- [ ] Domain added to catalog with status "pending"

## Output

After validation, this list will be exported as `crawler/config/targets-month-one.json` with the structure:

```json
{
  "release": "2026-08",
  "domains": [
    {
      "domain": "opentable.ca",
      "category": "restaurant",
      "task_relevant_paths": ["/restaurant", "/availability"],
      "rate_limit_rps": 1.0,
      "screenshots": true
    }
  ]
}
```

---

*This list is a starting draft. Final Month One targets will be confirmed after pre-crawl validation.*