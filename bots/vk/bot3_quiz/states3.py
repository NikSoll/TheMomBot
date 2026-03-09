from aiogram.fsm.state import State, StatesGroup

class QuizStates(StatesGroup):
    quiz_start = State()
    answering = State()