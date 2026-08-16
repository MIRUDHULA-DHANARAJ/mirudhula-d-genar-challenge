import matplotlib.pyplot as plt
import pandas as pd



# 1. MONTHLY CASE TREND

def plot_monthly_trend(cases_df):

    dates = pd.to_datetime(
        cases_df["receivedate"],
        format="%Y%m%d",
        errors="coerce"
    )

    monthly_cases = (
        dates
        .dt.to_period("M")
        .value_counts()
        .sort_index()
    )

    plt.figure(figsize=(10, 5))

    plt.plot(
        monthly_cases.index.astype(str),
        monthly_cases.values,
        marker="o"
    )

    plt.title("Monthly Safety Case Trend")
    plt.xlabel("Month")
    plt.ylabel("Number of Cases")

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


# 2. TOP REACTIONS


def plot_top_reactions(reactions_df, top_n=10):

    top_reactions = (
        reactions_df["reaction"]
        .value_counts()
        .head(top_n)
        .sort_values()
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        top_reactions.index,
        top_reactions.values
    )

    plt.title(f"Top {top_n} Adverse Reactions")
    plt.xlabel("Number of Reports")
    plt.ylabel("Reaction")

    plt.tight_layout()
    plt.show()


# 3. CASES BY AGE GROUP

def plot_cases_by_age_group(cases_df):

    age_counts = (
        cases_df["age_group"]
        .value_counts()
    )

   
    order = ["0-17","18-40","41-64","65+","Unknown" ]

    age_counts = age_counts.reindex( order).fillna(0)

    plt.figure(figsize=(8, 5))

    plt.bar(
        age_counts.index,
        age_counts.values
    )

    plt.title("Cases by Age Group")
    plt.xlabel("Age Group")
    plt.ylabel("Number of Cases")

    plt.tight_layout()
    plt.show()


# 4. OUTCOME DISTRIBUTION

def plot_outcome_distribution(reactions_df):

    outcomes = (
        reactions_df["outcome"]
        .value_counts()
        .sort_values()
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        outcomes.index,
        outcomes.values
    )

    plt.title("Outcome Distribution")
    plt.xlabel("Number of Reactions")
    plt.ylabel("Outcome")

    plt.tight_layout()
    plt.show()


# 5. REACTIONS BY AGE GROUP


def plot_reactions_by_age_group(
    reactions_df,
    cases_df,
    top_n=5
):

    merged_df = reactions_df.merge(
        cases_df[
            [
                "safetyreportid",
                "age_group"
            ] ], on="safetyreportid", how="left" )

    age_groups = [ "0-17", "18-40", "41-64", "65+", "Unknown" ]

    for group in age_groups:

        group_data = merged_df[
            merged_df["age_group"] == group]

        if group_data.empty:
            continue

        top_reactions = ( group_data["reaction"] .value_counts() .head(top_n) .sort_values())

        plt.figure(figsize=(9, 5))

        plt.barh(top_reactions.index,top_reactions.values
        )

        plt.title(
            f"Top {top_n} Reactions — Age Group {group}"
        )

        plt.xlabel("Number of Reactions")
        plt.ylabel("Reaction")

        plt.tight_layout()
        plt.show()


# 6. OUTCOME BY AGE GROUP

def plot_outcome_by_age_group(
    cases_df,
    reactions_df
):

    merged_df = reactions_df.merge(cases_df[
            [
                "safetyreportid",
                "age_group"
            ]],
        on="safetyreportid",
        how="left"
    )

    outcome_table = pd.crosstab(
        merged_df["age_group"],
        merged_df["outcome"]
    )

    order = ["0-17","18-40","41-64","65+","Unknown"]

    outcome_table = outcome_table.reindex(order).fillna(0)

    ax = outcome_table.plot(kind="bar",stacked=True,figsize=(11, 6))

    ax.set_title("Outcomes by Age Group")
    ax.set_xlabel("Age Group")
    ax.set_ylabel("Number of Reactions")

    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()