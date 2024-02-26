from aiohttp import web
from postgreSQL import DataBaseManager
import aiohttp_jinja2
import jinja2

base = DataBaseManager()

app = web.Application()
aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader('C:\\Users\\Difrat\\Constructor\\Constructor_storage\\templates'))


@aiohttp_jinja2.template('index.html')
async def dynamic_table(request):
    await base.create_pool()
    texts = await base.read_from_table('stock')
    return {'texts': texts}


async def handle_form(request):
    with open('templates/form.html', encoding='utf-8') as f:
        return web.Response(text=f.read(), content_type='text/html')


async def menu(request):
    with open('templates/menu.html', encoding='utf-8') as f:
        return web.Response(text=f.read(), content_type='text/html')


async def create_table(request):
    with open('templates/create_new_table.html', encoding='utf-8') as f:
        return web.Response(text=f.read(), content_type='text/html')


async def add_str(request):
    data = await request.post()
    name = data.get('name')
    count = int(data.get('count'))
    cell = data.get('cell')
    await base.create_pool()
    await base.insert_into_table(name, count, cell)
    return web.HTTPFound('/index')


async def handle_submit(request):
    data = await request.post()
    name = data.get('name')
    count = data.get('count')
    cell = data.get('cell')
    return web.Response(text=f'Вы ввели имя:{name}, количество:{count}, ячейка:{cell}!')


async def create_new_table(request):
    data = await request.post()
    name = data.get('table_name')
    datatype = data.get('datatype')
    await base.create_pool()
    await base.create_table(name, datatype)
    return web.Response(text='table is created!')
# async def menu(request):
#     return aiohttp_jinja2.render_template('menu.html', request, {})
#
#
# async def create_table(request):
#     return aiohttp_jinja2.render_template('create_new_table.html', request, {})


app.router.add_post('/submit', handle_submit)
app.router.add_post('/add_str', add_str)
app.router.add_post('/create_new_table', create_new_table)
app.router.add_get('/index', dynamic_table)
app.router.add_get('/menu', menu)
app.router.add_get('/create_new_table', create_table)
app.router.add_get('/', handle_form)

web.run_app(app)
