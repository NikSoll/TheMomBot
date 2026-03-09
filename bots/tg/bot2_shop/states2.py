from aiogram.fsm.state import State, StatesGroup

class ShopStates(StatesGroup):
    browsing = State()           #просмотр каталога
    viewing_product = State()    #просмотр конкретного товара
    in_cart = State()            #просмотр корзины
    entering_name = State()      #ввод имени
    entering_phone = State()     #ввод телефона
    entering_address = State()   #ввод адреса
    entering_comment = State()   #ввод комментария