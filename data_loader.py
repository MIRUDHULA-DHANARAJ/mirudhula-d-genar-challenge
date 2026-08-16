from pathlib import Path
import pandas as pd
from utils import normalize_age, age_group

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "bisoprolol.xlsx"


def load_data():
    raw_df = pd.read_excel(DATA_FILE)

    # keep only the latest version of each case
    cases_df = (
        raw_df
        .sort_values("safetyreportversion")
        .drop_duplicates("safetyreportid", keep="last")
    )

    # add age columns
    cases_df["normalized_age"] = cases_df.apply(
        lambda row: normalize_age(
            row["patient_patientonsetage"],
            row["patient_patientonsetageunit"]
        ),
        axis=1
    )
    cases_df["age_group"] = cases_df["normalized_age"].apply(age_group)

    # explode comma-joined reactions into one row per (case, reaction)
    reaction_rows = []
    for _, row in cases_df.iterrows():
        reactions = str(row["patient_reaction_reactionmeddrapt"]).split(",")
        outcomes = str(row["patient_reaction_reactionoutcome"]).split(",")

        for reaction, outcome in zip(reactions, outcomes):
            reaction_rows.append({
                "safetyreportid": row["safetyreportid"],
                "reaction": reaction.strip(),
                "outcome": outcome.strip(),
                "serious": row["serious"],
            })

    reactions_df = pd.DataFrame(reaction_rows)

    return cases_df, reactions_df


if __name__ == "__main__":
    cases_df, reactions_df = load_data()
    print("cases:", len(cases_df))
    print("reactions:", len(reactions_df))