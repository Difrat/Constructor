import asyncio
import asyncpg
import jinja2
import aiohttp_jinja2


# CRUD postgreSQL - готово
# Научится работать с пулом - готово
# Разабраться с пораметризованными запросами
class DataBaseManager():
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(user='postgres', password='GEl2Few#@;', database='const_db',
                                              host='localhost')

    # ID SERIAL PRIMARY KEY, NAME TEXT NOT NULL, COUNT INT NOT NULL, CELL TEXT NOT NULL, DATE DATE NOT NULL
    async def create_table(self, name: str, datatype: str):
        await self.pool.execute(
            f'CREATE TABLE IF NOT EXISTS {name}({datatype});')
        await self.pool.close()

    async def insert_into_table(self, name_itme, count_item, cell_item):
        await self.pool.execute('INSERT INTO new_table (name, count, cell, date) VALUES ($1, $2, $3, CURRENT_DATE)',
                                name_itme,
                                count_item, cell_item)
        await self.pool.close()

    async def read_from_table(self, table_name):
        result = [dict(r) for r in await self.pool.fetch(f'SELECT id, name, count, cell FROM {table_name}')]
        await self.pool.close()
        return result

    async def update_data(self):
        await self.pool.execute('UPDATE stock SET name = $1 WHERE id = 5;', 'toy')
        await self.pool.close()
        print('Значение обновлено!')

    async def delete_data(self):
        await self.pool.execute('DELETE FROM stock WHERE id = 2')
        await self.pool.close()
        print('Строка удалена!')
