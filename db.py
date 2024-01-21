import psycopg2
from psycopg2 import Error


class PostgresDB:
    def __init__(self):
        self.cursor = None
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(user="postgres",
                                               password="postgres",
                                               host="localhost",
                                               port="5432",
                                               database="postgres"
                                               )

            self.cursor = self.connection.cursor()
        except (Exception, Error) as error:
            print("Ошибка при подключении", error)

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def create_new_user(self, username, password, user_group):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM all_users WHERE username = '{username}');"
            self.cursor.execute(str_exec)

            if self.cursor.fetchone()[0]:
                res['status'] = False
                res['message'] = "Пользователь с таким логином существует"
            else:
                str_exec = ""
                str_exec = str_exec + f'INSERT INTO all_users (username, password, user_group) '
                str_exec = str_exec + f"VALUES ('{username}', '{password}', '{user_group}') RETURNING id;"

                self.cursor.execute(str_exec)
                self.connection.commit()
                student_id = self.cursor.fetchone()[0]

                # если все удачно, то запоминаем результат
                res['status'] = True
                res['data'] = student_id

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['message'] = "Ошибка при создание аккаунта"

        finally:
            self.close_connection()
            return res

    def create_customer(self, name, address, phone_number, global_id):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM customer WHERE name = '{name}' AND address = '{address}');"
            self.cursor.execute(str_exec)

            if self.cursor.fetchone()[0]:
                res['status'] = False
                res['message'] = "Пользователь с таким именем и адресом существует"
            else:
                str_exec = ""
                str_exec = str_exec + f'INSERT INTO customer (name, address, phone_number, global_id) '
                str_exec = str_exec + f"VALUES ('{name}', '{address}', '{phone_number}', '{global_id}');"

                self.cursor.execute(str_exec)
                self.connection.commit()

                # если все удачно, то запоминаем результат
                res['status'] = True
                res['message'] = "Пользователь создан"
                res['data'] = [name, address]

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['message'] = "Ошибка при создание аккаунта"

        finally:
            self.close_connection()
            return res

    def create_company(self, name, address, phone_number, owner, time_work, global_id):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM company WHERE name = '{name}' AND address = '{address}');"
            self.cursor.execute(str_exec)

            if self.cursor.fetchone()[0]:
                res['status'] = False
                res['message'] = "Пользователь с таким именем и адресом существует"
            else:
                str_exec = ""
                str_exec = str_exec + f'INSERT INTO company (name, address, phone_number, owner, time_work, global_id) '
                str_exec = str_exec + f"VALUES ('{name}', '{address}', '{phone_number}'," \
                                      f" '{owner}', '{time_work}', '{global_id}');"

                self.cursor.execute(str_exec)
                self.connection.commit()

                # если все удачно, то запоминаем результат
                res['status'] = True
                res['message'] = "Пользователь создан"
                res['data'] = [name, address]

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['message'] = "Ошибка при создание аккаунта"

        finally:
            self.close_connection()
            return res

    def create_worker(self, name, address, name_company, name_address,  phone_number, time_work, global_id):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM worker" \
                       f" WHERE name = '{name}' AND address = '{address}'" \
                       f" AND name_company = '{name_company}' AND name_address = '{name_address}');"
            self.cursor.execute(str_exec)

            if self.cursor.fetchone()[0]:
                res['status'] = False
                res['message'] = "Пользователь с такими данными существует"
            else:
                str_exec = ""
                str_exec = str_exec + f'INSERT INTO worker (name, address, name_company, name_address,' \
                                      f' phone_number, time_work, global_id) '
                str_exec = str_exec + f"VALUES ('{name}', '{address}', '{name_company}', '{name_address}', " \
                                      f" '{phone_number}', '{time_work}', '{global_id}');"

                self.cursor.execute(str_exec)
                self.connection.commit()

                # если все удачно, то запоминаем результат
                res['status'] = True
                res['message'] = "Пользователь создан"

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['message'] = "Ошибка при создание аккаунта"

        finally:
            self.close_connection()
            return res

    def show_table(self, table):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT * FROM {table};"
            self.cursor.execute(str_exec)
            res_values = self.cursor.fetchall()

            str_exec = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';"
            self.cursor.execute(str_exec)
            res_columns = self.cursor.fetchall()
            res_columns = [el[0] for el in res_columns]

            if len(res_values) == 0:
                res['status'] = False
                res['data'] = "Таблица пустая"
            else:
                res['status'] = True
                res['data'] = res_values
                res['columns'] = res_columns

        except (Exception, Error) as error:
            res['status'] = False
            res['data'] = "Ошибка при выдачи таблицы"

        finally:
            self.close_connection()
            return res

    def auth(self, username, password):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT user_group, id FROM all_users WHERE username = '{username}' AND password = '{password}';"
            self.cursor.execute(str_exec)
            res_values = self.cursor.fetchone()
            if res_values is None:
                res['status'] = False
                res['data'] = "Пользователь не найден"
                return

            res_values = list(res_values)
            match res_values[0]:
                case "1":
                    str_exec = f"SELECT name, address" \
                               f" FROM customer" \
                               f" WHERE global_id = '{res_values[1]}';"
                case "2":
                    str_exec = f"SELECT name, address" \
                               f" FROM company" \
                               f" WHERE global_id = '{res_values[1]}';"
                case "3":
                    str_exec = f"SELECT name, address, name_company, name_address" \
                               f" FROM worker" \
                               f" WHERE global_id = '{res_values[1]}';"
            self.cursor.execute(str_exec)
            res_values[1] = self.cursor.fetchone()
            if res_values is None:
                res['status'] = False
                res['data'] = "Пользователь не найден"
                return
            else:
                res['status'] = True
                res['data'] = res_values

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['data'] = "Ошибка при выдачи таблицы"

        finally:
            self.close_connection()
            return res

    def list_of_service(self):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT name_service FROM prices;"
            self.cursor.execute(str_exec)
            res_temp = self.cursor.fetchall()
            if len(res_temp) == 0:
                res['status'] = False
                res['data'] = "Нет услуг"
            else:
                res['status'] = True
                res['data'] = res_temp

        except (Exception, Error) as error:
            res['status'] = False
            res['data'] = "Ошибка при выдачи таблицы"

        finally:
            self.close_connection()
            return res

    def list_of_prices(self, service):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT name_company, price FROM prices WHERE name_service ='{service}';"
            self.cursor.execute(str_exec)
            res_temp = self.cursor.fetchall()
            if len(res_temp) == 0:
                res['status'] = False
                res['data'] = "Нет расценок"
            else:
                res['status'] = True
                res['data'] = res_temp

        except (Exception, Error) as error:
            res['status'] = False
            res['data'] = "Ошибка при выдачи таблицы"

        finally:
            self.close_connection()
            return res

    def list_of_workers(self, name_company, address):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT name, address, phone_number, time_work" \
                       f" FROM worker " \
                       f" WHERE name_company ='{name_company}' AND name_address ='{address}';"
            self.cursor.execute(str_exec)
            res_temp = self.cursor.fetchall()

            if len(res_temp) == 0:
                res['status'] = False
                res['data'] = "Нет работников"
            else:
                res['status'] = True
                res['data'] = res_temp

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['data'] = "Ошибка при выдачи таблицы"

        finally:
            self.close_connection()
            return res


