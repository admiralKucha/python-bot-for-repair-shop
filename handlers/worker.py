from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types
from states import Worker
from init import database, worker_dict

router = Router()
dict_change = dict()
dict_orders = dict()


@router.message(StateFilter(Worker.account), Command("exit"))
async def account_company(message: types.Message, state: FSMContext):
    await state.set_state(None)
    worker_dict.pop(message.text, None)
    await message.answer("Здравствуйте! У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                         "личный кабинет \n/list - посмотреть определенную таблицу")


@router.message(StateFilter(Worker.account), Command("info"))
async def account_company_service(message: types.Message, state: FSMContext):
    await message.answer("Что желаете сделать?\n"
                         "/change_user - Изменить свои данные\n"
                         "/delete_user - Удалить пользователя")


@router.message(StateFilter(Worker.account), Command("delete_user"))
async def account_company_service(message: types.Message, state: FSMContext):
    name, address, name_company, name_address = worker_dict[message.from_user.id]
    res_temp = database.delete_worker(name, address)
    await message.answer(res_temp['data'])

    await state.set_state(None)
    worker_dict.pop(message.text, None)
    await message.answer("Здравствуйте! У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                         "личный кабинет \n/list - посмотреть определенную таблицу")


@router.message(StateFilter(Worker.account), Command("change_user"))
async def account_company_service(message: types.Message, state: FSMContext):
    await message.answer("Что желаете изменить?\n"
                         "/phone_number - Номер телефона\n"
                         "/time_work - Время работы")
    await state.set_state(Worker.change_info)
    dict_change[message.from_user.id] = dict()


@router.message(StateFilter(Worker.change_info))
async def account_company_service(message: types.Message, state: FSMContext):
    await message.answer("Введите новую информацию")
    await state.set_state(Worker.change_info_put_value)
    dict_change[message.from_user.id]['key'] = message.text[1:]


@router.message(StateFilter(Worker.change_info_put_value))
async def account_company_service(message: types.Message, state: FSMContext):
    name, address, name_company, name_address = worker_dict[message.from_user.id]
    await state.set_state(Worker.account)
    dict_change[message.from_user.id]['value'] = message.text
    res_temp = database.change_info_worker(dict_change[message.from_user.id]['key'],
                                           dict_change[message.from_user.id]['value'],
                                           name,
                                           address,
                                           name_company,
                                           name_address)
    await message.answer(res_temp['message'])

    await message.answer("Что желаете сделать?\n"
                         "/info - посмотреть свои данные\n"
                         "/do_order  - сделать заказ\n"
                         "/exit - выйти из аккаунта")


@router.message(StateFilter(Worker.account), Command("do_order"))
async def account_company_service(message: types.Message, state: FSMContext):
    name, address, name_company, name_address = worker_dict[message.from_user.id]
    res_temp = database.list_of_orders(name_company, name_address)
    if not res_temp['status']:
        await message.answer(str(res_temp['data']))

    else:
        await state.set_state(Worker.orders)
        data = res_temp['data']
        dict_orders[message.from_user.id] = data
        await message.answer("Имя заказчика, Адрес заказчика, Название услуги")
        i = 0
        for el in data:
            i = i + 1
            await message.answer(f"/{i}" + ", ".join(el))

        await message.answer("Выберите заказ")


@router.message(StateFilter(Worker.orders))
async def account_company_service(message: types.Message, state: FSMContext):
    name, address, name_company, name_address = worker_dict[message.from_user.id]
    data = dict_orders[message.from_user.id][int(message.text[1:])]
    dict_orders[message.from_user.id] = data
    res_temp = database.delete_order(name_company, name_address, data)
    await message.answer(str(res_temp['data']))
    await state.set_state(Worker.account)
    await message.answer("Что желаете сделать?\n"
                         "/info - посмотреть свои данные\n"
                         "/do_order  - сделать заказ\n"
                         "/exit - выйти из аккаунта")