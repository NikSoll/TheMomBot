from config4 import SURVEYS


def get_main_menu():
    return [
        [{"text": "📋 Пройти опрос", "data": "surveys"}],
        [{"text": "📋 Мои опросы", "data": "my_surveys"}],
    ]


def get_surveys_keyboard():
    keyboard = []
    for survey in SURVEYS:
        keyboard.append([{
            "text": survey['name'],
            "data": f"survey_{survey['id']}"
        }])
    return keyboard


def get_survey_start_keyboard(survey_id):
    return [[{"text": "▶️ Начать опрос", "data": f"start_survey_{survey_id}"}]]


def get_single_choice_keyboard(survey_id, q_index, options):
    keyboard = []
    for i, option in enumerate(options):
        keyboard.append([{
            "text": option,
            "data": f"single_{survey_id}_{q_index}_{i}"
        }])
    return keyboard


def get_multiple_choice_keyboard(survey_id, q_index, options, selected=None):
    if selected is None:
        selected = []

    keyboard = []
    for i, option in enumerate(options):
        check = "✅ " if i in selected else ""
        keyboard.append([{
            "text": f"{check}{option}",
            "data": f"multiple_{survey_id}_{q_index}_select_{i}"
        }])
    keyboard.append([{
        "text": "✅ Готово",
        "data": f"multiple_{survey_id}_{q_index}_done"
    }])
    return keyboard


def get_scale_keyboard(survey_id, q_index, min_val, max_val):
    keyboard = []
    row = []
    for i in range(min_val, max_val + 1):
        row.append({"text": str(i), "data": f"scale_{survey_id}_{q_index}_{i}"})
        if len(row) == 5:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return keyboard


def get_after_survey_keyboard():
    return [[{"text": "📋 Другие опросы", "data": "surveys"}]]