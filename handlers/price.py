from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from states import Price
from aiogram import types
from init import database

router = Router()


@router.message(StateFilter(None), Command("price"))
async def show_list_service(message: types.Message, state: FSMContext):
    res_temp = database.list_of_service()
    if res_temp['status']:
        await state.set_state(Price.show_service_price)
        data = res_temp['data']
        string = ""
        for el in data:
            string = string + "/" + str(el) + '\n'
        string = string + "/exit"
        await message.answer(string)
    else:
        await message.answer(res_temp['data'])


@router.message(Price.show_service_price, Command("exit"))
async def exit_from_prices(message: types.Message, state: FSMContext):
    await state.set_state(None)
    await message.answer("У бота есть 3 функции для вас\n/price - посмотреть цены \n/auth - войти в "
                         "личный кабинет \n/list - посмотреть определенную таблицу")


@router.message(Price.show_service_price)
async def show_non_auth_prices(message: types.Message):
    res_temp = database.list_of_prices(message.text)
    if res_temp['status']:
        data = res_temp['data']
        string = ""
        for el in data:
            string = string + f"Компания {str(el[0])} представляет {str(message.text)} за {str(el[1])} " + '\n'
        string = string + "/exit"
        return string
    else:
        return res_temp['data']
