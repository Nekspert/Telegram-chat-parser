import sqlite3 as sql


class DataBase:
    def __init__(self, name_db: str) -> None:
        self.connect = sql.connect(f'{name_db}.db')
        self.cursor = self.connect.cursor()

    async def create_table(self, name_table: str, columns: tuple[tuple]) -> None:
        try:
            columns_definitions = ', '.join([f'{col_name} {col_type}' for col_name, col_type in columns])
            # print(columns_async definitions)
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {name_table} ({columns_definitions})')
            self.connect.commit()
        except sql.Error as ex:
            print('[!] Ошибка базы данных:', ex)
        except Exception as ex:
            print('[!] Общая ошибка:', ex)

    async def select_values(self, name_table: str, columns: tuple[str] | str, condition: str | None = None) -> list[
        tuple]:
        try:
            if isinstance(columns, tuple):
                columns = ', '.join(columns)
            query = f'SELECT {columns} FROM {name_table}'
            if condition is not None:
                query += f' WHERE {condition}'
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except sql.Error as ex:
            print('[!] Ошибка базы данных:', ex)
        except Exception as ex:
            print('[!] Общая ошибка:', ex)

    async def add_values_unique(self, name_table: str, values: tuple) -> None:
        try:
            # print(self.cursor.execute(f'PRAGMA table_info("{name_table}")').fetchall())
            # PRAGMA table_info - return columns
            data = await self.select_values(name_table=name_table, columns=
            self.cursor.execute(f'PRAGMA table_info("{name_table}")').fetchone()[1])
            if (values[0],) not in data:
                amount: str = '?, ' * len(values)
                self.cursor.executemany(f'INSERT INTO {name_table} VALUES ({amount[:-2]})', (values,))
                self.connect.commit()
                res: list[str] = [str(i)[:100] for i in values]
                print(f'[*] Added value to the "{name_table}": {res}')
            else:
                pass
        except sql.Error as ex:
            print('[!] Ошибка базы данных:', ex)
        except Exception as ex:
            print('[!] Общая ошибка:', ex)

    async def add_values_repetitive(self, name_table: str, values: tuple[tuple | str | int]) -> None:
        try:
            amount: str = '?, ' * len(values)
            self.cursor.executemany(f'INSERT INTO {name_table} VALUES ({amount[:-2]})', (values,))
            self.connect.commit()
            res: list[str] = [str(i)[:50] for i in values]
            print(f'[*] Added value to the "{name_table}": {res}')
        except sql.Error as ex:
            print('[!] Ошибка базы данных:', ex)
        except Exception as ex:
            print('[!] Общая ошибка:', ex)

    async def update_column_value(self, name_table: str, column_name: str, new_value: str, condition_column: str,
                                  condition_value: str):
        try:
            # Получение старого значения
            self.cursor.execute(f"SELECT {column_name} FROM {name_table} WHERE {condition_column} = ?",
                                (condition_value,))
            old_value = self.cursor.fetchone()
            if old_value is not None:
                old_value = old_value[0]
                # Новое значение
                updated_value = old_value + '\n' + new_value
                # Обновление значения в столбце
                self.cursor.execute(f"UPDATE {name_table} SET {column_name} = ? WHERE {condition_column} = ?",
                                    (updated_value, condition_value))
                self.connect.commit()
                print(f"Value updated")
                # print(f"Value updated: {old_value} + {new_value} = {updated_value}")
            else:
                print(f"No record found where {condition_column} = {condition_value}")
        except sql.Error as ex:
            print('[!] Ошибка базы данных:', ex)
        except Exception as ex:
            print('[!] Общая ошибка:', ex)

    async def update_values(self, name_table: str, expression: str, condition: str | None = None) -> None:
        try:
            if condition is None:
                if expression.split()[-1].isdigit():
                    self.cursor.execute(f'UPDATE {name_table} SET {expression}')
                else:
                    self.cursor.execute(
                        f"UPDATE {name_table} SET {expression.split('=')[0]} = '{expression.split('=')[1].strip()}'")
            else:
                if expression.split()[-1].isdigit():
                    self.cursor.execute(f'UPDATE {name_table} SET {expression} WHERE {condition}')
                else:
                    self.cursor.execute(
                        f"UPDATE {name_table} SET {expression.split('=')[0]} = '{expression.split('=')[1].strip()}' WHERE {condition}")
            self.connect.commit()
            print(f'[*] Updated "{expression}" from "{name_table}" where condition: {condition}')
        except sql.Error as ex:
            print('[!] Ошибка базы данных:', ex)
        except Exception as ex:
            print('[!] Общая ошибка:', ex)

    async def delete_column_value(self, name_table: str, column_name: str, index: int, condition: str):
        try:
            # Получение старого значения
            self.cursor.execute(f"SELECT {column_name} FROM {name_table} WHERE {condition}")
            old_value = self.cursor.fetchone()
            if old_value is not None:
                old_value: list = old_value[0].split('\n')
                del old_value[index - 1]
                # Новое значение ..............изначально + 1.............
                updated_value = '\n'.join(old_value)
                # Обновление значения в столбце
                self.cursor.execute(f"UPDATE {name_table} SET {column_name} = ? WHERE {condition}", (updated_value,))
                self.connect.commit()
                print(f"Old value deleted")
                # print(f"Value updated: {old_value} + {new_value} = {updated_value}")
            else:
                print(f"No record found where {condition}")
        except sql.Error as ex:
            print('[!] Ошибка базы данных:', ex)
        except Exception as ex:
            print('[!] Общая ошибка:', ex)

    async def delete_row(self, name_table: str, condition: str):
        # try:
        self.cursor.execute(f'DELETE FROM {name_table} WHERE {condition}')
        self.connect.commit()
        print(f'[*] DELETE FROM {name_table} WHERE {condition}')

    # except sql.Error as ex:
    #     print('[!] Ошибка базы данных:', ex)
    # except Exception as ex:
    #     print('[!] Общая ошибка:', ex)

    async def drop_table(self, name_table: str) -> None:
        try:
            self.cursor.execute(f'DROP TABLE {name_table}')
            self.connect.commit()
            print(f'[*] Dropped "{name_table}"')
        except sql.Error as ex:
            print('[!] Ошибка базы данных:', ex)
        except Exception as ex:
            print('[!] Общая ошибка:', ex)

    async def close_db(self):
        self.connect.close()
