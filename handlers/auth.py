from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types
from states import Auth, Company, Customer, Worker
from init import database, company_dict, worker_dict, customer_dict

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
    res_temp = database.auth(user_dict[id_user]['login'],
                             user_dict[id_user]['password'])

    user_dict.pop(id_user, None)
    if not res_temp['status']:
        await state.set_state(None)
        await message.answer(res_temp['data'])
        await message.answer("Здравствуйте! У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                             "личный кабинет \n/list - посмотреть определенную таблицу")
        return
    
    else:
        match res_temp['data'][0]:
            case "1":
                await state.set_state(Customer.account)
                customer_dict[message.from_user.id] = res_temp['data'][1]
                await message.answer("Вы вошли в свой аккаунт\n"
                                     "Что желаете сделать?\n"
                                     "/info - посмотреть свои данные\n"
                                     "/service - посмотреть услуги\n"
                                     "/exit - выйти из аккаунта")
            case "2":
                await state.set_state(Company.account)
                company_dict[message.from_user.id] = res_temp['data'][1]
                await message.answer("Вы вошли в свой аккаунт\n"
                                     "Что желаете сделать?\n"
                                     "/info - посмотреть свои данные\n"
                                     "/service - посмотреть свои услуги\n"
                                     "/orders - посмотреть заказы\n"
                                     "/worker - посмотреть своих рабочих\n"
                                     "/exit - выйти из аккаунта")

            case "3":
                await state.set_state(Worker.account)
                worker_dict[message.from_user.id] = res_temp['data'][1]
                await message.answer("Вы вошли в свой аккаунт\n"
                                     "Что желаете сделать?\n"
                                     "/info - посмотреть свои данные\n"
                                     "/orders - посмотреть заказы\n"
                                     "/exit - выйти из аккаунта")
