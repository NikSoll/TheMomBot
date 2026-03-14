from config3 import QUIZZES


def get_quiz_by_id(quiz_id):
    return next((q for q in QUIZZES if q["id"] == quiz_id), None)


def format_results(results):
    if not results:
        return "Нет результатов"

    lines = []
    for i, res in enumerate(results[:5], 1):
        date = res.get('date', '')
        quiz = res.get('quiz_name', '')
        result = res.get('result', '')
        lines.append(f"{i}. *{quiz}*")
        lines.append(f"   📅 {date}")
        lines.append(f"   🏆 {result}\n")

    return "\n".join(lines)