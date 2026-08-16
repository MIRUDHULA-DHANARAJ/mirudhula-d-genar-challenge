SYSTEM_PROMPT = """You are drafting one section of a PADER (Periodic Adverse Drug Experience Report).

Rules:
1. Only use numbers and facts given to you in the "data" below. Never calculate or guess a number that isn't there.
2. Never turn an observation into a safety conclusion. "143 cases reported X" is fine. "X is a confirmed safety signal" is not, unless the data explicitly says so.
3. If something is missing from the data (like no action history), say so plainly. Do not invent it.
4. Keep the tone neutral and factual, like a regulatory document. No marketing language.
5. Write only the section text. No headers, no repeating these instructions back.
"""

TEMPLATES = {
    "narrative_summary": """Section: Narrative Summary and Analysis

data:
{data}

Write 2-3 paragraphs summarizing the overall safety experience for this reporting period using only the numbers above. Cover total case volume, seriousness split, leading reactions (overall and among serious cases), outcomes, and demographic/geographic shape.""",

    "summary_analysis": """Section: Summary Analysis of Cases

data:
{data}

Write 1-2 paragraphs on case volume and demographics (age groups, sex, country) using only the numbers above.""",

    "reaction_analysis": """Section: Reaction / Adverse Event Analysis

data:
{data}

Summarize the most common reactions overall and among serious cases, using only the numbers above. Mention that System Organ Class grouping isn't available in the source data.""",

    "alerts": """Section: Serious Cases / 15-Day Alerts

data:
{data}

Summarize the alert case volume and seriousness criteria breakdown. Note the criteria are independent flags and won't sum to the total.""",

    "trends": """Section: Trends and Important Observations

data:
{data}

Describe the month-by-month case volume pattern factually. Do not call any pattern a "signal" or say it needs action -- just describe the numbers and note that significance is for a human reviewer to decide.""",

    "history_of_actions": """Section: History of Actions

data:
{data}

State in 1-2 sentences that no history-of-actions data was supplied for this period. Do not invent any actions.""",
}