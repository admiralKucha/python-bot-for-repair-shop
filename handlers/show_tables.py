from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import types
from states import Tables
from init import database

router = Router()


@router.message(StateFilter(None), Command("list"))
async def choose_table(message: types.Message, state: FSMContext):
    await message.answer("Какую таблицу вы хотите видеть?\n"
                         "/1 all_users\n"
                         "/2 company\n"
                         "/3 customer\n"
                         "/4 orders\n"
                         "/5 prices\n"
                         "/6 service\n"
                         "/7 worker\n"
                         "/exit")

    await state.set_state(Tables.choose_table)


@router.message(StateFilter(Tables.choose_table), Command("exit"))
async def exit_show_table(message: types.Message, state: FSMContext):
    await state.set_state(None)
    await message.answer("Здравствуйте! У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                         "личный кабинет \n/list - посмотреть определенную таблицу")


@router.message(Tables.choose_table)
async def show_table(message: types.Message, state: FSMContext):
    text = "error"
    res = dict()
    match message.text:
        case "/1":
            text = "all_users"
        case "/2":
            text = "company"
        case "/3":
            text = "customer"
        case "/4":
            text = "orders"
        case "/5":
            text = "prices"
        case "/6":
            text = "service"
        case "/7":
            text = "worker"

    if text == "error":
        res['status'] = False
        res['data'] = "Выбрана неправильная таблица"
    else:
        res = database.show_table(text)

    if not res['status']:
        await message.answer(res['data'])
    else:
        await message.answer(", ".join(res['columns']))

        strings = res['data']
        for string in strings:
            string = ", ".join([str(el) for el in string])
            await message.answer(string)

    await message.answer("Какую таблицу вы хотите видеть далее?\n"
                         "/1 all_users\n"
                         "/2 company\n"
                         "/3 customer\n"
                         "/4 orders\n"
                         "/5 prices\n"
                         "/6 service\n"
                         "/7 worker\n"
                         "/exit")



