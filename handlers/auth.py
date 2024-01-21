from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types
from states import Auth, Company, Customer, Worker
from init import database

router = Router()
user_dict = dict()


@router.message(StateFilter(None), Command("login"))
async def login(message: types.Message, state: FSMContext):
    await message.answer("Введите логин")
    await state.set_state(Auth.username)
    user_dict[message.from_user.id] = dict()


@router.message(Auth.username)
async def input_username(message: types.Message, state: FSMContext):
    await message.answer("Введите пароль")
    await state.set_state(Auth.password)
    user_dict[message.from_user.id]['login'] = message.text


@router.message(Auth.password)
async def input_password(message: types.Message, state: FSMContext):
    id_user = message.from_user.id
    user_dict[id_user]['password'] = message.text
    rest_temp = database.auth(user_dict[id_user]['login'],
                              user_dict[id_user]['password'])

    user_dict.pop(id_user, None)
    if not rest_temp['status']:
        await state.set_state(None)
        await message.answer(rest_temp['data'])
        return
    else:
        match rest_temp['data']:
            case 1:
                await state.set_state(Customer.account)
            case 2:
                await state.set_state(Company.account)
            case 3:
                await state.set_state(Worker.account)


