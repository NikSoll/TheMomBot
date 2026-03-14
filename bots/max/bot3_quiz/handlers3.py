from datetime import datetime
from config3 import QUIZZES, MESSAGES
from . import keyboards3 as kb
from . import utils3
from .states3 import QuizStates
from .database3 import db

user_sessions = {}


def register_handlers(bot):
    @bot.on_message("text")
    async def message_handler(event):
        user_id = event.user_id
        text = event.text

        if text == "/start":
            await start_handler(event, bot)
        else:
            await start_handler(event, bot)

    @bot.on_callback("start")
    async def start_handler(event, bot=None):
        user_id = event.user_id
        if not QUIZZES:
            await event.bot.send_message(
                user_id=user_id,
                text=MESSAGES["no_quizzes"]
            )
            return

        await event.bot.send_message(
            user_id=user_id,
            text="Выберите квиз:",
            keyboard=kb.get_quizzes_keyboard()
        )

    @bot.on_callback("quizzes")
    async def quizzes_handler(event):
        user_id = event.user_id
        await event.bot.send_message(
            user_id=user_id,
            text="Выберите квиз:",
            keyboard=kb.get_quizzes_keyboard()
        )

    @bot.on_callback_pattern(r"quiz_(\d+)")
    async def quiz_selected_handler(event, quiz_id):
        user_id = event.user_id
        quiz = utils3.get_quiz_by_id(int(quiz_id))

        if quiz:
            user_sessions[user_id] = {
                "quiz_id": int(quiz_id),
                "current_q": 0,
                "answers": [],
                "points": {}
            }

            await event.bot.send_message(
                user_id=user_id,
                text=MESSAGES["quiz_start"].format(
                    name=quiz['name'],
                    description=quiz['description'],
                    questions=len(quiz['questions'])
                ),
                keyboard=kb.get_quiz_start_keyboard(int(quiz_id))
            )

    @bot.on_callback_pattern(r"start_quiz_(\d+)")
    async def start_quiz_handler(event, quiz_id):
        user_id = event.user_id
        await show_question(event.bot, user_id, int(quiz_id), 0)

    async def show_question(bot, user_id, quiz_id, q_index):
        quiz = utils3.get_quiz_by_id(quiz_id)
        if not quiz or q_index >= len(quiz['questions']):
            return

        question = quiz['questions'][q_index]
        text = MESSAGES["question"].format(
            current=q_index + 1,
            total=len(quiz['questions']),
            text=question['text']
        )

        await bot.send_message(
            user_id=user_id,
            text=text,
            keyboard=kb.get_question_keyboard(quiz_id, q_index, question)
        )

    @bot.on_callback_pattern(r"answer_(\d+)_(\d+)_(\d+)")
    async def answer_handler(event, quiz_id, q_index, answer_index):
        user_id = event.user_id
        quiz_id = int(quiz_id)
        q_index = int(q_index)
        answer_index = int(answer_index)

        quiz = utils3.get_quiz_by_id(quiz_id)
        if not quiz or q_index >= len(quiz['questions']):
            return

        question = quiz['questions'][q_index]
        selected_option = question['options'][answer_index]

        session = user_sessions.get(user_id, {})
        answers = session.get('answers', [])
        answers.append({
            'question': question['text'],
            'answer': selected_option['text']
        })

        points = session.get('points', {})
        for category, point_value in selected_option['points'].items():
            points[category] = points.get(category, 0) + point_value

        user_sessions[user_id] = {
            "quiz_id": quiz_id,
            "current_q": q_index + 1,
            "answers": answers,
            "points": points
        }

        next_q = q_index + 1
        if next_q < len(quiz['questions']):
            await show_question(event.bot, user_id, quiz_id, next_q)
        else:
            await show_result(event.bot, user_id, quiz_id)

    async def show_result(bot, user_id, quiz_id):
        session = user_sessions.get(user_id, {})
        points = session.get('points', {})

        quiz = utils3.get_quiz_by_id(quiz_id)
        result_type = max(points, key=points.get) if points else None
        result = next((r for r in quiz['results'] if r['type'] == result_type), None)

        result_text = result['text'] if result else "Результат не определен"

        # Сохранение в БД
        db.save_result({
            'user_id': user_id,
            'username': "",
            'quiz_id': quiz_id,
            'quiz_name': quiz['name'],
            'result': result_text,
            'points': points,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        await bot.send_message(
            user_id=user_id,
            text=MESSAGES["result"].format(result=result_text),
            keyboard=kb.get_after_quiz_keyboard()
        )

        user_sessions.pop(user_id, None)

    @bot.on_callback("my_results")
    async def my_results_handler(event):
        user_id = event.user_id
        results = db.get_user_results(user_id)

        if not results:
            await event.bot.send_message(
                user_id=user_id,
                text=MESSAGES["no_results"]
            )
            return

        text = utils3.format_results(results)
        await event.bot.send_message(
            user_id=user_id,
            text=text
        )