# A2W/ASP Benchmark Tasks and Evaluation

## Benchmark Design

The benchmark compares agent task performance under two conditions: raw web access with no ASP available, and ASP-guided access using the inferred Draft for the target domain. All other inputs are held constant: the same agent implementation, the same browser environment, and the same network conditions.

## Task Definition Format

Each task is defined as a JSON document with the following fields. domain is the target domain on which the task is executed. goal is a natural language description of the task. verification is a predicate that returns true if the task was completed successfully. category describes the task type from a fixed taxonomy. difficulty is an integer from 1 to 3 indicating expected complexity. max_steps is the agent step budget before the task is considered failed.

## Pilot Task Set

The following tasks form the pilot benchmark covering five representative site categories.

For a restaurant website under domain restaurant.example.com, the task is to find tonight's reservation availability and report the earliest available time slot. Verification checks that the agent produced a date and time on the correct date. Difficulty is 1. Max steps is 8.

For a government services website under domain gov.example.ca, the task is to locate the application form for a business permit and report the form's title and download URL. Verification checks that the agent found a downloadable PDF or online form link with a matching title. Difficulty is 2. Max steps is 12.

For an e-commerce store under domain shop.example.com, the task is to add a specified product to the cart and reach the checkout page without entering payment details. Verification checks that a cart or checkout page is reached with the correct product name visible. Difficulty is 2. Max steps is 10.

For a healthcare clinic website under domain clinic.example.com, the task is to find the clinic's contact phone number and office hours for a specified day. Verification checks that the agent produced a valid phone number and hours for the correct day. Difficulty is 1. Max steps is 6.

For a SaaS documentation site under domain docs.example.com, the task is to locate the API authentication section and report the first code example. Verification checks that the agent produced code or a code block reference from the authentication section. Difficulty is 2. Max steps is 10.

For a university website under domain uni.example.ca, the task is to find the application deadline for the computer science undergraduate program. Verification checks that the agent produced a calendar date associated with the correct program name. Difficulty is 3. Max steps is 15.

## Metrics

Task success rate measures the fraction of tasks that reach a verified end state within the step budget. Step count measures the number of agent actions taken per task, reported as mean and median. Latency measures wall-clock time from task start to verification, reported as mean and median. Ambiguity events count instances where the agent selected an action from multiple plausible options, indicating uncertainty or incorrect classification. Policy violations count instances where the agent attempted an action blocked by the site's declared policies.

## Evaluation Script Design

The evaluation harness is a Python module that loads task definitions from a JSONL file, instantiates a reference agent with two configuration presets for raw web and ASP-guided modes, executes each task in a sandboxed Playwright browser session, logs every agent decision and browser action, verifies the end state against the task predicate, and writes structured results to JSONL.

The harness writes one JSONL record per trial. Each record contains the task id, domain, condition, success boolean, step count, latency milliseconds, ambiguity events list, policy violations list, final URL, and verification result. Aggregate metrics are computed from these records and published in the benchmark report for each release.

## Reproducibility

Each benchmark run is parameterized by a configuration file that specifies the agent version, browser version, task set version, and release identifier. The configuration is committed alongside the results so that every published benchmark can be reproduced exactly by checking out the corresponding code and configuration tags.
