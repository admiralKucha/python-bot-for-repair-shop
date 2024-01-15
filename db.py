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
                student_id = self.cursor.fetchone()[0]

                # если все удачно, то запоминаем результат
                res['status'] = True
                res['data'] = student_id

        except (Exception, Error) as error:
            res['status'] = False
            res['message'] = "Ошибка при создание аккаунта"
            self.close_connection()

        finally:
            return res

    def create_customer(self, name, address, phone_number, global_id):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
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

        except (Exception, Error) as error:
            res['status'] = False
            res['message'] = "Ошибка при создание аккаунта"

        finally:
            self.close_connection()
            return res

    def create_company(self, name, address, phone_number, owner, time_work, global_id):
        # выводим всех неподтвержденных пользователей
        res = dict()
        try:
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

        except (Exception, Error) as error:
            print(error)
            res['status'] = False
            res['message'] = "Ошибка при создание аккаунта"

        finally:
            self.close_connection()
            return res
