# From Cozi to GameChanger

**Workflow automation · Read-only calendar tools · OAuth**

[Back to profile](../README.md) · [Cozi for ChatGPT](cozi-calendar-integration.md)

I built the Cozi prototype to answer a question I ask at home all the time. What’s coming up? The family calendar already held the answer. Connecting it to ChatGPT let me ask about schedules, conflicts, and shared free time in plain English.

I wanted the same convenience for a youth baseball schedule in GameChanger. The team calendar called for a different approach to access, while much of the calendar logic could carry over.

## What changed between builds

| | Cozi prototype | GameChanger build |
| --- | --- | --- |
| Workflow | Family schedules, conflicts, and shared availability | Team events, schedule searches, and overlaps |
| Calendar logic | Parse iCalendar feeds, handle recurring events, and answer date-range queries | Reuse the calendar logic and adapt the queries for a team schedule |
| Access | Private, read-only family calendar prototype | Separate read-only connection with GitHub OAuth restricted to an approved account |

The GameChanger feed URL stays in an encrypted Cloudflare Worker secret. ChatGPT calls structured calendar tools through MCP. The Worker checks authorization before reading the feed.

## What the interaction looks like

**Example prompt** “What are our next two events?”

| Day | Event | Time |
| --- | --- | --- |
| Tuesday | Fielding practice | 6:00–7:15 p.m. |
| Saturday | Intrasquad scrimmage | 10:00–11:30 a.m. |

*Fictional schedule for illustration.*

## How I verified it

I checked both sides of the deployed connection. Anonymous tool requests returned HTTP 401 with a Bearer challenge. After signing in, I verified that ChatGPT could retrieve the next two events from the live calendar.

The next workflow I’d try is a weekly coaching brief that pulls upcoming practices and games, flags overlaps or missing locations, and gives coaches a short prep list.

*Independent, unofficial project. The integration is private. This write-up uses fictional schedule entries.*
