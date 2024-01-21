from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types
from states import Worker
from init import database, worker_dict

router = Router()


@router.message(StateFilter(Worker.account), Command("exit"))
async def account_company(message: types.Message, state: FSMContext):
    await state.set_state(None)
    worker_dict.pop(message.text, None)
    await message.answer("Здравствуйте! У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                         "личный кабинет \n/list - посмотреть определенную таблицу")

