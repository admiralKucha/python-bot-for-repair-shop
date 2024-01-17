from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types

router = Router()


@router.message(StateFilter(None), Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Здравствуйте! У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                         "личный кабинет \n/list - посмотреть определенную таблицу")


@router.message(StateFilter(None), Command("auth"))
async def cmd_auth(message: types.Message):
    await message.answer("Что желаете?\n/create - создать аккаунт\n/login - авторизоваться")


@router.message(StateFilter(None), Command("list"))
async def show_list(message: types.Message, state: FSMContext):
    await message.answer("Какую ")