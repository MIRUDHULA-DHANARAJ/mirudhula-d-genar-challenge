import analysis as an


def narrative_summary_context(cases_df, reactions_df):
    return {
        "reporting_period": an.reporting_period(cases_df),
        "case_summary": an.case_summary(cases_df),
        "top_reactions": an.top_reactions(reactions_df, 5),
        "top_serious_reactions": an.top_serious_reactions(reactions_df, 5),
        "outcomes": an.outcome_summary(reactions_df),
        "demographics": an.demographic_summary(cases_df),
    }


def summary_analysis_context(cases_df):
    return {
        "case_summary": an.case_summary(cases_df),
        "demographics": an.demographic_summary(cases_df),
    }


def reaction_analysis_context(reactions_df):
    return {
        "top_reactions": an.top_reactions(reactions_df, 15),
        "top_serious_reactions": an.top_serious_reactions(reactions_df, 15),
        "note": "No System Organ Class field exists in the source data, only "
                "MedDRA Preferred Term. Do not invent SOC groupings.",
    }


def alerts_context(cases_df):
    return {
        "alert_summary": an.alert_summary(cases_df),
        "note": "The seriousness criteria are independent yes/no flags, not "
                "mutually exclusive. They will not sum to total_alert_cases.",
    }


def trends_context(cases_df):
    return {
        "monthly_case_volume": an.monthly_trend(cases_df),
    }


def history_of_actions_context():
    return {
        "actions_provided": False,
        "note": "No history-of-actions data (labeling changes, studies, "
                "regulatory communications) was supplied for this exercise. "
                "State this plainly. Do not invent any actions.",
    }