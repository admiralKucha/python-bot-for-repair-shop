from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types
from states import Company
from init import database, company_dict

router = Router()

dict_worker = dict()


@router.message(StateFilter(Company.account), Command("exit"))
async def account_company(message: types.Message, state: FSMContext):
    await state.set_state(None)
    company_dict.pop(message.text, None)
    await message.answer("Здравствуйте! У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                         "личный кабинет \n/list - посмотреть определенную таблицу")


@router.message(StateFilter(Company.account), Command("worker"))
async def account_company_worker(message: types.Message):
    await message.answer("Что желаете сделать?\n"
                         "/list_worker - Посмотреть своих работников\n"
                         "/create - Зарегистрировать нового работника")


@router.message(StateFilter(Company.account), Command("list_worker"))
async def account_company_list(message: types.Message):
    name, address = company_dict[message.from_user.id]
    res_temp = database.list_of_workers(name, address)
    if not res_temp['status']:
        await message.answer(str(res_temp['data']))

    else:
        data = res_temp['data']
        await message.answer("Имя, Адрес, Номер телефона, График работы")
        for el in data:
            await message.answer(", ".join(el))

    await message.answer("Что желаете сделать?\n"
                         "/info - посмотреть свои данные\n"
                         "/service - посмотреть свои услуги\n"
                         "/orders - посмотреть заказы\n"
                         "/worker - посмотреть своих рабочих\n"
                         "/exit - выйти из аккаунта")


@router.message(StateFilter(Company.account), Command("create"))
async def account_company_create_worker(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id] = dict()
    await message.answer("Введите имя")
    await state.set_state(Company.worker_name)


@router.message(StateFilter(Company.worker_name))
async def account_company_create_worker(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id]['name'] = message.text
    await message.answer("Введите адрес")
    await state.set_state(Company.worker_address)


@router.message(StateFilter(Company.worker_address))
async def account_company_create_worker(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id]['address'] = message.text
    await message.answer("Введите номер телефона")
    await state.set_state(Company.worker_phone_number)


@router.message(StateFilter(Company.worker_phone_number))
async def account_company_create_worker(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id]['phone_number'] = message.text
    await message.answer("Введите график работы")
    await state.set_state(Company.worker_time_work)


@router.message(StateFilter(Company.worker_time_work))
async def account_company_create_worker(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id]['time_work'] = message.text
    await message.answer("Введите логин")
    await state.set_state(Company.worker_login)


@router.message(StateFilter(Company.worker_login))
async def account_company_create_worker(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id]['login'] = message.text
    await message.answer("Введите пароль")
    await state.set_state(Company.worker_password)


@router.message(StateFilter(Company.worker_password))
async def account_company_create_worker(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id]['password'] = message.text

    # начать писать здесь
    user_group = 3
    res_temp = database.create_new_user(dict_worker[message.from_user.id]['login'],
                                        dict_worker[message.from_user.id]['password'],
                                        user_group)

    if not res_temp['status']:  # возникла ошибки
        await message.answer(res_temp['message'])

    else:
        global_id = res_temp['data']
        name_company, address_company = company_dict[message.from_user.id]
        res_temp = database.create_worker(dict_worker[message.from_user.id]['name'],
                                          dict_worker[message.from_user.id]['address'],
                                          name_company,
                                          address_company,
                                          dict_worker[message.from_user.id]['phone_number'],
                                          dict_worker[message.from_user.id]['time_work'],
                                          global_id)

        await message.answer(res_temp['message'])

    await message.answer("Что желаете сделать далее?\n"
                         "/info - посмотреть свои данные\n"
                         "/service - посмотреть свои услуги\n"
                         "/orders - посмотреть заказы\n"
                         "/worker - посмотреть своих рабочих\n"
                         "/exit - выйти из аккаунта")

    dict_worker.pop(message.from_user.id, None)
    await state.set_state(Company.account)
