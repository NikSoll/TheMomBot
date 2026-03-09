from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime

from . import keyboards4 as kb
from . import utils4
from .states4 import SurveyStates
from .config4 import SURVEYS, MESSAGES
from .database4 import db

user_sessions = {}


def register_handlers(dp):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(
            MESSAGES["welcome"],
            reply_markup=kb.get_main_menu(),
            parse_mode="Markdown"
        )

    @dp.message(F.text == "📋 Пройти опрос")
    async def show_surveys(message: types.Message):
        if not SURVEYS:
            await message.answer(MESSAGES["no_surveys"])
            return

        await message.answer(
            MESSAGES["surveys_list"],
            reply_markup=kb.get_surveys_keyboard(),
            parse_mode="Markdown"
        )

    @dp.callback_query(F.data.startswith("survey_"))
    async def start_survey(callback: types.CallbackQuery, state: FSMContext):
        survey_id = int(callback.data.split("_")[1])
        survey = utils4.get_survey_by_id(survey_id)

        if not survey:
            await callback.answer("Опрос не найден")
            return

        await state.update_data(
            survey_id=survey_id,
            current_q=0,
            answers=[],
            multiple_answers=[]
        )

        await callback.message.edit_text(
            MESSAGES["survey_start"].format(
                name=survey['name'],
                description=survey['description'],
                questions=len(survey['questions'])
            ),
            reply_markup=kb.get_survey_start_keyboard(survey_id),
            parse_mode="Markdown"
        )
        await state.set_state(SurveyStates.survey_start)
        await callback.answer()

    @dp.callback_query(F.data.startswith("start_survey_"), SurveyStates.survey_start)
    async def begin_survey(callback: types.CallbackQuery, state: FSMContext):
        survey_id = int(callback.data.split("_")[2])
        data = await state.get_data()

        if data.get('survey_id') != survey_id:
            await callback.answer("Ошибка")
            return

        await show_question(callback.message, state, survey_id, 0)
        await state.set_state(SurveyStates.answering)
        await callback.answer()

    async def show_question(message: types.Message, state: FSMContext, survey_id, q_index):
        survey = utils4.get_survey_by_id(survey_id)
        if not survey or q_index >= len(survey['questions']):
            return

        question = survey['questions'][q_index]
        data = await state.get_data()
        multiple_answers = data.get('multiple_answers', [])

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
            reply_markup = kb.get_multiple_choice_keyboard(survey_id, q_index, question['options'])

        elif question['type'] == 'scale':
            text = MESSAGES["question_scale"].format(
                current=q_index + 1,
                total=len(survey['questions']),
                text=question['text'],
                min=question['min'],
                max=question['max']
            )
            reply_markup = kb.get_scale_keyboard(survey_id, q_index, question['min'], question['max'])

        await message.edit_text(text, reply_markup=reply_markup, parse_mode="Markdown")

    @dp.callback_query(F.data.startswith("single_"), SurveyStates.answering)
    async def process_single_answer(callback: types.CallbackQuery, state: FSMContext):
        parts = callback.data.split("_")
        survey_id = int(parts[1])
        q_index = int(parts[2])
        answer_index = int(parts[3])

        survey = utils4.get_survey_by_id(survey_id)
        question = survey['questions'][q_index]
        answer_text = question['options'][answer_index]

        data = await state.get_data()
        answers = data.get('answers', [])
        answers.append({
            'question': question['text'],
            'answer': answer_text,
            'type': 'single'
        })
        await state.update_data(answers=answers)

        await go_to_next_question(callback.message, state, survey_id, q_index)
        await callback.answer()

    @dp.callback_query(F.data.startswith("multiple_"), SurveyStates.answering)
    async def process_multiple_answer(callback: types.CallbackQuery, state: FSMContext):
        parts = callback.data.split("_")
        survey_id = int(parts[1])
        q_index = int(parts[2])
        action = parts[3]

        survey = utils4.get_survey_by_id(survey_id)
        question = survey['questions'][q_index]

        data = await state.get_data()
        multiple_answers = data.get('multiple_answers', [])

        if action == "select":
            option_index = int(parts[4])
            option_text = question['options'][option_index]

            if option_index in multiple_answers:
                multiple_answers.remove(option_index)
            else:
                multiple_answers.append(option_index)

            await state.update_data(multiple_answers=multiple_answers)

            await callback.message.edit_reply_markup(
                reply_markup=kb.get_multiple_choice_keyboard(
                    survey_id, q_index, question['options'], multiple_answers
                )
            )

        elif action == "done":
            if multiple_answers:
                selected_options = [question['options'][i] for i in multiple_answers]
                answers = data.get('answers', [])
                answers.append({
                    'question': question['text'],
                    'answer': ", ".join(selected_options),
                    'type': 'multiple',
                    'selected': selected_options
                })
                await state.update_data(answers=answers, multiple_answers=[])

                await go_to_next_question(callback.message, state, survey_id, q_index)

        await callback.answer()

    @dp.callback_query(F.data.startswith("scale_"), SurveyStates.answering)
    async def process_scale_answer(callback: types.CallbackQuery, state: FSMContext):
        parts = callback.data.split("_")
        survey_id = int(parts[1])
        q_index = int(parts[2])
        value = int(parts[3])

        survey = utils4.get_survey_by_id(survey_id)
        question = survey['questions'][q_index]

        data = await state.get_data()
        answers = data.get('answers', [])
        answers.append({
            'question': question['text'],
            'answer': value,
            'type': 'scale'
        })
        await state.update_data(answers=answers)

        await go_to_next_question(callback.message, state, survey_id, q_index)
        await callback.answer()

    @dp.message(SurveyStates.answering)
    async def process_text_answer(message: types.Message, state: FSMContext):
        data = await state.get_data()
        survey_id = data.get('survey_id')
        q_index = data.get('current_q', 0)

        survey = utils4.get_survey_by_id(survey_id)
        if not survey:
            return

        question = survey['questions'][q_index]
        answers = data.get('answers', [])
        answers.append({
            'question': question['text'],
            'answer': message.text,
            'type': 'text'
        })
        await state.update_data(answers=answers)

        await go_to_next_question(message, state, survey_id, q_index)

    async def go_to_next_question(message: types.Message, state: FSMContext, survey_id, q_index):
        survey = utils4.get_survey_by_id(survey_id)
        next_q = q_index + 1

        if next_q < len(survey['questions']):
            await state.update_data(current_q=next_q)
            await show_question(message, state, survey_id, next_q)
        else:
            await finish_survey(message, state, survey_id)

    async def finish_survey(message: types.Message, state: FSMContext, survey_id):
        data = await state.get_data()
        survey = utils4.get_survey_by_id(survey_id)

        survey_result = {
            'user_id': message.chat.id,
            'username': message.chat.username or "",
            'survey_id': survey_id,
            'survey_name': survey['name'],
            'answers': data.get('answers', []),
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        db.save_survey_result(survey_result)

        await message.edit_text(
            MESSAGES["thanks"],
            reply_markup=kb.get_after_survey_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()

    @dp.message(F.text == "📋 Мои опросы")
    async def my_surveys(message: types.Message):
        results = db.get_user_surveys(message.from_user.id)

        if not results:
            await message.answer(MESSAGES["no_surveys_taken"])
            return

        text = utils4.format_surveys_list(results)
        await message.answer(text, parse_mode="Markdown")