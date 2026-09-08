# Cozi for ChatGPT

### A small integration built around a real coordination problem.

**Workflow automation · MCP tooling · Deterministic calendar logic**  
**Updated September 8, 2026 · Private deployed MVP**

[Back to profile](../README.md)

## The job to be done

A family calendar already contained the information needed to answer questions about schedules, overlapping events, and free time. The friction was repeatedly inspecting and reconciling that information by hand.

I built an unofficial, read-only integration that lets ChatGPT query a Cozi iCalendar feed through a Cloudflare Worker and structured Model Context Protocol (MCP) tools.

## Seven tools, one focused boundary

| Tool category | Supported question |
|---|---|
| Family members | Who is represented in the calendar? |
| Events | What is scheduled within a date range? |
| Next event | What is the next event for a person? |
| Search | Which events match a title, place, or description? |
| Conflicts | Which events overlap? |
| Free time | Where is a shared open window? |
| Availability summary | How does busy/free time compare without double-counting overlaps? |

The calendar engine handles timed and all-day events, recurrence rules, exclusions, participant prefixes, timezone-aware output, and overlapping-event unions.

## The design choice

**Calendar feed → Fetch and parse → Deterministic tools → Conversational answer**

The language interface makes questions easier to ask. The tool layer performs the calendar calculations. The integration does not need permission to add, delete, or reschedule events to solve its initial use case.

Keeping the first version read-only reduced the consequence of a mistaken interpretation and made the acceptance questions concrete.

## Validation and release boundary

The private MVP's retained August 11, 2026 validation covered schedule queries, next-event lookup, person-specific schedules, conflict detection, shared free-time search, and availability comparisons.

That is private end-to-end validation—not public-release approval. Per-user connection/authentication, onboarding, and privacy work remain requirements before a broader release. The calendar feed is treated as a credential; neither it nor real calendar contents are published in this case study.

## My contribution and the transferable value

I defined the practical problem, the tool boundaries, the expected answers, and the test scenarios, and directed AI-assisted implementation and deployment.

The relevant product pattern extends beyond a family calendar: expose the minimum useful capability, keep calculations testable, protect the underlying data, and validate the actual user question rather than merely demonstrating that an API responds.

*Evidence basis: the private implementation README and its retained validation record. Source and live calendar access remain private. This is an independent, unofficial integration, not an endorsement by Cozi or OpenAI.*
