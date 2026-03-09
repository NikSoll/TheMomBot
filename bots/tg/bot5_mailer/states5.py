from aiogram.fsm.state import State, StatesGroup

class MailerStates(StatesGroup):
    choosing_group = State()
    entering_text = State()
    entering_photo = State()
    confirm = State()