from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class FormRegisterFSM(StatesGroup):
    "FSM для регистарции пользователя"
    
    start_register = State()
    password = State()
    
    
class FormTaskFSM(StatesGroup):
    "FSM для выполнения подсчета слов"
    
    start_task = State()
    
    
class FormAdminFSM(StatesGroup):
    "FSM для действий администратора"
    
    choice_action = State()
    choice_month = State()
    choice_day = State()
    