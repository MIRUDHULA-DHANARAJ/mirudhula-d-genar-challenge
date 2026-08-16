from pathlib import Path
import pandas as pd


# Project root = one level above src/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Input dataset
DATA_FILE = PROJECT_ROOT / "data" / "bisoprolol.xlsx"

# Load data
df = pd.read_excel(DATA_FILE)

# Keep only the latest version of each safety report
df = (
    df.sort_values("safetyreportversion")
      .drop_duplicates("safetyreportid", keep="last")
)

# Results
total_cases = len(df)
serious_cases = (df["serious"] == "serious").sum()

print(f"Total cases: {total_cases}")
print(f"Serious cases: {serious_cases}")

sample = df[df["patient_reaction_reactionmeddrapt"].astype(str).str.contains(",")]
print(sample[["safetyreportid", "patient_reaction_reactionmeddrapt", "patient_reaction_reactionoutcome"]].head(3))