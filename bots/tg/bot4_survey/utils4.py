import json


def get_survey_by_id(survey_id):
    from .config4 import SURVEYS
    return next((s for s in SURVEYS if s["id"] == survey_id), None)


def format_surveys_list(surveys):
    if not surveys:
        return "Нет пройденных опросов"

    lines = []
    for i, survey in enumerate(surveys[:5], 1):
        date = survey.get('Дата', survey.get('date', ''))
        name = survey.get('Опрос', survey.get('survey_name', ''))

        lines.append(f"{i}. *{name}*")
        lines.append(f"   📅 {date}\n")

    if len(surveys) > 5:
        lines.append(f"_Показаны последние 5 из {len(surveys)} опросов_")

    return "\n".join(lines)