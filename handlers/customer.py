from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types
from states import Customer
from init import database, customer_dict

router = Router()

dict_change = dict()
dict_order = dict()


@router.message(StateFilter(Customer.account), Command("exit"))
async def account_company(message: types.Message, state: FSMContext):
    await state.set_state(None)
    customer_dict.pop(message.text, None)
    await message.answer("Здравствуйте! У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                         "личный кабинет \n/list - посмотреть определенную таблицу")


@router.message(StateFilter(Customer.account), Command("info"))
async def account_company_service(message: types.Message, state: FSMContext):
    await message.answer("Что желаете сделать?\n"
                         "/change_user - Изменить свои данные\n"
                         "/delete_user - Удалить пользователя")


@router.message(StateFilter(Customer.account), Command("delete_user"))
async def account_company_service(message: types.Message, state: FSMContext):
    name, address = customer_dict[message.from_user.id]
    res_temp = database.delete_customer(name, address)
    await message.answer(res_temp['data'])

    await state.set_state(None)
    customer_dict.pop(message.text, None)
    await message.answer("Здравствуйте! У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                         "личный кабинет \n/list - посмотреть определенную таблицу")


@router.message(StateFilter(Customer.account), Command("change_user"))
async def account_company_service(message: types.Message, state: FSMContext):
    await message.answer("Что желаете изменить?\n"
                         "/phone_number - Номер телефона\n")
    await state.set_state(Customer.change_info)
    dict_change[message.from_user.id] = dict()


@router.message(StateFilter(Customer.change_info))
async def account_company_service(message: types.Message, state: FSMContext):
    await message.answer("Введите новую информацию")
    await state.set_state(Customer.change_info_put_value)
    dict_change[message.from_user.id]['key'] = message.text[1:]


@router.message(StateFilter(Customer.change_info_put_value))
async def account_company_service(message: types.Message, state: FSMContext):
    name_company, address = customer_dict[message.from_user.id]
    await state.set_state(Customer.account)
    dict_change[message.from_user.id]['value'] = message.text
    res_temp = database.change_info_customer(dict_change[message.from_user.id]['key'],
                                             dict_change[message.from_user.id]['value'],
                                             name_company,
                                             address)
    await message.answer(res_temp['message'])

    await message.answer("Что желаете сделать?\n"
                         "/info - посмотреть свои данные\n"
                         "/service - посмотреть услуги\n"
                         "/exit - выйти из аккаунта")


@router.message(StateFilter(Customer.account), Command("service"))
async def account_company_service(message: types.Message, state: FSMContext):
    await message.answer("Что желаете сделать?\n"
                         "/all_orders - посмотреть свои заказы\n"
                         "/create_service - создать новый заказ\n"
                         "/exit - выйти из аккаунта")


@router.message(StateFilter(Customer.account), Command("create_service"))
async def account_company_service(message: types.Message, state: FSMContext):
    dict_order[message.from_user.id] = dict()
    res_temp = database.list_of_service()
    if res_temp['status']:
        await state.set_state(Customer.choose_orders)
        data = res_temp['data']
        string = ""
        for el in data:
            string = string + str(el[0]) + '\n'
        string = string + "/exit"
        await message.answer(string)
        await message.answer("Чтобы выбрать, напишите")
    else:
        await message.answer(res_temp['data'])


@router.message(StateFilter(Customer.choose_orders))
async def account_company_service(message: types.Message, state: FSMContext):
    dict_order[message.from_user.id]['name_service'] = message.text
    res_temp = database.list_of_prices(message.text)
    if res_temp['status']:
        await state.set_state(Customer.choose_company)
        data = res_temp['data']
        print(data)
        dict_order[message.from_user.id]['name_company'] = data
        string = ""
        i = 0
        for el in data:
            string = string + f"/{i} компания {str(el[0])} по адресу {str(el[1])}   представляет {str(message.text)} за {str(el[2])} " + '\n'
            i += 1
        await message.answer(string)
    else:
        await message.answer(res_temp['data'])


@router.message(StateFilter(Customer.choose_company))
async def account_company_service(message: types.Message, state: FSMContext):
    name_customer, address_customer = customer_dict[message.from_user.id]
    dict_order[message.from_user.id]['name_company'] = dict_order[message.from_user.id]['name_company'][int(message.text[1:])]
    res_temp = database.create_order(name_customer,
                                     address_customer,
                                     dict_order[message.from_user.id]['name_service'],
                                     dict_order[message.from_user.id]['name_company'])
    dict_order.pop(message.from_user.id, None)
    await state.set_state(Customer.account)
    await message.answer(res_temp['message'])

    await message.answer("Что желаете сделать?\n"
                         "/info - посмотреть свои данные\n"
                         "/service - посмотреть услуги\n"
                         "/exit - выйти из аккаунта")


@router.message(StateFilter(Customer.account), Command("all_orders"))
async def account_company_service(message: types.Message, state: FSMContext):
    name_customer, address_customer = customer_dict[message.from_user.id]
    res_temp = database.list_of_orders_for_customer(name_customer, address_customer)
    if res_temp['status']:
        data = res_temp['data']
        string = ""
        for el in data:
            string = string + f"Услугу {str(el[0])}  представляет компания {str(el[1])} по адресу {str(el[2])} " + '\n'
        await message.answer(string)
    else:
        await message.answer(res_temp['data'])

    await message.answer("Что желаете сделать?\n"
                         "/info - посмотреть свои данные\n"
                         "/service - посмотреть услуги\n"
                         "/exit - выйти из аккаунта")