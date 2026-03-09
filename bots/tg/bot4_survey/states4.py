from aiogram.fsm.state import State, StatesGroup

class SurveyStates(StatesGroup):
    survey_start = State()
    answering = State()