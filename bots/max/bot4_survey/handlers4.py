from datetime import datetime
from config4 import SURVEYS, MESSAGES
from . import keyboards4 as kb
from . import utils4
from .states4 import SurveyStates
from .database4 import db

user_sessions = {}


def register_handlers(bot):
    @bot.on_message("text")
    async def message_handler(event):
        user_id = event.user_id
        text = event.text
        session = user_sessions.get(user_id, {"state": None})

        if text == "/start":
            await start_handler(event, bot)
        elif session.get("state") == SurveyStates.ANSWERING:
            await process_text_answer(event, bot)
        else:
            await start_handler(event, bot)

    @bot.on_callback("start")
    async def start_handler(event, bot=None):
        user_id = event.user_id
        if not SURVEYS:
            await event.bot.send_message(
                user_id=user_id,
                text=MESSAGES["no_surveys"]
            )
            return

        await event.bot.send_message(
            user_id=user_id,
            text=MESSAGES["surveys_list"],
            keyboard=kb.get_surveys_keyboard()
        )

    @bot.on_callback("surveys")
    async def surveys_handler(event):
        user_id = event.user_id
        await event.bot.send_message(
            user_id=user_id,
            text=MESSAGES["surveys_list"],
            keyboard=kb.get_surveys_keyboard()
        )

    @bot.on_callback_pattern(r"survey_(\d+)")
    async def survey_selected_handler(event, survey_id):
        user_id = event.user_id
        survey = utils4.get_survey_by_id(int(survey_id))

        if survey:
            user_sessions[user_id] = {
                "survey_id": int(survey_id),
                "current_q": 0,
                "answers": [],
                "multiple_answers": []
            }

            await event.bot.send_message(
                user_id=user_id,
                text=MESSAGES["survey_start"].format(
                    name=survey['name'],
                    description=survey['description'],
                    questions=len(survey['questions'])
                ),
                keyboard=kb.get_survey_start_keyboard(int(survey_id))
            )

    @bot.on_callback_pattern(r"start_survey_(\d+)")
    async def start_survey_handler(event, survey_id):
        user_id = event.user_id
        await show_question(event.bot, user_id, int(survey_id), 0)

    async def show_question(bot, user_id, survey_id, q_index):
        survey = utils4.get_survey_by_id(survey_id)
        if not survey or q_index >= len(survey['questions']):
            return

        question = survey['questions'][q_index]
        session = user_sessions.get(user_id, {})

        if question['type'] == 'text':
            text = MESSAGES["question_text"].format(
                current=q_index + 1,
                total=len(survey['questions']),
                text=question['text']
            )
            reply_markup = None

        elif question['type'] == 'single':
            text = MESSAGES["question_single"].format(
                current=q_index + 1,
                total=len(survey['questions']),
                text=question['text']
            )
            reply_markup = kb.get_single_choice_keyboard(survey_id, q_index, question['options'])

        elif question['type'] == 'multiple':
            text = MESSAGES["question_multiple"].format(
                current=q_index + 1,
                total=len(survey['questions']),
                text=question['text']
            )
            multiple_answers = session.get('multiple_answers', [])
            reply_markup = kb.get_multiple_choice_keyboard(survey_id, q_index, question['options'], multiple_answers)

        elif question['type'] == 'scale':
            text = MESSAGES["question_scale"].format(
                current=q_index + 1,
                total=len(survey['questions']),
                text=question['text'],
                min=question['min'],
                max=question['max']
            )
            reply_markup = kb.get_scale_keyboard(survey_id, q_index, question['min'], question['max'])

        await bot.send_message(
            user_id=user_id,
            text=text,
            keyboard=reply_markup
        )

    @bot.on_callback_pattern(r"single_(\d+)_(\d+)_(\d+)")
    async def single_answer_handler(event, survey_id, q_index, answer_index):
        user_id = event.user_id
        survey_id = int(survey_id)
        q_index = int(q_index)
        answer_index = int(answer_index)

        survey = utils4.get_survey_by_id(survey_id)
        question = survey['questions'][q_index]
        answer_text = question['options'][answer_index]

        session = user_sessions.get(user_id, {})
        answers = session.get('answers', [])
        answers.append({
            'question': question['text'],
            'answer': answer_text,
            'type': 'single'
        })
        user_sessions[user_id]['answers'] = answers

        await go_to_next_question(event.bot, user_id, survey_id, q_index)

    @bot.on_callback_pattern(r"multiple_(\d+)_(\d+)_select_(\d+)")
    async def multiple_select_handler(event, survey_id, q_index, option_index):
        user_id = event.user_id
        survey_id = int(survey_id)
        q_index = int(q_index)
        option_index = int(option_index)

        session = user_sessions.get(user_id, {})
        multiple_answers = session.get('multiple_answers', [])

        if option_index in multiple_answers:
            multiple_answers.remove(option_index)
        else:
            multiple_answers.append(option_index)

        user_sessions[user_id]['multiple_answers'] = multiple_answers

        survey = utils4.get_survey_by_id(survey_id)
        question = survey['questions'][q_index]

        await event.bot.send_message(
            user_id=user_id,
            text="✓ Выбор обновлен. Продолжайте выбирать или нажмите Готово.",
            keyboard=kb.get_multiple_choice_keyboard(survey_id, q_index, question['options'], multiple_answers)
        )

    @bot.on_callback_pattern(r"multiple_(\d+)_(\d+)_done")
    async def multiple_done_handler(event, survey_id, q_index):
        user_id = event.user_id
        survey_id = int(survey_id)
        q_index = int(q_index)

        session = user_sessions.get(user_id, {})
        multiple_answers = session.get('multiple_answers', [])

        survey = utils4.get_survey_by_id(survey_id)
        question = survey['questions'][q_index]
        selected_options = [question['options'][i] for i in multiple_answers]

        answers = session.get('answers', [])
        answers.append({
            'question': question['text'],
            'answer': ", ".join(selected_options),
            'type': 'multiple',
            'selected': selected_options
        })
        user_sessions[user_id]['answers'] = answers
        user_sessions[user_id]['multiple_answers'] = []

        await go_to_next_question(event.bot, user_id, survey_id, q_index)

    @bot.on_callback_pattern(r"scale_(\d+)_(\d+)_(\d+)")
    async def scale_answer_handler(event, survey_id, q_index, value):
        user_id = event.user_id
        survey_id = int(survey_id)
        q_index = int(q_index)
        value = int(value)

        survey = utils4.get_survey_by_id(survey_id)
        question = survey['questions'][q_index]

        session = user_sessions.get(user_id, {})
        answers = session.get('answers', [])
        answers.append({
            'question': question['text'],
            'answer': value,
            'type': 'scale'
        })
        user_sessions[user_id]['answers'] = answers

        await go_to_next_question(event.bot, user_id, survey_id, q_index)

    async def process_text_answer(event, bot):
        user_id = event.user_id
        session = user_sessions.get(user_id, {})
        survey_id = session.get('survey_id')
        q_index = session.get('current_q', 0)

        survey = utils4.get_survey_by_id(survey_id)
        if not survey:
            return

        question = survey['questions'][q_index]
        answers = session.get('answers', [])
        answers.append({
            'question': question['text'],
            'answer': event.text,
            'type': 'text'
        })
        user_sessions[user_id]['answers'] = answers

        await go_to_next_question(bot, user_id, survey_id, q_index)

    async def go_to_next_question(bot, user_id, survey_id, q_index):
        survey = utils4.get_survey_by_id(survey_id)
        next_q = q_index + 1

        if next_q < len(survey['questions']):
            user_sessions[user_id]['current_q'] = next_q
            await show_question(bot, user_id, survey_id, next_q)
        else:
            await finish_survey(bot, user_id, survey_id)

    async def finish_survey(bot, user_id, survey_id):
        session = user_sessions.get(user_id, {})
        survey = utils4.get_survey_by_id(survey_id)

        survey_result = {
            'user_id': user_id,
            'username': "",
            'survey_id': survey_id,
            'survey_name': survey['name'],
            'answers': session.get('answers', []),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        db.save_survey_result(survey_result)

        await bot.send_message(
            user_id=user_id,
            text=MESSAGES["thanks"],
            keyboard=kb.get_after_survey_keyboard()
        )

        user_sessions.pop(user_id, None)

    @bot.on_callback("my_surveys")
    async def my_surveys_handler(event):
        user_id = event.user_id
        results = db.get_user_surveys(user_id)

        if not results:
            await event.bot.send_message(
                user_id=user_id,
                text=MESSAGES["no_surveys_taken"]
            )
            return

        text = utils4.format_surveys_list(results)
        await event.bot.send_message(
            user_id=user_id,
            text=text
        )