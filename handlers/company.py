from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types
from states import Company
from init import database, company_dict

router = Router()

dict_worker = dict()
dict_service = dict()
dict_update_service = dict()
dict_change = dict()


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
async def account_company_create_worker_name(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id]['name'] = message.text
    await message.answer("Введите адрес")
    await state.set_state(Company.worker_address)


@router.message(StateFilter(Company.worker_address))
async def account_company_create_worker_address(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id]['address'] = message.text
    await message.answer("Введите номер телефона")
    await state.set_state(Company.worker_phone_number)


@router.message(StateFilter(Company.worker_phone_number))
async def account_company_create_worker_phone(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id]['phone_number'] = message.text
    await message.answer("Введите график работы")
    await state.set_state(Company.worker_time_work)


@router.message(StateFilter(Company.worker_time_work))
async def account_company_create_worker_time(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id]['time_work'] = message.text
    await message.answer("Введите логин")
    await state.set_state(Company.worker_login)


@router.message(StateFilter(Company.worker_login))
async def account_company_create_worker_login(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id]['login'] = message.text
    await message.answer("Введите пароль")
    await state.set_state(Company.worker_password)


@router.message(StateFilter(Company.worker_password))
async def account_company_create_worker_password(message: types.Message, state: FSMContext):
    dict_worker[message.from_user.id]['password'] = message.text

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


@router.message(StateFilter(Company.account), Command("orders"))
async def account_company_orders(message: types.Message, state: FSMContext):
    name, address = company_dict[message.from_user.id]
    res_temp = database.list_of_orders(name, address)
    if not res_temp['status']:
        await message.answer(str(res_temp['data']))

    else:
        data = res_temp['data']
        await message.answer("Имя заказчика, Адрес заказчика, Название услуги")
        for el in data:
            await message.answer(", ".join(el))

    await message.answer("Что желаете сделать?\n"
                         "/info - посмотреть свои данные\n"
                         "/service - посмотреть свои услуги\n"
                         "/orders - посмотреть заказы\n"
                         "/worker - посмотреть своих рабочих\n"
                         "/exit - выйти из аккаунта")


@router.message(StateFilter(Company.account), Command("service"))
async def account_company_service(message: types.Message, state: FSMContext):
    await message.answer("Что желаете сделать?\n"
                         "/list_service - Посмотреть свои услуги\n"
                         "/create_service - Создать новую услугу")


@router.message(StateFilter(Company.account), Command("create_service"))
async def account_company_create_service(message: types.Message, state: FSMContext):
    await message.answer("Что желаете сделать?\n"
                         "/create_new_service - Создать услугу, которой не было на рынке\n"
                         "/add_service - Обновить свое меню")


@router.message(StateFilter(Company.account), Command("create_new_service"))
async def account_company_create_service_name(message: types.Message, state: FSMContext):
    await state.set_state(Company.service_name)
    await message.answer("Введите название услуги")
    dict_service[message.from_user.id] = dict()


@router.message(StateFilter(Company.service_name))
async def account_company_create_service_description(message: types.Message, state: FSMContext):
    await state.set_state(Company.service_description)
    await message.answer("Опишите услугу")
    dict_service[message.from_user.id]['name'] = message.text


@router.message(StateFilter(Company.service_description))
async def account_company_create_service_time_work(message: types.Message, state: FSMContext):
    await state.set_state(Company.service_time_work)
    await message.answer("Сколько она должна выполнятся?")
    dict_service[message.from_user.id]['description'] = message.text


@router.message(StateFilter(Company.service_time_work))
async def account_company_create_service_reg(message: types.Message, state: FSMContext):
    await state.set_state(Company.account)
    dict_service[message.from_user.id]['time_work'] = message.text
    res_temp = database.create_new_service(dict_service[message.from_user.id]['name'],
                                           dict_service[message.from_user.id]['description'],
                                           dict_service[message.from_user.id]['time_work'])

    await message.answer(res_temp['message'])
    if not res_temp['status']:  # возникла ошибки
        return
    dict_service.pop(message.from_user.id, None)
    await message.answer("Что желаете сделать?\n"
                         "/create_new_service - Создать услугу, которой не было на рынке\n"
                         "/add_service - Обновить свое меню")


@router.message(StateFilter(Company.account), Command("add_service"))
async def account_company_add_service(message: types.Message, state: FSMContext):
    res_temp = database.list_of_all_service()
    if not res_temp['status']:  # возникла ошибки
        await message.answer(res_temp['data'])
        return
    await state.set_state(Company.service_all)
    res_temp = res_temp['data']
    await message.answer("Выберите, какую хотите добавить/изменить:")
    for el in res_temp:
        await message.answer(f"{el[0]}")
    await message.answer(f"Необходимо ввести услугу")


@router.message(StateFilter(Company.service_all))
async def account_company_add_service_price(message: types.Message, state: FSMContext):
    await state.set_state(Company.service_price)
    dict_update_service[message.from_user.id] = dict()
    dict_update_service[message.from_user.id]['name'] = message.text
    await message.answer("Введите цену")


@router.message(StateFilter(Company.service_price))
async def account_company_add_service_reg(message: types.Message, state: FSMContext):
    await state.set_state(Company.account)
    name_company, address = company_dict[message.from_user.id]
    dict_update_service[message.from_user.id]['price'] = message.text
    res_temp = database.create_new_price(dict_update_service[message.from_user.id]['name'],
                                         dict_update_service[message.from_user.id]['price'],
                                         name_company,
                                         address)

    await message.answer(res_temp['message'])
    dict_update_service.pop(message.from_user.id, None)
    await message.answer("Что желаете сделать?\n"
                         "/create_new_service - Создать услугу, которой не было на рынке\n"
                         "/add_service - Обновить свое меню")


@router.message(StateFilter(Company.account), Command("list_service"))
async def account_company_service(message: types.Message, state: FSMContext):
    name_company, address = company_dict[message.from_user.id]
    res_temp = database.list_company_prices(name_company, address)
    if not res_temp['status']:  # возникла ошибки
        await message.answer(res_temp['data'])
        return
    res_temp = res_temp['data']
    await message.answer("Услуги, которые вы предоставляете")
    for el in res_temp:
        el = [str(i) for i in el]
        await message.answer(f"{', '.join(el)}")
    await message.answer("Что желаете сделать?\n"
                         "/list_service - Посмотреть свои услуги\n"
                         "/create_service - Создать новую услугу")


@router.message(StateFilter(Company.account), Command("info"))
async def account_company_service(message: types.Message, state: FSMContext):
    await message.answer("Что желаете сделать?\n"
                         "/change_user - Изменить свои данные\n"
                         "/delete_user - Удалить пользователя")


@router.message(StateFilter(Company.account), Command("delete_user"))
async def account_company_service(message: types.Message, state: FSMContext):
    name_company, address = company_dict[message.from_user.id]
    res_temp = database.delete_company(name_company, address)
    await message.answer(res_temp['data'])

    await state.set_state(None)
    company_dict.pop(message.text, None)
    await message.answer("Здравствуйте! У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                         "личный кабинет \n/list - посмотреть определенную таблицу")


@router.message(StateFilter(Company.account), Command("change_user"))
async def account_company_service(message: types.Message, state: FSMContext):
    await message.answer("Что желаете изменить?\n"
                         "/phone_number - Номер телефона\n"
                         "/owner - Имя владельца\n"
                         "/time_work - Время работы")
    await state.set_state(Company.change_info)
    dict_change[message.from_user.id] = dict()


@router.message(StateFilter(Company.change_info))
async def account_company_service(message: types.Message, state: FSMContext):
    await message.answer("Введите новую информацию")
    await state.set_state(Company.change_info_put_value)
    dict_change[message.from_user.id]['key'] = message.text[1:]


@router.message(StateFilter(Company.change_info_put_value))
async def account_company_service(message: types.Message, state: FSMContext):
    name_company, address = company_dict[message.from_user.id]
    await state.set_state(Company.account)
    dict_change[message.from_user.id]['value'] = message.text
    res_temp = database.change_info_company(dict_change[message.from_user.id]['key'],
                                            dict_change[message.from_user.id]['value'],
                                            name_company,
                                            address)
    await message.answer(res_temp['message'])

    await message.answer("Что желаете сделать?\n"
                         "/info - посмотреть свои данные\n"
                         "/service - посмотреть свои услуги\n"
                         "/orders - посмотреть заказы\n"
                         "/worker - посмотреть своих рабочих\n"
                         "/exit - выйти из аккаунта")
