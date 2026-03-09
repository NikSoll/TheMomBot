def get_quiz_by_id(quiz_id):
    from .config3 import QUIZZES
    return next((q for q in QUIZZES if q["id"] == quiz_id), None)


def format_results(results):
    if not results:
        return "Нет результатов"

    lines = []
    for i, res in enumerate(results[:5], 1):
        date = res.get('Дата', res.get('date', ''))
        quiz = res.get('Квиз', res.get('quiz_name', ''))
        result = res.get('Результат', res.get('result', ''))

        lines.append(f"{i}. *{quiz}*")
        lines.append(f"   📅 {date}")
        lines.append(f"   🏆 {result}\n")

    if len(results) > 5:
        lines.append(f"_Показаны последние 5 из {len(results)} результатов_")

    return "\n".join(lines)