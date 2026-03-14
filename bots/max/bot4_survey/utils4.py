import json
from config4 import SURVEYS


def get_survey_by_id(survey_id):
    return next((s for s in SURVEYS if s["id"] == survey_id), None)


def format_surveys_list(surveys):
    if not surveys:
        return "Нет пройденных опросов"

    lines = []
    for i, survey in enumerate(surveys[:5], 1):
        date = survey.get('date', '')
        name = survey.get('survey_name', '')
        lines.append(f"{i}. *{name}*")
        lines.append(f"   📅 {date}\n")

    return "\n".join(lines)