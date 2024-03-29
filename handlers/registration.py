from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states import Registration, Customer, Company
from aiogram import types
from init import database, company_dict, customer_dict

router = Router()
# информация для регистрация
dict_about_reg = dict()


@router.message(StateFilter(None), Command("create"))
async def cmd_create(message: types.Message, state: FSMContext):
    await message.answer("Введите свое имя")
    await state.set_state(Registration.user_name)
    dict_about_reg[message.from_user.id] = dict()


@router.message(Registration.user_name)
async def cmd_name_user(message: types.Message, state: FSMContext):
    await message.answer("Введите свой адрес")
    await state.set_state(Registration.user_address)
    dict_about_reg[message.from_user.id]['name'] = message.text


@router.message(Registration.user_address)
async def cmd_address_user(message: types.Message, state: FSMContext):
    await message.answer("Введите номер телефона")
    await state.set_state(Registration.user_phone_number)
    dict_about_reg[message.from_user.id]['address'] = message.text


@router.message(Registration.user_phone_number)
async def cmd_phone_number_user(message: types.Message, state: FSMContext):
    await message.answer("Введите тип пользователя\n"
                         "1 - заказчик\n"
                         "2 - компания")
    await state.set_state(Registration.user_group)
    dict_about_reg[message.from_user.id]['phone_number'] = message.text


@router.message(Registration.user_group)
async def cmd_group_user(message: types.Message, state: FSMContext):
    text = message.text
    dict_about_reg[message.from_user.id]['user_group'] = text
    if text == '1':
        await message.answer("Придумайте логин")
        await state.set_state(Registration.user_create_login)
    elif text == '2':
        await message.answer("Введите название компании")
        dict_about_reg[message.from_user.id]['owner'] = dict_about_reg[message.from_user.id]['name']
        await state.set_state(Registration.company_name)


@router.message(Registration.company_name)
async def cmd_company_user(message: types.Message, state: FSMContext):
    await message.answer("Введите график работы")
    await state.set_state(Registration.company_schedule)
    dict_about_reg[message.from_user.id]['name'] = message.text


@router.message(Registration.company_schedule)
async def cmd_schedule_user(message: types.Message, state: FSMContext):
    await message.answer("Придумайте логин")
    await state.set_state(Registration.user_create_login)
    dict_about_reg[message.from_user.id]['time_work'] = message.text


@router.message(Registration.user_create_login)
async def cmd_login_user(message: types.Message, state: FSMContext):
    await message.answer("Придумайте пароль")
    await state.set_state(Registration.user_create_password)
    dict_about_reg[message.from_user.id]['login'] = message.text


@router.message(Registration.user_create_password)
async def cmd_password_user(message: types.Message, state: FSMContext):
    await state.set_state(None)
    user_group = dict_about_reg[message.from_user.id]['user_group']
    dict_about_reg[message.from_user.id]['password'] = message.text
    res_temp = database.create_new_user(dict_about_reg[message.from_user.id]['login'],
                                        dict_about_reg[message.from_user.id]['password'],
                                        user_group)

    if not res_temp['status']:  # возникла ошибки
        await message.answer(res_temp['message'])
        await message.answer("Здравствуйте! У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                             "личный кабинет \n/list - посмотреть определенную таблицу")

    else:
        global_id = res_temp['data']
        if user_group == str(1):
            res_temp = database.create_customer(dict_about_reg[message.from_user.id]['name'],
                                                dict_about_reg[message.from_user.id]['address'],
                                                dict_about_reg[message.from_user.id]['phone_number'],
                                                global_id)
            if not res_temp['status']:
                await message.answer(res_temp['message'])
                await message.answer(
                    "Здравствуйте! У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                    "личный кабинет \n/list - посмотреть определенную таблицу")
                return

            await state.set_state(Customer.account)
            await message.answer(res_temp['message'])
            customer_dict[message.from_user.id] = res_temp['data']
            await message.answer("Вы вошли в свой аккаунт\n"
                                 "Что желаете сделать?\n"
                                 "/info - посмотреть свои данные\n"
                                 "/service - посмотреть услуги\n"
                                 "/exit - выйти из аккаунта")
        else:
            res_temp = database.create_company(dict_about_reg[message.from_user.id]['name'],
                                               dict_about_reg[message.from_user.id]['address'],
                                               dict_about_reg[message.from_user.id]['phone_number'],
                                               dict_about_reg[message.from_user.id]['owner'],
                                               dict_about_reg[message.from_user.id]['time_work'],
                                               global_id)
            if not res_temp['status']:
                await message.answer(res_temp['message'])
                return

            await state.set_state(Company.account)
            await message.answer(res_temp['message'])
            company_dict[message.from_user.id] = res_temp['data']
            await message.answer("Вы вошли в свой аккаунт\n"
                                 "Что желаете сделать?\n"
                                 "/info - посмотреть свои данные\n"
                                 "/service - посмотреть свои услуги\n"
                                 "/orders - посмотреть заказы\n"
                                 "/worker - посмотреть своих рабочих\n"
                                 "/exit - выйти из аккаунта")

    dict_about_reg.pop(message.from_user.id, None)
