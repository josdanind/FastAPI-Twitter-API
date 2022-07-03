from xml.sax.saxutils import prepare_input_source
import psycopg2
from decouple import config

# fastAPI
from fastapi import status, HTTPException

# libraries own
from utils.encrypt import context

db_config = {
    "host": config('DB_HOST'),
    "port": config('DB_PORT'),
    "user": config('DB_USER'),
    "dbname": config('DB_NAME'),
    "password": config('DB_PASS'),
}

class ConnectDB:
    with_commit = ["INSERT", "DELETE", "UPDATE"]
    without_commit = ["SELECT"]

    def __init__(self, config:dict, table:str) -> None:
        self.credentials = config
        self.table = table
        self.connect = None
        self.cursor = None
        self.on = False
    
    @property
    def table(self):
        return self.__table
    
    @table.setter
    def table(self, table):
        self.__table = table
    
    @property
    def on(self):
        return self.__on

    @on.setter
    def on(self, connection):
        try:
            if type(connection) != bool:
                raise ValueError(
                    "Error: "
                    "The .on attribute only accepts a boolean value"
                    )

            if connection:
                self.__connect()
            else:
                if not self.connect and not self.cursor:
                    self.__on = False
                    return

                self.__disconnect()
        except ValueError as err:
            print(err)

    def __connect(self):
        self.connect = psycopg2.connect(**self.credentials)
        self.cursor = self.connect.cursor()
        self.__on = True

    def __disconnect(self):
        self.cursor.close()
        self.connect.close()
        self.__on = False

    def __execute_query(self, query, action):
        try:
            if action in self.without_commit:
                self.cursor.execute(query)
                values = self.cursor.fetchone()

                if values:
                    column_names = [head[0] for head in self.cursor.description]
                    data = dict(zip(column_names, values))
                    return data
            else:
                self.cursor.execute(query)
                self.connect.commit()
        except psycopg2.OperationalError as err:
            print("DataBase Error")
            print(err)

    def existence(self, message, error_if_exist=True, **to_search):
        first_key =  next(iter(to_search))
        first_value = to_search[first_key]
        result = self.select_row(**{f'{first_key}': first_value})
        if error_if_exist:
            if result:
                raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=message)
        else:
            if not result:
                raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=message)
            else:
                return result

    def select_row(self, **to_search):
        first_key= next(iter(to_search))
        first_value = to_search[first_key]

        query = f"SELECT * FROM {self.__table} WHERE {first_key}='{first_value}'"
        return self.__execute_query(query, "SELECT")

    def select_all(self):
        query = f"SELECT * FROM {self.__table}"
        self.cursor.execute(query)
        users_data =  self.cursor.fetchall()
        column_names = [head[0] for head in self.cursor.description]
        response_data = [dict(zip(column_names, data)) for data in users_data]

        return response_data

    def insert_content(self, data):
        fields = ",".join(data.keys())
        values = ",".join(list(map(lambda x: f"'{x}'", data.values())))

        query = ("INSERT INTO "
        f"{self.__table}({fields}) "
        f"VALUES({values});"
        )

        self.__execute_query(query, "INSERT")

    def login_user(self, **credentials):
        try:
            for k in credentials.keys():
                if k in ["email", "nickname"]:
                    key = k
                    value = credentials[k]
                elif k == "password":
                    password = credentials[k]
                else:
                    raise KeyError(
                        'Error:'
                        'the key must be "email" or "nickname"'
                        ' and "password"')
        except KeyError as err:
            print(err)

        user_data = self.existence(
            message="The user does not exist!",
            error_if_exist=False,
            **{f'{key}': value}
        )

        hash_password = user_data["password"]

        if context.verify(password, hash_password):
            user_data['birth_date'] = str(user_data['birth_date'])
            user_data['message'] = 'Login success!'
            return user_data
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password")

    def delete_row(self, **condition):
        first_key= next(iter(condition))
        first_value = condition[first_key]

        query = f"DELETE FROM {self.__table} WHERE {first_key}='{first_value}'"

        self.__execute_query(query, "DELETE")

    def update_row(self, to_update, **condition):
        fields = []
        for k,v in to_update.items():
            if not to_update[k]:
                continue
            else:
                fields.append(f"{k}='{v}'")

        fields_str = ", ".join(fields)

        try:
            for k in condition.keys():
                if k in ["id", "email", "nickname"]:
                    key = k
                    value = condition[k]
                else:
                    raise KeyError(
                        'Error:'
                        'the key must be "id", "email", "nickname"')
        except KeyError as err:
            print(err)

        query = (f"UPDATE {self.__table} "
        f"SET {fields_str} "
        f"WHERE {key}='{value}';"
        )
        self.__execute_query(query, "UPDATE")
        
        
connect_db = ConnectDB(db_config, 'users')