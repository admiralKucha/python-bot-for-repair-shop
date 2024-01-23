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

    def create_worker(self, name, address, name_company, name_address, phone_number, time_work, global_id):
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

            str_exec = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}';"
            self.cursor.execute(str_exec)
            res_columns = self.cursor.fetchall()
            res_columns = [el[0] for el in res_columns]

            str_exec = f"SELECT {', '.join(res_columns)} FROM {table};"
            self.cursor.execute(str_exec)
            res_values = self.cursor.fetchall()

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
                               f" WHERE global_id = {res_values[1]};"
                case "2":
                    str_exec = f"SELECT name, address" \
                               f" FROM company" \
                               f" WHERE global_id = {res_values[1]};"
                case "3":
                    str_exec = f"SELECT name, address, name_company, name_address" \
                               f" FROM worker" \
                               f" WHERE global_id = {res_values[1]};"
            self.cursor.execute(str_exec)
            res_values[1] = self.cursor.fetchone()
            print(res_values)
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

    def list_of_all_service(self):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT name FROM service;"
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
            str_exec = f"SELECT name_company, address, price FROM prices WHERE name_service = '{service}';"
            self.cursor.execute(str_exec)
            res_temp = self.cursor.fetchall()
            if len(res_temp) == 0:
                res['status'] = False
                res['data'] = "Нет расценок"
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

    def list_of_orders(self, name_company, address):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT name_customer, address_customer, name_service " \
                       f" FROM orders " \
                       f" WHERE name_company ='{name_company}' AND name_address ='{address}';"
            self.cursor.execute(str_exec)
            res_temp = self.cursor.fetchall()

            if len(res_temp) == 0:
                res['status'] = False
                res['data'] = "Нет заказов"
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

    def create_new_service(self, name, description, time_work):
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM service" \
                       f" WHERE name = '{name}');"
            self.cursor.execute(str_exec)

            if self.cursor.fetchone()[0]:
                res['status'] = False
                res['message'] = "Такая услуга существует"
            else:
                str_exec = ""
                str_exec = str_exec + f'INSERT INTO service (name, description, time_work) ' \
                                      f" VALUES ('{name}', '{description}', '{time_work}');"

                self.cursor.execute(str_exec)
                self.connection.commit()

                # если все удачно, то запоминаем результат
                res['status'] = True
                res['message'] = "Услуга создана"

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['message'] = "Ошибка при создание услуги"

        finally:
            self.close_connection()
            return res

    def create_new_price(self, name_service, price, name_company, address):
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM prices" \
                       f" WHERE name_service = '{name_service}' AND" \
                       f" name_company = '{name_company}' AND" \
                       f" address = '{address}');"
            self.cursor.execute(str_exec)

            if self.cursor.fetchone()[0]:
                str_exec = f"UPDATE prices SET price = {price}" \
                           f" WHERE name_service = '{name_service}' AND" \
                           f" name_company = '{name_company}' AND" \
                           f" address = '{address}';"
                self.cursor.execute(str_exec)
                self.connection.commit()
                res['status'] = True
                res['message'] = "Услуга обновлена"

            else:
                str_exec = ""
                str_exec = str_exec + f'INSERT INTO prices (price, name_service, name_company, address) ' \
                                      f" VALUES ('{price}', '{name_service}', '{name_company}', '{address}');"

                self.cursor.execute(str_exec)
                self.connection.commit()

                # если все удачно, то запоминаем результат
                res['status'] = True
                res['message'] = "Услуга добавлена"

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['message'] = "Ошибка при создание услуги"

        finally:
            self.close_connection()
            return res

    def list_company_prices(self, name_company, address):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT name_service, price " \
                       f" FROM prices " \
                       f" WHERE name_company ='{name_company}' AND address ='{address}';"
            self.cursor.execute(str_exec)
            res_temp = self.cursor.fetchall()

            if len(res_temp) == 0:
                res['status'] = False
                res['data'] = "Нет услуг"
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

    def delete_company(self, name_company, address):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT global_id " \
                       f" FROM company " \
                       f" WHERE name ='{name_company}' AND address ='{address}';"
            self.cursor.execute(str_exec)
            res_temp = self.cursor.fetchone()

            if res_temp is None:
                res['status'] = False
                res['data'] = "Такого пользователя нет"
            else:
                str_exec = f'DELETE FROM all_users WHERE id = {res_temp[0]} RETURNING id;'
                self.cursor.execute(str_exec)
                self.connection.commit()
                res['status'] = True
                res['data'] = "Аккаунт удален"

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['data'] = "Ошибка при удалении аккаунта"

        finally:
            self.close_connection()
            return res

    def change_info_company(self, key, value, name, address):
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM company" \
                       f" WHERE name = '{name}' AND" \
                       f" address = '{address}');"
            self.cursor.execute(str_exec)

            if self.cursor.fetchone()[0]:
                str_exec = f"UPDATE company SET {key} = '{value}'" \
                       f" WHERE name = '{name}' AND" \
                       f" address = '{address}';"
                self.cursor.execute(str_exec)
                self.connection.commit()
                res['status'] = True
                res['message'] = "Информация обновлена"

            else:
                res['status'] = False
                res['message'] = "Такого пользователя не существует"

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['message'] = "Ошибка при создание услуги"

        finally:
            self.close_connection()
            return res

    def delete_customer(self, name, address):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT global_id " \
                       f" FROM customer " \
                       f" WHERE name ='{name}' AND address ='{address}';"
            self.cursor.execute(str_exec)
            res_temp = self.cursor.fetchone()

            if res_temp is None:
                res['status'] = False
                res['data'] = "Такого пользователя нет"
            else:
                str_exec = f'DELETE FROM all_users WHERE id = {res_temp[0]} RETURNING id;'
                self.cursor.execute(str_exec)
                self.connection.commit()
                res['status'] = True
                res['data'] = "Аккаунт удален"

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['data'] = "Ошибка при удалении аккаунта"

        finally:
            self.close_connection()
            return res

    def delete_worker(self, name, address):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT global_id " \
                       f" FROM worker " \
                       f" WHERE name ='{name}' AND address ='{address}';"
            self.cursor.execute(str_exec)
            res_temp = self.cursor.fetchone()

            if res_temp is None:
                res['status'] = False
                res['data'] = "Такого пользователя нет"
            else:
                str_exec = f'DELETE FROM all_users WHERE id = {res_temp[0]} RETURNING id;'
                self.cursor.execute(str_exec)
                self.connection.commit()
                res['status'] = True
                res['data'] = "Аккаунт удален"

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['data'] = "Ошибка при удалении аккаунта"

        finally:
            self.close_connection()
            return res

    def change_info_customer(self, key, value, name, address):
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM customer" \
                       f" WHERE name = '{name}' AND" \
                       f" address = '{address}');"
            self.cursor.execute(str_exec)

            if self.cursor.fetchone()[0]:
                str_exec = f"UPDATE customer SET {key} = '{value}'" \
                       f" WHERE name = '{name}' AND" \
                       f" address = '{address}';"
                self.cursor.execute(str_exec)
                self.connection.commit()
                res['status'] = True
                res['message'] = "Информация обновлена"

            else:
                res['status'] = False
                res['message'] = "Такого пользователя не существует"

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['message'] = "Ошибка при изменение пользователя"

        finally:
            self.close_connection()
            return res

    def create_order(self, name_customer, address_customer, name_service, company):
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM orders" \
                       f" WHERE name_customer = '{name_customer}' AND" \
                       f" address_customer = '{address_customer}' AND" \
                       f" name_service = '{name_service}' AND" \
                       f" name_company = '{company[0]}' AND" \
                       f" name_address = '{company[1]}');"
            self.cursor.execute(str_exec)

            if self.cursor.fetchone()[0]:
                res['status'] = False
                res['message'] = "Такой заказ уже есть"

            else:
                str_exec = ""
                str_exec = str_exec + f'INSERT INTO orders (name_customer, address_customer,' \
                                      f' name_service, name_company, name_address) ' \
                                      f" VALUES ('{name_customer}', '{address_customer}', '{name_service}'," \
                                      f" '{company[0]}', '{company[1]}');"

                self.cursor.execute(str_exec)
                self.connection.commit()

                # если все удачно, то запоминаем результат
                res['status'] = True
                res['message'] = "Заказ добавлен"

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['message'] = "Ошибка при создание заказа"

        finally:
            self.close_connection()
            return res

    def list_of_orders_for_customer(self, name_customer, address_customer):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT name_service, name_company, name_address " \
                       f" FROM orders " \
                       f" WHERE name_customer ='{name_customer}' AND address_customer ='{address_customer}';"
            self.cursor.execute(str_exec)
            res_temp = self.cursor.fetchall()

            if len(res_temp) == 0:
                res['status'] = False
                res['data'] = "Нет заказов"
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

    def change_info_worker(self, key, value, name, address, name_company, name_address):
        res = dict()
        try:
            self.connect()
            str_exec = f"SELECT EXISTS (SELECT * FROM worker" \
                       f" WHERE name = '{name}' AND" \
                       f" address = '{address}' AND" \
                       f" name_company = '{name_company}' AND" \
                       f" name_address = '{name_address}');"
            self.cursor.execute(str_exec)

            if self.cursor.fetchone()[0]:
                str_exec = f"UPDATE worker SET {key} = '{value}'" \
                           f" WHERE name = '{name}' AND" \
                           f" address = '{address}' AND" \
                           f" name_company = '{name_company}' AND" \
                           f" name_address = '{name_address}');"
                self.cursor.execute(str_exec)
                self.connection.commit()
                res['status'] = True
                res['message'] = "Информация обновлена"

            else:
                res['status'] = False
                res['message'] = "Такого пользователя не существует"

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['message'] = "Ошибка при изменение пользователя"

        finally:
            self.close_connection()
            return res

    def delete_order(self, name_company, address, data):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
            self.connect()
            str_exec = f"DELETE FROM orders WHERE name_customer = '{data[0]}' AND" \
                       f" address_customer = '{data[1]}' AND name_service = '{data[2]}' AND " \
                       f" name_company = '{name_company}' AND name_address = '{address}';"
            self.cursor.execute(str_exec)
            self.connection.commit()
            res['status'] = True
            res['data'] = "Заказ выполнен"

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['data'] = "Произошла ошибка"

        finally:
            self.close_connection()
            return res


