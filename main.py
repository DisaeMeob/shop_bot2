import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import TOKEN, ADMIN_ID
from db import create_table, add_user, exists, get_users, get_stat
from tovar import create_table_order, add_order,exist_order,delete_order, create_stock, add_stock, exist_stock, delete_stock, get_order_name, get_stock_name,get_order_photo,get_stock_photo,update_stock,update_order

logging.basicConfig(level=logging.INFO)

create_table()
create_table_order()
create_stock()

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
    buy = State()
    vib = State()
    name = State()
    cost = State()
    photo = State()
    userbuy = State()
    buyintophoto = State()
    photosearch = State()
    broadcast = State()

class UpdateDel(StatesGroup):
    vib = State()
    name = State()
    cost = State()
    photo = State()
    upd = State()
    delete = State()
    delete2 = State()

user_kb = types.InlineKeyboardMarkup(row_width=2)
user_kb.add(
    types.InlineKeyboardButton(text='🛍 Товары', callback_data='buy'),
    types.InlineKeyboardButton(text='📸 Фотопоиск', callback_data='search'),
    types.InlineKeyboardButton(text='📢 Наши каналы', callback_data='telegram_chanel'),
    types.InlineKeyboardButton(text='❓ Помощь', callback_data='help')
)

vib = types.InlineKeyboardMarkup(row_width=2)
vib.add(
    types.InlineKeyboardButton(text='✅ В наличии', callback_data='stock'),
    types.InlineKeyboardButton(text='📦 Под заказ', callback_data='order'),
    types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit')
)

est = types.InlineKeyboardMarkup(row_width=1)
est.add(
    types.InlineKeyboardButton(text='🎒 Сумка arcteryx', callback_data='Сумка arcteryx'),
    types.InlineKeyboardButton(text='🧢 Шапка oakley', callback_data='Шапка oakley'),
    types.InlineKeyboardButton(text='👕 Футболка UTOPIA TRAVIS', callback_data='Футболка UTOPIA TRAVIS'),
    types.InlineKeyboardButton(text='🧣 Шарф ГОША РУБЧИНСКИЙ', callback_data='Шарф ГОША РУБЧИНСКИЙ'),
    types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit')
)

order_buy = types.InlineKeyboardMarkup(row_width=1)
order_buy.add(
    types.InlineKeyboardButton(text='👕 Футболка Lonsdale', callback_data='Футболка Lonsdale'),
    types.InlineKeyboardButton(text='🥋 Футболка Manto', callback_data='Футболка Manto'),
    types.InlineKeyboardButton(text='🧥 Футболка Stone Island', callback_data='Футболка Stone Island'),
    types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit')
)

order = ['Футболка Lonsdale', 'Футболка Manto', 'Футболка Stone Island']
stock = ['Сумка arcteryx', 'Шапка oakley', 'Футболка UTOPIA TRAVIS', 'Шарф ГОША РУБЧИНСКИЙ']
upd_list = order+stock
@dp.callback_query_handler(lambda call: call.data == 'exit', state='*')
async def exit(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer('Привет! Добро пожаловать в iypka_shop. Выберите опцию', reply_markup=user_kb)
    await state.finish()

stock_list = ['Сумка arcteryx','Шапка oakley','Футболка UTOPIA TRAVIS','Шарф ГОША РУБЧИНСКИЙ']

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Добро пожаловать в iypka_shop. Выберите опцию",reply_markup=user_kb)
    exist = exists(message.from_user.id)
    if not exist:
        add_user(message.from_user.id)

@dp.callback_query_handler(lambda call: call.data == 'help')
async def help(call: types.CallbackQuery):
    await call.answer()
    text = (
    "<b>ℹ️ Помощь</b>\n\n"
    "Добро пожаловать в раздел помощи! Ниже собраны ответы на самые частые вопросы 💬\n\n"
    
    "<b>📦 Как оформить заказ?</b>\n"
    "1. Нажмите кнопку <b>«Список товаров»</b>\n"
    "2. Выберите категорию: <b>В наличии</b> или <b>Под заказ</b>\n"
    "3. Найдите нужный товар, нажмите на него\n"
    "4. Нажмите кнопку <b>«Фото товара»</b>, чтобы посмотреть изображение\n"
    "5. Если всё устраивает — нажмите <b>«Купить»</b> и подтвердите заявку\n\n"

    "<b>❗Что значит «Под заказ»?</b>\n"
    "Товары <b>под заказ</b> доставляются по предоплате.\n"
    "⏳ Срок доставки — <b>до 14 дней</b>\n\n"

    "<b>💳 Способы оплаты</b>\n"
    "— Kaspi\n"
    "— Halyk Bank\n"
    "(реквизиты предоставим после подтверждения заказа)\n\n"

    "<b>💬 У меня вопрос или нужна консультация</b>\n"
    "Напишите напрямую админу — <a href='https://t.me/feaagff'>@feaagff</a>\n\n"

    "<b>📍 Где находится магазин?</b>\n"
    "Мы работаем <b>онлайн</b>. Возможна доставка или самовывоз по договорённости.\n\n"

    "<b>📸 Не нашли нужный товар?</b>\n"
    "Отправьте фото или название — мы постараемся найти и заказать для вас."
)
    ext = types.InlineKeyboardMarkup()
    ext.add(types.InlineKeyboardButton(text='↩️ Выйти', callback_data='exit'))
    await call.message.edit_text(text, parse_mode='html', reply_markup=ext)

@dp.callback_query_handler(lambda call: call.data == 'search')
async def photosearch(call: types.CallbackQuery):
    await call.answer()
    ext = types.InlineKeyboardMarkup()
    ext.add(types.InlineKeyboardButton(text='↩️Выйти', callback_data='exit'))
    await call.message.edit_text(
        '''<b>🔍 Фотопоиск товара</b>\n\n
Отправьте нам <b>фото</b> интересующего вас товара или <b>опишите его текстом</b>. Мы постараемся найти или предложить похожие варианты 🛍️\n
Сообщение отправится напрямую админу — он свяжется с вами как можно скорее 💬\n
Если хотите — можете написать сразу: <a href='https://t.me/feaagff'>@feaagff</a>''',
        parse_mode='html',
        reply_markup=ext
    )
    await Form.photosearch.set()



@dp.callback_query_handler(lambda call: call.data == 'telegram_chanel')
async def telegram_channel(call: types.CallbackQuery):
    await call.answer()

    text = """
<b>📢 Наши каналы в Telegram:</b>

🔹 <b>Основной канал</b> — следите за новинками, акциями и пополнением ассортимента:
🛍 Вещи в наличии и под заказ  
📸 Удобная функция фотопоиска  
🚚 Доставка Казпочтой и СДЭК  

🔹 <b>Отзывы</b> — реальные мнения покупателей, фото и обратная связь после заказа.

Присоединяйтесь, чтобы ничего не пропустить!
"""

    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🔗 Перейти в основной канал", url="https://t.me/+3b0cODqHbYBmZTYy"),
        types.InlineKeyboardButton("💬 Смотреть отзывы", url="https://t.me/iyoka_shop_otziv"),
        types.InlineKeyboardButton("↩️ Назад", callback_data="exit")
    )

    await call.message.edit_text(text, parse_mode='html', reply_markup=kb)

@dp.message_handler(content_types=['photo'], state=Form.photosearch)
async def photo_to_admin(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    username = message.from_user.username or "Без username"

    await message.answer(
        '''✅ <b>Фото отправлено!</b>\n
Ожидайте ответ от администратора. Он свяжется с вами в ближайшее время.\n
Если срочно — напишите напрямую: <a href='https://t.me/feaagff'>@feaagff</a>''',
        parse_mode='html'
    )
    await bot.send_photo(
        ADMIN_ID,
        photo,
        caption=(
            f'📩 <b>Фотопоиск</b>\n'
            f'Пользователь: @{username}\n'
            f'ID: {message.from_user.id}\n'
            f'Отправил фото для поиска товара.'
        ),
        parse_mode='html'
    )
    await state.finish()
@dp.message_handler(content_types=['text'], state=Form.photosearch)
async def text_to_admin(message: types.Message, state: FSMContext):
    text = message.text
    username = message.from_user.username or "Без username"

    await message.answer(
        '''✅ <b>Сообщение отправлено!</b>\n
Администратор получил ваш запрос и скоро ответит.\n
Если хотите ускорить процесс — напишите ему напрямую: <a href='https://t.me/feaagff'>@feaagff</a>''',
        parse_mode='html'
    )
    await bot.send_message(
        ADMIN_ID,
        f'📩 <b>Фотопоиск</b>\nПользователь: @{username}\nID: {message.from_user.id}\nТекст запроса: <b>{text}</b>',
        parse_mode='html'
    )
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == 'buy')
async def buy(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        '📦 <b>Выберите категорию:</b>\n\n'
        '— <b>В наличии</b> — товары, которые доступны прямо сейчас\n'
        '— <b>Под заказ</b> — товары, которые мы доставим по предоплате',
        parse_mode='html',
        reply_markup=vib
    )
    await Form.buy.set()

order_list = ['stock', 'order']    

@dp.callback_query_handler(lambda call: call.data in order_list,state=Form.buy)
async def handle_buy_option(call: types.CallbackQuery):
    await call.answer()
    if call.data == 'stock':
        await call.message.edit_text(
            '🟢 <b>Товары в наличии</b>\n\n'
            'Выберите нужный товар из списка:',
            parse_mode='html',
            reply_markup=est
        )
        await Form.userbuy.set()
    elif call.data == 'order':
        await call.message.edit_text(
            '🛍 <b>Товары под заказ</b>\n\n'
            'Выберите интересующий вас товар:',
            parse_mode='html',
            reply_markup=order_buy
        )
        await Form.userbuy.set()
    

photo = types.InlineKeyboardMarkup()
photo.add(
    types.InlineKeyboardButton(text='📸 Фото товара', callback_data='photos'),
    types.InlineKeyboardButton(text='❌ Выйти', callback_data='exit')
)

@dp.callback_query_handler(lambda call: call.data in stock + order, state=Form.userbuy)
async def userbuy(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(name = call.data)
    await call.answer()
    orderexist = exist_order(call.data)
    stockexist = exist_stock(call.data)
    if orderexist:
            name, cost = get_order_name(call.data)
            await call.message.answer(
            f'📦 <b>{name}</b>\n💰 Стоимость: <b>{cost}тг</b>\n\nНажмите кнопку ниже, чтобы посмотреть фото:',
            parse_mode='html',
            reply_markup=photo
        )
    elif stockexist:
        name, cost = get_stock_name(call.data)
        await call.message.answer(
            f'📦 <b>{name}</b>\n💰 Стоимость: <b>{cost}тг</b>\n\nНажмите кнопку ниже, чтобы посмотреть фото:',
            parse_mode='html',
            reply_markup=photo
        )
    else:
        await call.message.answer(
            '⚠️ Этот товар ещё не добавлен. Пожалуйста, выберите другой.'
        )
        return
    
    
@dp.callback_query_handler(lambda call: call.data == 'photos', state = Form.userbuy)
async def photos(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    name = data['name']
    print('📦 Данные из state:', data)
    print('🔎 Проверка в базе:')
    print('exist_stock:', exist_stock(name))
    print('exist_order:', exist_order(name))
    print('get_stock_photo:', get_stock_photo(name))
    print('get_order_photo:', get_order_photo(name))
    stock = exist_stock(name)
    in_order = exist_order(name)

    buy = types.InlineKeyboardMarkup(row_width=2)
    buy.add(
        types.InlineKeyboardButton(text='🛒 Купить', callback_data='buyintophoto'),
        types.InlineKeyboardButton(text='↩️ Назад', callback_data='exit')
    )
    if stock:
        photo = get_stock_photo(name)
        if photo:
            await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=f'📸 Фото товара: <b>{name}</b>',
            parse_mode='html',
            reply_markup=buy
        )
        else:
            await call.message.answer('Фото для этого товара не найдено')
    elif in_order:
        photo = get_order_photo(name)
        if photo:
            await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=f'📸 Фото товара: <b>{name}</b>',
            parse_mode='html',
            reply_markup=buy
        )
        else:
            await call.message.answer('Фото для этого товара не найдено')
    else:
        await call.message.answer('Фото для этого товара не найдено')
    

@dp.callback_query_handler(lambda call: call.data == 'buyintophoto', state=Form.userbuy)
async def buyintophoto(call: types.CallbackQuery):
    yesno = types.InlineKeyboardMarkup(row_width=2)
    yesno.add(
        types.InlineKeyboardButton(text='✅ Да', callback_data='yes'),
        types.InlineKeyboardButton(text='❌ Нет', callback_data='no')
    )
    await call.answer()
    await call.message.answer(
        '❓ <b>Подтвердить покупку?</b>',
        parse_mode='html',
        reply_markup=yesno
    )
@dp.callback_query_handler(lambda call: call.data in ['yes','no'], state=Form.userbuy)
async def yesorno(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    if call.data == 'yes':
        await call.answer()
        await call.message.answer(
            f'✅Заявка на покупку товара <b>{name}</b> была отправлена администратору.\n'
            f'Дождитесь, пока он напишет вам, либо напишите @feaagff ❤️ /start',
            parse_mode='html'
        )
        await bot.send_message(
            ADMIN_ID,
            f'📥 <b>Новая заявка на покупку</b>\n\n'
            f'🔹 Товар: <b>{name}</b>\n'
            f'👤 Username: @{call.from_user.username or "—"}\n'
            f'🆔 ID: {call.from_user.id}',
            parse_mode='html'
        )
        await state.finish()

    elif call.data == 'no':
        await call.answer()
        await call.message.answer(
            f'❌ Заявка на покупку <b>{name}</b> отменена.',
            parse_mode='html'
        )
        await state.finish()



admin_kb = types.InlineKeyboardMarkup(row_width=1)
admin_kb.add(
    types.InlineKeyboardButton(text='➕ Добавить товар', callback_data='add_photo'),
    types.InlineKeyboardButton(text='📨 Рассылка по пользователям', callback_data='send_message'),
    types.InlineKeyboardButton(text='✏️ Обновить / ❌ Удалить товар', callback_data='update_delete'),
    types.InlineKeyboardButton(text='📊 Статистика', callback_data='stat'),
    types.InlineKeyboardButton(text='↩️ Выйти', callback_data='exit')
)



@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("Вы вошли в админ панель",reply_markup=admin_kb)
    else:
        await message.answer("Вы не являетесь администратором")
        return

@dp.callback_query_handler(lambda call: call.data == "update_delete")
async def upddel(call: types.CallbackQuery):
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton(text='➕ Добавить товар', callback_data='upd_photo'),
        types.InlineKeyboardButton(text='❌ Удалить товар', callback_data='del_photo'),
        types.InlineKeyboardButton(text='↩️ Выйти', callback_data='exit')
    )
    await call.answer()
    await call.message.edit_text('Выберите, что вы хотите сделать: ', reply_markup=kb)
    
@dp.callback_query_handler(lambda call: call.data in ['upd_photo','del_photo'])
async def delupd(call: types.CallbackQuery):
    if call.data == 'upd_photo':
        await call.answer()
        await call.message.edit_text('Выберите товар, который хотите обновить', reply_markup=vib)
        await UpdateDel.upd.set()
    elif call.data == 'del_photo':
        await call.answer()
        await call.message.edit_text('Выберите товар, который хотите удалить', reply_markup=vib)
        await UpdateDel.delete.set()
    else:
        await call.answer()
        await call.message.answer('Вы не выбрали что вы хотите сделать')
        return


@dp.callback_query_handler(state=UpdateDel.delete)
async def vib3(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    if call.data == 'stock':
        await call.message.edit_text('В наличии', reply_markup=est)
        await state.finish()
        await UpdateDel.delete2.set()
    elif call.data == 'order':
        await call.message.edit_text('Под заказ', reply_markup=order_buy)
        await UpdateDel.delete2.set()

@dp.callback_query_handler(lambda call: call.data in order + stock, state=UpdateDel.delete2)
async def vib2(call: types.CallbackQuery, state: FSMContext):
    yesno_kb = types.InlineKeyboardMarkup(row_width=2)
    yesno_kb.add(
    types.InlineKeyboardButton(text='✅ Да', callback_data='yes'),
    types.InlineKeyboardButton(text='❌ Нет', callback_data='no')
)
    await call.answer()
    await state.update_data(name = call.data)
    data = await state.get_data()
    name = data['name']
    await call.message.answer(f'Вы точно хотите удалить товар?{name}', reply_markup=yesno_kb)

@dp.callback_query_handler(lambda call: call.data in ['yes','no'],state=UpdateDel.delete2)
async def delete2(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    order = exist_order(name)
    stock = exist_stock(name)
    if call.data == 'yes':
        await call.answer()
        if stock:
            delete_stock(name)
            await call.message.edit_text('Товар удален из базы данных')
        elif order:
            delete_order(name)
            await call.message.edit_text('Товар удален из базы данных')
        else:
            await call.message.edit_text('Товар не найден в базе данных')
    elif call.data == 'no':
        await call.answer()
        await call.message.edit_text('Вы отменили удаление товара')
        return
    await state.finish()

@dp.callback_query_handler(state=UpdateDel.upd)
async def vib3(call: types.CallbackQuery):
    await call.answer()
    if call.data == 'stock':
        await call.message.edit_text('В наличии', reply_markup=est)
        await UpdateDel.name.set()
    elif call.data == 'order':
        await call.message.edit_text('Под заказ', reply_markup=order_buy)
        await UpdateDel.name.set()

@dp.callback_query_handler(state=UpdateDel.name)
async def vib4(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(name = call.data)
    await call.message.answer(f'Введите новую стоимость для товара {call.data}')
    await UpdateDel.cost.set()

@dp.message_handler(state=UpdateDel.cost)
async def vib5(message: types.Message, state: FSMContext):
    await state.update_data(cost = message.text)
    await message.answer('Выберите обновленное фото для товара')
    await UpdateDel.photo.set()

@dp.message_handler(content_types=['photo'], state=UpdateDel.photo)
async def vib6(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    name = data['name']
    cost = data['cost']
    order = exist_order(name)
    stock = exist_stock(name)
    print("🔍 Проверка:")
    print("name:", name)
    print("exist_order:", exist_order(name))
    print("exist_stock:", exist_stock(name))

    if order:
        update_order(cost,photo,name)
        await message.answer(f'✅ Товар <b>{name}</b> обновлен.\nТеперь его стоимость: <b>{cost}тг</b>', parse_mode='html')
        await state.finish()
    elif stock:
        update_stock(cost,photo,name)
        await message.answer(f'✅ Товар <b>{name}</b> обновлен.\nТеперь его стоимость: <b>{cost}тг</b>', parse_mode='html')
        await state.finish()
    else:
        await message.answer(f'❌ Товар <b>{name}</b> не найден. Проверьте название.', parse_mode='html')
        await state.finish()




@dp.callback_query_handler(lambda call: call.data == 'add_photo')
async def add_photo(call: types.CallbackQuery):
    await call.answer()
    await call.message.edit_text('Выберите куда вы хотите добавить фото и установить стоимость', reply_markup=vib)
    await Form.vib.set()

@dp.callback_query_handler(lambda call: call.data in ['stock','order'],state=Form.vib)
async def vib2(call: types.CallbackQuery):
    await call.answer()
    if call.data == 'stock':
        await call.message.edit_text('В наличии', reply_markup=est)
        await Form.buy.set()
    elif call.data == 'order':
        await call.message.edit_text('Под заказ', reply_markup=order_buy)
        await Form.buy.set()
    

@dp.callback_query_handler(state=Form.buy)
async def getname(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(name=call.data)
    await call.message.answer(f'Введите стоимость для товара: <b>{call.data}</b>', parse_mode='html')
    await Form.cost.set()

@dp.message_handler(state=Form.cost)
async def getcost(message: types.Message, state: FSMContext):
    await state.update_data(cost=message.text)
    await message.answer(f'Отправьте фото для товара')
    await Form.photo.set()

@dp.message_handler(content_types=['photo'], state=Form.photo)
async def getphoto(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    name = data['name']
    cost = data['cost']
    
    orderresult = exist_order(name)
    stockresult = exist_stock(name)
    if orderresult:
        await message.answer('Ваш товар находится в БД заказа, перейдите во влкадку обновления товара')
    elif stockresult:
         await message.answer('Ваш товар находится в БД наличия, перейдите во влкадку обновления товара')
    else:
        if name in order:
            add_order(name, cost, photo)
            await message.answer(f'Товар <b>{name}</b> стоимостью <b>{cost}</b> - добавлен в БД заказа', parse_mode='html')
        elif name in stock:
            add_stock(name,cost,photo)
            await message.answer(f'Товар <b>{name}</b> стоимостью <b>{cost}</b> - добавлен в БД наличия', parse_mode='html')
    await state.finish()

@dp.callback_query_handler(lambda call: call.data == 'send_message')
async def broadcast(call: types.CallbackQuery):
    await call.answer()
    await call.message.answer('📨 Введите сообщение, которое хотите отправить всем пользователям: ')
    await Form.broadcast.set()

@dp.message_handler(state=Form.broadcast)
async def send_message(message: types.Message, state: FSMContext):
    users = get_users()
    text = message.text 
    success = 0
    failed = 0
    for user in users:
        try:
            await bot.send_message(user, text)
            success += 1
            await state.finish()
        except:
            failed += 1
            await state.finish()
    await message.answer(
        f"✅ Рассылка завершена\n\n"
        f"👥 Получили сообщение: <b>{success}</b>\n"
        f"⚠️ Ошибок при отправке: <b>{failed}</b>",
        parse_mode='html'
    )

@dp.callback_query_handler(lambda call: call.data == 'stat')
async def stat(call: types.CallbackQuery):
    await call.answer()
    users = get_stat()
    if not users:
        await call.message.answer('❌ Нет пользователей в базе.')
        return
    for user in users:
      await call.message.answer(f'🆔: {user[0]}')

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Я вас не понимаю, выберите опцию: ",reply_markup=user_kb)

    


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)
