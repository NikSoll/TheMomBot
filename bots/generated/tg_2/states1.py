from aiogram.fsm.state import State, StatesGroup

class BookingStates(StatesGroup):
    choosing_master = State()
    choosing_date = State()
    choosing_time = State()
    entering_name = State()
    entering_phone = State()
    entering_comment = State()