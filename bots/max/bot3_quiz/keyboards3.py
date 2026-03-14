from config3 import QUIZZES

def get_main_menu():
    return [
        [{"text": "🎯 Квизы", "data": "quizzes"}],
        [{"text": "📊 Мои результаты", "data": "my_results"}],
    ]

def get_quizzes_keyboard():
    keyboard = []
    for quiz in QUIZZES:
        keyboard.append([{
            "text": quiz['name'],
            "data": f"quiz_{quiz['id']}"
        }])
    return keyboard

def get_quiz_start_keyboard(quiz_id):
    return [[{"text": "▶️ Начать квиз", "data": f"start_quiz_{quiz_id}"}]]

def get_question_keyboard(quiz_id, q_index, question):
    keyboard = []
    for i, option in enumerate(question['options']):
        keyboard.append([{
            "text": option['text'],
            "data": f"answer_{quiz_id}_{q_index}_{i}"
        }])
    return keyboard

def get_after_quiz_keyboard():
    return [[{"text": "🎯 Другие квизы", "data": "quizzes"}]]