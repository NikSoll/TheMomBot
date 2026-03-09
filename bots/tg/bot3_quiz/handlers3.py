from aiogram import types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime

from . import keyboards3 as kb
from . import utils3
from .states3 import QuizStates
from .config3 import QUIZZES, MESSAGES
from .database3 import db

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

    @dp.message(F.text == "🎯 Квизы")
    async def show_quizzes(message: types.Message):
        if not QUIZZES:
            await message.answer(MESSAGES["no_quizzes"])
            return

        await message.answer(
            "Выберите квиз:",
            reply_markup=kb.get_quizzes_keyboard()
        )

    @dp.callback_query(F.data.startswith("quiz_"))
    async def start_quiz(callback: types.CallbackQuery, state: FSMContext):
        quiz_id = int(callback.data.split("_")[1])
        quiz = utils3.get_quiz_by_id(quiz_id)

        if not quiz:
            await callback.answer("Квиз не найден")
            return

        await state.update_data(
            quiz_id=quiz_id,
            current_q=0,
            answers=[],
            points={}
        )

        await callback.message.edit_text(
            MESSAGES["quiz_start"].format(
                name=quiz['name'],
                description=quiz['description'],
                questions=len(quiz['questions'])
            ),
            reply_markup=kb.get_quiz_start_keyboard(quiz_id),
            parse_mode="Markdown"
        )
        await state.set_state(QuizStates.quiz_start)
        await callback.answer()

    @dp.callback_query(F.data.startswith("start_quiz_"), QuizStates.quiz_start)
    async def begin_quiz(callback: types.CallbackQuery, state: FSMContext):
        quiz_id = int(callback.data.split("_")[2])
        data = await state.get_data()

        if data.get('quiz_id') != quiz_id:
            await callback.answer("Ошибка")
            return

        await show_question(callback.message, state, quiz_id, 0)
        await state.set_state(QuizStates.answering)
        await callback.answer()

    async def show_question(message: types.Message, state: FSMContext, quiz_id, q_index):
        quiz = utils3.get_quiz_by_id(quiz_id)
        if not quiz or q_index >= len(quiz['questions']):
            return

        question = quiz['questions'][q_index]
        data = await state.get_data()
        answers = data.get('answers', [])

        text = MESSAGES["question"].format(
            current=q_index + 1,
            total=len(quiz['questions']),
            text=question['text']
        )

        await message.edit_text(
            text,
            reply_markup=kb.get_question_keyboard(quiz_id, q_index, question),
            parse_mode="Markdown"
        )

    @dp.callback_query(F.data.startswith("answer_"), QuizStates.answering)
    async def process_answer(callback: types.CallbackQuery, state: FSMContext):
        parts = callback.data.split("_")
        quiz_id = int(parts[1])
        q_index = int(parts[2])
        answer_index = int(parts[3])

        quiz = utils3.get_quiz_by_id(quiz_id)
        if not quiz or q_index >= len(quiz['questions']):
            await callback.answer("Ошибка")
            return

        question = quiz['questions'][q_index]
        selected_option = question['options'][answer_index]

        data = await state.get_data()
        answers = data.get('answers', [])
        answers.append({
            'question': question['text'],
            'answer': selected_option['text']
        })

        points = data.get('points', {})
        for category, point_value in selected_option['points'].items():
            points[category] = points.get(category, 0) + point_value

        await state.update_data(answers=answers, points=points)

        next_q = q_index + 1
        if next_q < len(quiz['questions']):
            await show_question(callback.message, state, quiz_id, next_q)
        else:
            await show_result(callback.message, state, quiz_id)

        await callback.answer()

    async def show_result(message: types.Message, state: FSMContext, quiz_id):
        data = await state.get_data()
        points = data.get('points', {})

        quiz = utils3.get_quiz_by_id(quiz_id)
        result_type = max(points, key=points.get)
        result = next((r for r in quiz['results'] if r['type'] == result_type), None)

        if result:
            result_text = result['text']
        else:
            result_text = "Результат не определен"

        user_id = message.chat.id
        user_sessions[user_id] = {
            'quiz_id': quiz_id,
            'result': result_text,
            'points': points,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        db.save_result({
            'user_id': user_id,
            'username': message.chat.username or "",
            'quiz_id': quiz_id,
            'quiz_name': quiz['name'],
            'result': result_text,
            'points': points,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        await message.edit_text(
            MESSAGES["result"].format(result=result_text),
            reply_markup=kb.get_after_quiz_keyboard(),
            parse_mode="Markdown"
        )
        await state.clear()

    @dp.message(F.text == "📊 Мои результаты")
    async def my_results(message: types.Message):
        results = db.get_user_results(message.from_user.id)

        if not results:
            await message.answer(MESSAGES["no_results"])
            return

        text = utils3.format_results(results)
        await message.answer(text, parse_mode="Markdown")

    @dp.message(F.text == "🏠 Главное меню")
    async def main_menu(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(
            MESSAGES["welcome"],
            reply_markup=kb.get_main_menu()
        )