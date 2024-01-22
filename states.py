from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    # это часть есть у всех типов пользователей в регистрации
    user_create_login = State()
    user_create_password = State()
    user_name = State()  # у фирмы он тоже есть - это поле владелец
    user_address = State()
    user_phone_number = State()

    # выбираем тип пользователя
    user_group = State()

    # для заказчика больше ничего не надо - отправляем его в личный кабинет
    # состояния для личного кабинета - другой класс

    # для фирмы осталось только несколько полей
    company_name = State()
    company_schedule = State()

    # Описание работы данного класса
    # -Человек нажимает на кнопку для регистрации, его просят ввести Имя, Адрес, Номер телефона
    # -После идет выбор группы
    # -После идет уникальная информация для каждого типа пользователей
    # -После все попадают на состояния заполнения логина, пароля
    # -Все из пароля попадают в личный кабинет


class Tables(StatesGroup):
    choose_table = State()

    # Для унификации написана как группа классов
    # -Человек выбирает таблицу, мы ее отображаем: одно сообщение - одна строка


class Auth(StatesGroup):
    username = State()
    password = State()
    # -Человек проходит авторизацию
    # -Набирает логин и пароль
    # -Если все хорошо - отправляем в кабинет, в зависимости от его роли
    # -Иначе - отправляем обратно в состояние неавторизованного


class Price(StatesGroup):
    show_service_price = State()

    # Для унификации написана как группа классов
    # -Человек выбирает услугу, мы отображаем: Компания - цена


class Company(StatesGroup):
    account = State()
    # -Человек зашел в свой аккаунт и теперь имеет больше функций в зависимости от своей роли

    worker_name = State()
    worker_address = State()
    worker_phone_number = State()
    worker_time_work = State()
    worker_login = State()
    worker_password = State()
    # -Компания создает работника, пишет все его данные, придумывает логин и пароль

    service_name = State()
    service_description = State()
    service_time_work = State()
    # -Компания создает услугу, описывает ее

    service_all = State()
    service_price = State()
    # -Компания добавляет услугу к себе в меню, описывая расценки

    change_info = State()
    change_info_put_value = State()
    # -Компания изменяет информацию о себе


class Customer(StatesGroup):
    account = State()
    # -Человек зашел в свой аккаунт и теперь имеет больше функций в зависимости от своей роли


class Worker(StatesGroup):
    account = State()
    # -Человек зашел в свой аккаунт и теперь имеет больше функций в зависимости от своей роли

