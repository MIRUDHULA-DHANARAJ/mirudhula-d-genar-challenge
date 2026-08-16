import pandas as pd


def case_summary(cases_df):
    total = len(cases_df)
    serious = len(cases_df[cases_df["serious"] == "serious"])
    non_serious = total - serious
    return {
        "total_cases": total,
        "serious_cases": serious,
        "non_serious_cases": non_serious,
    }


def demographic_summary(cases_df):
    return {
        "age_groups": cases_df["age_group"].value_counts(dropna=False).to_dict(),
        "sex": cases_df["patient_patientsex"].fillna("unknown").value_counts().to_dict(),
        "countries": cases_df["occurcountry"].fillna("unknown").value_counts().to_dict(),
    }


def top_reactions(reactions_df, n=15):
    return reactions_df["reaction"].value_counts().head(n).to_dict()


def top_serious_reactions(reactions_df, n=15):
    serious = reactions_df[reactions_df["serious"] == "serious"]
    return serious["reaction"].value_counts().head(n).to_dict()


def outcome_summary(reactions_df):
    return reactions_df["outcome"].fillna("unknown").value_counts().to_dict()


def monthly_trend(cases_df):
    dates = pd.to_datetime(cases_df["receivedate"], format="%Y%m%d", errors="coerce")
    monthly = dates.dt.to_period("M").value_counts().sort_index()
    return {str(k): int(v) for k, v in monthly.items()}


def alert_summary(cases_df):
    alerts = cases_df[cases_df["fulfillexpeditecriteria"] == "yes"]

    return {
        "total_alert_cases": len(alerts),
        "death": int((alerts["seriousnessdeath"] == "yes").sum()),
        "life_threatening": int((alerts["seriousnesslifethreatening"] == "yes").sum()),
        "hospitalization": int((alerts["seriousnesshospitalization"] == "yes").sum()),
        "disabling": int((alerts["seriousnessdisabling"] == "yes").sum()),
        "congenital_anomaly": int((alerts["seriousnesscongenitalanomali"] == "yes").sum()),
        "other": int((alerts["seriousnessother"] == "yes").sum()),
    }


def case_index(cases_df, reactions_df):
    # one row per case: reactions joined together, for the report's appendix table
    reactions_by_case = (
        reactions_df.groupby("safetyreportid")["reaction"]
        .apply(lambda x: "; ".join(sorted(set(x))))
        .to_dict()
    )
    outcomes_by_case = (
        reactions_df.groupby("safetyreportid")["outcome"]
        .apply(lambda x: "; ".join(sorted(set(x))))
        .to_dict()
    )

    rows = []
    for _, row in cases_df.iterrows():
        rid = row["safetyreportid"]
        rows.append({
            "case_id": int(rid),
            "reactions": reactions_by_case.get(rid, ""),
            "seriousness": row["serious"],
            "outcome": outcomes_by_case.get(rid, ""),
            "country": row["occurcountry"],
            "date": str(row["receivedate"]),
        })

    return sorted(rows, key=lambda r: r["date"])


def reporting_period(cases_df):
    dates = pd.to_datetime(cases_df["receivedate"], format="%Y%m%d", errors="coerce")
    return {
        "start_date": dates.min().date().isoformat(),
        "end_date": dates.max().date().isoformat(),
    }