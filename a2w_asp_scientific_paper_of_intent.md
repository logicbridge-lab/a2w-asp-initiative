# Scientific Paper of Intent: A2W/ASP — Agent-to-Web Standard and Agentic Site Profiles

## Authors

LogicBridge AI Lab, Toronto, Canada

## Abstract

We present the Agent-to-Web (A2W) standard and Agentic Site Profile (ASP) as a framework for structured interaction between autonomous agents and web domains. As autonomous agents increasingly navigate the web to perform tasks on behalf of users, the absence of a standardized machine-readable site contract imposes significant costs in reliability, safety, efficiency, and auditability. We propose a lightweight, domain-published profile format that declares identity, resources, actions, policies, and interaction patterns for autonomous agents. We further propose a bootstrap research program that generates inferred ASP Drafts through automated crawling and structural extraction, publishes them as a monthly open corpus, and benchmarks agent performance under raw web versus ASP-guided conditions. We hypothesize that ASP-guided navigation will significantly outperform raw web inference across task success rate, step efficiency, ambiguity reduction, and policy compliance.

## 1. Introduction

The World Wide Web was designed as a hypertext system for human readers. HTML, CSS, and the Document Object Model are presentation-oriented abstractions. Navigation structure, form semantics, and interactive elements are optimized for visual consumption by people. This design works well for its original purpose but creates a fundamental impedance mismatch when autonomous agents need to use websites as tools, data sources, or transaction platforms.

Current approaches to agent-web interaction fall into three categories. The first is DOM-based inference, where agents parse the HTML structure and attempt to identify semantic elements through heuristics, accessibility metadata, and machine learning. The second is vision-based inference, where agents take screenshots and use multimodal models to identify click targets and form fields. The third is API-based integration, where agents use formal programmatic interfaces when available.

All three approaches have significant limitations. DOM and vision-based methods are brittle, site-specific, and difficult to evaluate systematically. API-based integration is reliable but rare, especially for smaller organizations that cannot afford to build and maintain dual interfaces. The result is a fragmented landscape where agent reliability is unpredictable, site operators have limited governance over agent behavior, and the cost of integration scales unfavorably with the number of target domains.

## 2. Related Work

The problem of machine-readable site description has several precedents. Robots.txt provides a simple policy mechanism for crawler exclusion but lacks the expressiveness to describe actions, workflows, or authentication requirements. Sitemaps provide URL discovery but not interaction semantics. Schema.org offers structured data markup embedded in HTML but is oriented toward search engine understanding rather than agent action. OpenAPI and GraphQL provide formal API descriptions but require dedicated backend infrastructure that most websites do not maintain.

The closest analogue to our proposal is the robots.txt standard extended with the proposed robots-extensions work, which adds crawl-delay and allow-directive granularity. However, even extended robots.txt does not approach the expressiveness needed for task-oriented agent interaction.

Our approach differs from prior work in three ways. First, we target task-oriented agent behavior rather than just data access. Second, we provide a schema that can be inferred automatically for bootstrap adoption. Third, we commit to an open, recurring corpus that creates immediate utility even before domain owners publish their own profiles.

## 3. The A2W Standard

A2W defines a discovery mechanism and representation format for agent-facing site descriptions. The discovery mechanism specifies that agents should look for an ASP at a well-known path, currently proposed as /.well-known/asp. The representation format is a JSON or YAML document conforming to the ASP schema.

The standard does not mandate that sites publish an ASP. It defines what an ASP looks like when one exists and how agents should discover and interpret it. This is intentionally lightweight: the standard succeeds when it provides a convention that agents can rely on and sites can optionally adopt.

## 4. The ASP Schema

The ASP schema comprises the following top-level sections. Each section has a defined structure and recommended subfields.

Domain identifies the scope of the profile, using the domain name as the primary key. Owner includes contact information and optionally a verification mechanism. Version follows semantic versioning for the profile document itself, independent of the site's own versioning.

Scope defines which parts of the domain the profile covers. A site may publish multiple ASPs for different subdomains or services, or a single unified profile.

Resources describe the machine-accessible surfaces of the site. Each resource entry includes a path, content type, description, and optional schema reference. Resources may be pages, data feeds, file endpoints, or API endpoints.

Actions define the operations an agent can perform. Each action includes a name, description, parameters, expected output, and preconditions. Actions may be simple (search, lookup) or compound (book appointment, place order). Actions may also specify idempotency, side effects, and cost.

Policies are constraints on agent behavior. Rate limit policies specify maximum request frequency. Authentication policies specify required credentials. Data usage policies specify how retrieved data may be used. Prohibition policies specify actions that are never permitted regardless of technical feasibility.

Workflows define multi-step procedures that combine multiple actions. A workflow specifies an ordered sequence of actions, branching conditions, failure handling, and state management. Workflows enable complex tasks to be described as composable units rather than monolithic action definitions.

Auth specifies authentication mechanisms. Supported types include none, api_key, oauth2, and custom. Each type includes the parameters needed for the agent to obtain and present credentials.

Evidence documents the origin of the profile. For domain-authored profiles, this is a declaration of authenticity. For inferred ASP Drafts, this links to the crawl evidence and extraction pipeline output used to generate each field.

Observability specifies telemetry and monitoring of agent interactions. This may include request logging, performance metrics, status endpoints, and feedback channels.

## 5. Hypotheses

Our primary hypothesis is that sites that publish an ASP will be more efficiently and safely navigable by autonomous agents than sites accessed through raw browser-based inference alone. We break this into four testable sub-hypotheses.

H1 states that agents operating with ASP guidance will achieve higher task success rates and require fewer steps than agents operating without ASPs, when performing equivalent tasks on the same sites.

H2 states that agents operating with ASP guidance will exhibit lower ambiguity in action classification, measured by the frequency of uncertain or incorrect action selection events.

H3 states that agents operating with ASP guidance will demonstrate improved governance compliance, measured by the rate of policy violations and the clarity of agent intent to site operators.

H4 states that a recurring open corpus of inferred ASP Drafts will bootstrap adoption and accelerate the transition from inferred to domain-authored profiles.

## 6. Method

Our research program has four phases executed in parallel and iterated monthly.

Phase one is the crawler and capture phase. We deploy a polite, robots-respecting web crawler that captures HTML, rendered text, metadata, and optional headless-browser screenshots from target domains. The crawler respects robots.txt directives and rate-limiting signals. Output is organized as a versioned archive per domain per release.

Phase two is the structural extraction phase. A combination of heuristic rules and small model-assisted classification extracts page purpose, navigation structure, form semantics, and candidate actions from the raw crawl data. Each extracted element is assigned a confidence score. Evidence references are preserved for auditability.

Phase three is the ASP Draft generation phase. The extracted elements are compiled into a structured ASP Draft according to the schema. Fields are populated where confidence exceeds a threshold and marked as unknown otherwise. The full evidence trail is included for every populated field.

Phase four is the benchmarking phase. We define a task set covering common agent use cases across multiple site categories. Each task is attempted under raw web and ASP-guided conditions using one or more reference agent implementations. Results are published alongside each monthly corpus release.

## 7. Evaluation

We evaluate our hypotheses through the benchmarking phase metrics. H1 is evaluated by comparing task success rates and step counts between conditions. H2 is evaluated by measuring the frequency of ambiguity events during task execution. H3 is evaluated by counting policy violation incidents in each condition. H4 is evaluated by tracking community adoption metrics: number of domains with published ASPs, number of inferred Drafts downloaded, and number of contributions from external researchers.

Expected findings include statistically significant improvements in ASP-guided task success rates, substantial reductions in ambiguity events, near-zero policy violations under ASP guidance, and steady growth in corpus adoption over the first twelve months.

## 8. Limitations and Risks

Several limitations and risks deserve acknowledgment. The bootstrap corpus will initially contain inferred Drafts that are necessarily incomplete and may contain errors. Site operators may object to inferred profiles of their domains, though the profiles are derived from public crawl data. The benchmarking harness may not capture all agent use cases, and results may not generalize to every site category. Finally, adoption by domain owners is not guaranteed even if the technical approach succeeds.

We address these risks through transparency about confidence scores, opt-out mechanisms for site operators, extensible benchmark task definitions, and a community engagement strategy that prioritizes collaborative over adversarial adoption.

## 9. Open Corpus Commitment

We commit to publishing a monthly open corpus of crawl data, ASP Drafts, and benchmark results. The corpus is released under an open license that permits reuse, derivation, and redistribution with attribution. The corpus is designed to be a community resource comparable in spirit to Common Crawl but focused on agent interaction rather than general web data.

## 10. Conclusion

A2W/ASP addresses a fundamental and growing gap between the human-optimized web and the needs of autonomous agents. The standard is lightweight, the schema is practical, and the bootstrap program creates immediate value even before widespread adoption. We invite collaborators, site operators, agent developers, and researchers to join this effort. The first monthly release is targeted within 90 days. The full specification and reference implementation will be published at the project repository.

## References

(To be populated as the initiative progresses. Initial reference areas include the robots.txt standard, the Common Crawl corpus, the Schema.org vocabulary, OpenAPI specification, and relevant work on web agent benchmarks.)
