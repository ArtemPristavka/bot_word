from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class FormRegisterFSM(StatesGroup):
    "FSM для регистарции пользователя"
    
    start_register = State()
    password_1 = State()
    password_2 = State()