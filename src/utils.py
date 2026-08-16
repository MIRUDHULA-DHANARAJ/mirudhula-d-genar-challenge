import pandas as pd


def normalize_age(age, unit):
    if unit == "year":
        return age
    elif unit == "month":
        return age / 12
    elif unit == "week":
        return age / 52
    elif unit == "day":
        return age / 365
    else:
        return None


def age_group(age):
    if pd.isna(age):
        return "Unknown"
    elif age <= 17:
        return "0-17"
    elif age <= 40:
        return "18-40"
    elif age <= 64:
        return "41-64"
    else:
        return "65+"