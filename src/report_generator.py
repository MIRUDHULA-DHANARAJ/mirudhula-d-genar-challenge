import argparse
import json

from data_loader import load_data
import analysis as an
import context_builder as ctx
import prompts
import human_review as hr
import llm_client

PRODUCT_NAME = "Bisoprolol"

# Offline text: same prompts above, run by hand through Claude since this
# machine has no ANTHROPIC_API_KEY. --online mode calls the real API with
# the exact same prompts if you have a key.
OFFLINE_TEXT = {
    "narrative_summary": (
        "During the reporting period of 2024-12-27 to 2025-12-26, 1,024 cases involving "
        "Bisoprolol were received, of which 1,023 (99.9%) were classified as serious and 1 "
        "(0.1%) as non-serious.\n\n"
        "The most frequently reported reactions overall were Acute kidney injury (80 cases), "
        "Drug ineffective (54 cases), Hypotension (46 cases), Drug interaction (42 cases), and "
        "Dyspnoea (38 cases). Among serious cases specifically, the same five reactions led, "
        "with Drug ineffective at 53 of its 54 reports being serious.\n\n"
        "Reported outcomes were: recovered/resolved (1,280), unknown (1,033), not "
        "recovered/ongoing (536), recovering/resolving (406), fatal (134), and "
        "recovered with sequelae (34). The case population was close to evenly split by sex "
        "(503 female, 493 male, 28 unknown) and skewed toward older patients (674 aged 65+, "
        "218 aged 41-64). The leading reporting sources were the EU region (342), United "
        "Kingdom (278), and France (185)."
    ),
    "summary_analysis": (
        "The dataset comprises 1,024 unique cases after deduplicating resubmitted case "
        "versions, of which 1,023 (99.9%) were serious and 1 non-serious.\n\n"
        "By age group, the population is predominantly 65+ (674 cases), followed by 41-64 "
        "(218), unknown (86), 18-40 (30), and 0-17 (16). By sex, cases are nearly even: 503 "
        "female, 493 male, 28 unknown. By country, the leading sources are the EU region "
        "(342), United Kingdom (278), and France (185), with the remainder spread across "
        "Canada, Italy, Germany, Spain, Poland, and Portugal."
    ),
    "reaction_analysis": (
        "The most frequently reported reactions, at the MedDRA Preferred Term level, were "
        "Acute kidney injury (80), Drug ineffective (54), Hypotension (46), Drug interaction "
        "(42), and Dyspnoea (38). Restricted to serious cases only, the ranking is nearly "
        "identical, indicating reactions for this product are reported almost entirely in "
        "the context of serious cases.\n\n"
        "No System Organ Class field exists in the source data, only MedDRA Preferred Term. "
        "Reactions are therefore reported at the Preferred Term level only; SOC-level "
        "grouping was not attempted."
    ),
    "alerts": (
        "1,023 cases met 15-day Alert (expedited) reporting criteria during the period. "
        "Within these, cases met one or more of the following seriousness criteria: other "
        "medically important (905), hospitalization (482), life-threatening (105), death "
        "(68), disabling (44), and congenital anomaly (7). These criteria are independent "
        "flags, not mutually exclusive, so a case may meet more than one and the breakdown "
        "does not sum to the total of 1,023."
    ),
    "trends": (
        "Case volume varied month to month across the 13-month reporting window rather than "
        "following a single steady trend. This is an observation of reporting volume over "
        "time, not a safety conclusion -- whether any month-to-month change is meaningful is "
        "a determination for a qualified human reviewer."
    ),
    "history_of_actions": (
        "No history-of-actions data (labeling changes, safety studies, regulatory "
        "communications, or risk-minimization measures) was supplied for this reporting "
        "period. No actions are reported in this section."
    ),
}


def generate_all(cases_df, reactions_df, online):
    contexts = {
        "narrative_summary": ctx.narrative_summary_context(cases_df, reactions_df),
        "summary_analysis": ctx.summary_analysis_context(cases_df),
        "reaction_analysis": ctx.reaction_analysis_context(reactions_df),
        "alerts": ctx.alerts_context(cases_df),
        "trends": ctx.trends_context(cases_df),
        "history_of_actions": ctx.history_of_actions_context(),
    }

    for section_id, data in contexts.items():
        user_prompt = prompts.TEMPLATES[section_id].format(data=json.dumps(data, indent=2))

        if online:
            text = llm_client.generate_section(prompts.SYSTEM_PROMPT, user_prompt)
        else:
            text = OFFLINE_TEXT[section_id]

        hr.submit(section_id, text)

    print("sections generated and queued for review. run: python human_review.py list")


def section_text(queue, section_id):
    item = queue.get(section_id)
    if not item:
        return "[NOT GENERATED YET]"
    if item["status"] == "approved":
        return item["text"]
    banner = f"[{item['status'].upper()} - NOT APPROVED YET]"
    if item.get("note"):
        banner += f" ({item['note']})"
    return banner + "\n\n" + item["text"]


def build_report(cases_df, reactions_df):
    queue = hr.load_queue()
    period = an.reporting_period(cases_df)
    case_stats = an.case_summary(cases_df)
    alert_stats = an.alert_summary(cases_df)

    lines = []
    lines.append(f"# Periodic Adverse Drug Experience Report (PADER)\n")
    lines.append(f"**Product:** {PRODUCT_NAME}")
    lines.append(f"**Reporting Period:** {period['start_date']} to {period['end_date']}")
    lines.append(f"**Total Cases:** {case_stats['total_cases']}\n")
    lines.append("---\n")

    lines.append("## 1. Reporting Period\n")
    lines.append(f"- Product: {PRODUCT_NAME}")
    lines.append(f"- Reporting period: {period['start_date']} to {period['end_date']}")
    lines.append(f"- Total cases: {case_stats['total_cases']}\n")

    lines.append("## 2. Narrative Summary and Analysis\n")
    lines.append(section_text(queue, "narrative_summary") + "\n")

    lines.append("## 3. Summary Analysis of Cases\n")
    lines.append(section_text(queue, "summary_analysis") + "\n")

    lines.append("## 4. Reaction / Adverse Event Analysis\n")
    lines.append(section_text(queue, "reaction_analysis") + "\n")
    lines.append("| Reaction | Count |")
    lines.append("|---|---|")
    for reaction, count in an.top_reactions(reactions_df, 15).items():
        lines.append(f"| {reaction} | {count} |")
    lines.append("")

    lines.append("## 5. Serious Cases / 15-Day Alerts\n")
    lines.append(section_text(queue, "alerts") + "\n")
    lines.append("| Criterion | Count |")
    lines.append("|---|---|")
    for k, v in alert_stats.items():
        if k != "total_alert_cases":
            lines.append(f"| {k.replace('_', ' ').title()} | {v} |")
    lines.append("")

    lines.append("## 6. Trends and Important Observations\n")
    lines.append(section_text(queue, "trends") + "\n")
    lines.append("| Month | Cases |")
    lines.append("|---|---|")
    for month, count in an.monthly_trend(cases_df).items():
        lines.append(f"| {month} | {count} |")
    lines.append("")

    lines.append("## 7. History of Actions\n")
    lines.append(section_text(queue, "history_of_actions") + "\n")

    lines.append("## 8. Case Index / Listing\n")
    lines.append("| Case ID | Reactions | Seriousness | Date | Country | Outcome |")
    lines.append("|---|---|---|---|---|---|")
    for row in an.case_index(cases_df, reactions_df):
        lines.append(
            f"| {row['case_id']} | {row['reactions'][:80]} | {row['seriousness']} | "
            f"{row['date']} | {row['country']} | {row['outcome']} |"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true")
    parser.add_argument("--render-only", action="store_true")
    parser.add_argument("--out", default="report_output.md")
    args = parser.parse_args()

    cases_df, reactions_df = load_data()

    if not args.render_only:
        generate_all(cases_df, reactions_df, online=args.online)
        return

    report = build_report(cases_df, reactions_df)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report)
    print("report written to", args.out)


if __name__ == "__main__":
    main()