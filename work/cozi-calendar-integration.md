# Cozi for ChatGPT

### Ask the calendar a useful question.

**Workflow automation · MCP integration · Deterministic calendar logic**

[Back to profile](../README.md)

A family calendar already contained the information needed to answer questions about schedules, overlapping events, and shared free time. The friction was reconciling it manually.

I built an unofficial, read-only integration that exposes a Cozi iCalendar feed through a Cloudflare Worker and structured Model Context Protocol tools.

## Seven focused tools

The integration lists participants and events, finds a person's next event, searches event details, detects conflicts, finds shared open windows, and summarizes availability without double-counting overlaps.

The calendar engine handles timed and all-day events, recurrence, exclusions, participant prefixes, and time zones.

**Calendar feed → Fetch and parse → Deterministic calculation → Conversational answer**

The language interface makes questions easier to ask; the tool layer performs the calculations. Reading the calendar was sufficient for the initial use case, so the integration did not need permission to add, delete, or reschedule events.

## Delivery and contribution

The deployed private MVP passed retained end-to-end validation on August 11, 2026 across schedules, next-event lookup, conflicts, shared free time, and availability comparisons.

I defined the problem, tool boundaries, expected answers, and test scenarios, and directed AI-assisted implementation and deployment. The transferable pattern is to expose the minimum useful capability, keep calculations testable, and validate the actual user question.

*Private MVP, not a public integration release. Per-user authentication, onboarding, and privacy work remain prerequisites for broader distribution. Source, calendar contents, and feed credentials remain private. Independent and unofficial; not endorsed by Cozi or OpenAI.*
