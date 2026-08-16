# Architecture

```
bisoprolol.xlsx
      |
      v
data_loader.py
  - keep latest version of each case (1068 rows -> 1024 cases)
  - split comma-joined reactions into separate rows (-> 3423 reaction rows)
      |
      v
analysis.py                          <- pure pandas, no AI
  - case_summary, demographic_summary
  - top_reactions, top_serious_reactions
  - outcome_summary, alert_summary
  - monthly_trend, case_index
      |
      v
context_builder.py
  - one small JSON packet per report section
  - only the numbers that section needs, nothing else
      |
      v
prompts.py
  - one system prompt (rules, same for every section)
  - one short template per section
      |
      v
llm_client.py                        <- only file that calls Claude
      |
      v
human_review.py
  - every section sits as "pending" until approved
  - flagged/pending sections show a banner instead of final text
      |
      v
report_generator.py
  - pulls approved text in
  - pulls tables straight from analysis.py (not through the model)
  - writes report_output.md
```

## Why this shape

Two separate tables (cases vs reactions) because case-level questions (total cases,
serious split) and reaction-level questions (top reactions) have different
denominators. Mixing them up is how "1,068 cases" type mistakes happen.

`context_builder.py` is its own file instead of being built inline, because deciding
what goes in each section's packet is the actual point of the exercise, not just
plumbing.

One system prompt shared across all sections because the ground rules (don't invent
numbers, don't turn observations into conclusions) are the same everywhere. Only the
numbers and section-specific instruction change per call.

Review gate is a plain JSON file, not a UI — for Version 0 it just needs to exist and
actually block unapproved text from reaching the final report.
