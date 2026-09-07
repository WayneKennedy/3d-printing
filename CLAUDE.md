# Working on the printer

@AGENTS.md

Everything needed to drive this machine is in [AGENTS.md](AGENTS.md), imported above — access,
the rules that will cost a print if broken, slicing, monitoring and aborting. It is
provider-neutral because other harnesses work this repo too.

## Claude-specific notes

- **Prefer a background `Monitor` on `tools/print-monitor.py` over polling.** A print here runs
  8–14 hours; a monitor that emits on every terminal state costs one notification per event,
  where repeated status queries cost a tool call each and still miss a failure between polls.
- **Never let a project fact live only in chat or in auto-memory.** Memory holds pointers; the
  repo holds the fact. Durable conclusions go to [docs/decisions.md](docs/decisions.md),
  unresolved ones to [docs/open-questions.md](docs/open-questions.md).
