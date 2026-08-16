# Version 1 plan

Didn't build this — here's how I'd do it if I had more time.

## What's hardcoded right now

`context_builder.py` — one function per PADER section, hand-written.
`prompts.py` — flat dict of PADER's 6 templates.

Everything else doesn't care what report type is asking for it.

## The fix

Move the section list into a config file instead of Python code:

```yaml
report_type: PADER
sections:
  - id: narrative_summary
    analyses: [case_summary, demographic_summary, top_reactions, outcome_summary]
    prompt_file: prompts/narrative_summary.txt
  - id: alerts
    analyses: [alert_summary]
    prompt_file: prompts/alerts.txt
```

Replace all the hand-written context functions with one generic one:

```python
def build_context(section_config, cases_df, reactions_df):
    return {name: getattr(analysis, name)(cases_df, reactions_df) for name in section_config["analyses"]}
```

New report type = new YAML + new prompt files. No new Python unless it needs a number
that doesn't exist yet — and that's just one new function in `analysis.py`, same
pattern as the rest.

## What this gets me

- New report type reusing existing numbers = config only, no code changes
- New report type needing new numbers = one function in `analysis.py` + config
- `analysis.py` functions already don't know or care about report type — that's why
  this refactor is small

## Skipping for now

- Click-a-sentence-see-the-source UI — the data for it already exists via
  `case_index()`, this would just be UI on top
- Tracking which dataset/prompt/model version made which report — easy to add later,
  not core to this
