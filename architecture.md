# Architecture

```mermaid
flowchart TD
    A[Bisoprolol Excel Dataset] --> B[data_loader.py]

    B --> C[Case-level DataFrame]
    B --> D[Reaction-level DataFrame]

    C --> E[analysis.py]
    D --> E

    E --> F[Deterministic Analysis Results]

    F --> G[context_builder.py]

    G --> H[Section-specific Context]

    H --> I[prompts.py]
    I --> J[LLM Generation]
    J --> K[llm_client.py]

    K --> L[Generated Section Text]

    L --> M[human_review.py]
    M --> N{Human Review}

    N -->|Approve| O[Approved Sections]
    N -->|Flag| P[Flagged Sections]

    O --> Q[report_generator.py]
    Q --> R[PADER Report]
```

## Architecture Overview

The system separates deterministic data processing from LLM-based narrative generation.

- `data_loader.py` loads and prepares the source data.
- `analysis.py` performs deterministic calculations.
- `context_builder.py` creates section-specific evidence.
- `prompts.py` controls the narrative generation instructions.
- `llm_client.py` handles the LLM call.
- `human_review.py` provides human approval/flagging.
- `report_generator.py` assembles the final report.