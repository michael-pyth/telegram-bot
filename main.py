from pyrogram import Client, filters
import config, datetime, keyboards, random, json, base64, os, asyncio
from FusionBrain_AI import generate
from pyrogram.types import ForceReply

bot = Client(
    "bozoBot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

def button_filter(button):
    async def func(_, __, msg):
        return msg.text == button.text
    return filters.create(func, "ButtonFilter", button=button)

def load_users():
    with open('users.json', 'r') as file:
        return json.load(file)

def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file)

def ensure_user(users, user_id):
    if str(user_id) not in users:
        users[str(user_id)] = {
            "tokens": 100,
            "settings": {
                "width": 1024,
                "height": 1024,
                "style": "DEFAULT"
            }
        }

@bot.on_message(filters.command('start'))
async def start(client, message):
    await message.reply('i have awoken (use the menu with the weird 4 balls for convenience)',
                        reply_markup=keyboards.kb_main)
    await client.send_photo(message.chat.id, 'files/cat.jpg')
    users = load_users()
    ensure_user(users, message.from_user.id)
    save_users(users)

@bot.on_message(filters.command('info') | button_filter(keyboards.btn_info))
async def info(client, message):
    await message.reply('i am some random bot with some functions (but i am stupid)')

@bot.on_message(filters.command('time') | button_filter(keyboards.btn_time))
async def time(client, message):
    await message.reply(str(datetime.datetime.now()))

@bot.on_message(filters.command('games') | button_filter(keyboards.btn_games))
async def games(client, message):
    await message.reply('choose', reply_markup=keyboards.kb_games)

@bot.on_message(filters.command('back') | button_filter(keyboards.btn_back))
async def back(client, message):
    await message.reply('main menu', reply_markup=keyboards.kb_main)

@bot.on_message(filters.command('profile') | button_filter(keyboards.btn_profile))
async def profile(client, message):
    users = load_users()
    await message.reply(f'user id:{message.from_user.id}, {users[str(message.from_user.id)]["tokens"]} tokens')

@bot.on_message(filters.command('rock paper scissors') | button_filter(keyboards.btn_rps))
async def rps(client, message):
    users = load_users()
    ensure_user(users, message.from_user.id)
    if users[str(message.from_user.id)]["tokens"] >= 10:
        await message.reply('you', reply_markup=keyboards.kb_rps)
    else:
        await message.reply(f'broke, you have {users[str(message.from_user.id)]["tokens"]}, minimum is 10')

@bot.on_message(button_filter(keyboards.btn_rock) |
                button_filter(keyboards.btn_paper) |
                button_filter(keyboards.btn_scissors))
async def choice_rps(client, message):
    rock = keyboards.btn_rock.text
    paper = keyboards.btn_paper.text
    scissors = keyboards.btn_scissors.text
    user = message.text
    pc = random.choice([rock, paper, scissors])
    users = load_users()
    if user == pc:
        await message.reply('draw')
    elif (user == paper and pc == rock) or (user == rock and pc == scissors) or (user == scissors and pc == paper):
        await message.reply(f'win, bot chose {pc}')
        users[str(message.from_user.id)]["tokens"] += 10
    elif (user == paper and pc == scissors) or (user == rock and pc == paper) or (user == scissors and pc == rock):
        await message.reply(f'loss, bot chose {pc}')
        users[str(message.from_user.id)]["tokens"] -= 10
    save_users(users)

@bot.on_message(filters.command('quest') | button_filter(keyboards.btn_quest))
async def quest(client, message):
    await message.reply_text('quest?',
                             reply_markup=keyboards.inline_kb_start_quest)

@bot.on_callback_query()
async def handle_query(client, query):
    if query.data == 'start_quest':
        await client.answer_callback_query(query.id, text='welcome to the stupid quest which only losers would try', show_alert=True)
        await query.message.reply_text('you start on a mountain with an overhang, theres a small cliff and an icicle, whats the first thing you do?', reply_markup=keyboards.inline_kb_1)
    elif query.data == 'cliff':
        await client.send_voice(chat_id=query.message.chat.id, voice='AwACAgQAAxkDAAIBhGiWIqwt-elbBUr5S9HDGYy6PEERAAImGQAC6E-4UPrqUqAPEjD-HgQ')
        await query.message.reply_text('you land in a small flower patch, reminding you of a game you played, what do you do', reply_markup=keyboards.inline_kb_fallen)
    elif query.data == 'icicle':
        await query.message.reply_text('you grab the icicle, but you slip into a glacier, what do you do', reply_markup=keyboards.inline_kb_glacier)
    elif query.data == 'explore':
        await query.message.reply_text('you decided to explore, and you find a living flower named "Flowey", what do you do', reply_markup=keyboards.inline_kb_explore)
    elif query.data == 'climbend':
        await query.message.reply_text('you decided to climb back out. after you got out you decided that its too risky to stay here and went back where you came from')
    elif query.data == 'fightflowey':
        await query.message.reply_text('you are fighting at full strength, but its not enough, until a cow like being appears with the name "Toriel" and saves you. it takes you to its house and acts as a loving mother, what do you do', reply_markup=keyboards.inline_kb_toriel)
    elif query.data == 'floweydeath':
        await query.message.reply_text('you try to run away, but to no avail, his pellets penetrate your heart and you drop dead')
    elif query.data == 'happy':
        await query.message.reply_text('you decided its best to stay with her, shes also happy, you have a great life down in the house')
    elif query.data == 'dungeondeath':
        await query.message.reply_text('you decide to run away through the mysterious door in the basement. you dont make it far until the monsters brutally murder you and take your soul')
    elif query.data == 'village':
        await query.message.reply_text('you decide to go deeper into the glacier, when it suddenly opens up to a village, what do you do', reply_markup=keyboards.inline_kb_village)
    elif query.data == 'icicleclimbend':
        await query.message.reply_text('you use the icicle to climb back up out of the glacier and decide its not safe around here and go back home')
    elif query.data == 'newlife':
        await query.message.reply_text('after starting your new life, you help everyone in the village. and after many years you eventually become village chief')
    elif query.data == 'robberdeath':
        await query.message.reply_text('you decided to run away, but not long after you find robbers. the robbers think that your organs may be valuable on the black market and kill you')
    await query.message.delete()

@bot.on_message(filters.command('setwidth'))
async def set_width(client, message):
    await message.reply_text('use multiples of 64 for better results')
    users = load_users()
    ensure_user(users, message.from_user.id)
    try:
        width = int(message.text.split()[1])
        users[str(message.from_user.id)]['settings']['width'] = width
        await message.reply(f'set width to {width}')
        save_users(users)
    except:
        await message.reply(f'current: /setwidth {users[str(message.from_user.id)]['settings']['width']}')

@bot.on_message(filters.command('setheight'))
async def set_height(client, message):
    await message.reply_text('use multiples of 64 for better results')
    users = load_users()
    ensure_user(users, message.from_user.id)
    try:
        height = int(message.text.split()[1])
        users[str(message.from_user.id)]['settings']['height'] = height
        await message.reply(f'set height to {height}')
        save_users(users)
    except:
        await message.reply(f'current: /setheight {users[str(message.from_user.id)]['settings']['height']}')

@bot.on_message(filters.command('setstyle'))
async def set_style(client, message):
    await message.reply_text('styles: KANDINSKY, UHD, ANIME, DEFAULT (has to be full caps)')
    users = load_users()
    ensure_user(users, message.from_user.id)
    try:
        style = message.text.split()[1].upper()
        users[str(message.from_user.id)]['settings']['style'] = style
        await message.reply(f'set style to {style}')
        save_users(users)
    except:
        await message.reply(f'current: /setstyle {users[str(message.from_user.id)]['settings']['style']}')

@bot.on_message(filters.command('image'))
async def image(client, message):
    users = load_users()
    ensure_user(users, message.from_user.id)
    if len(message.text.split()) > 1:
        query = message.text.replace('/image', '').strip()
        await message.reply_text(f'tip: there are commands to change some settings(hint, these: /setstyle, /setheight, /setwidth')
        await message.reply_text(f'generating image with prompt {query}, wait')
        images = await generate(query, settings=users[str(message.from_user.id)]['settings'])
        if images:
            image_data = base64.b64decode(images[0])
            random_number = random.randint(1, 10000)
            filename = f'images/image{random_number}.jpg'
            with open(filename, 'wb') as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, filename, reply_to_message_id=message.id)
            os.remove(filename)
        else:
            await message.reply_text('error, try again', reply_to_message_id=message.id)
    else:
        await message.reply_text('prompt missing')

query_text = 'prompt'
@bot.on_message(button_filter(keyboards.btn_image))
async def image_command(client, message):
    await message.reply(query_text, reply_markup=ForceReply(True))

@bot.on_message(filters.reply)
async def reply(client, message):
    if message.reply_to_message.text == query_text:
        users = load_users()
        ensure_user(users, message.from_user.id)
        query = message.text
        await message.reply_text(f'generating image with prompt {query}, wait')
        images = await generate(query, settings=users[str(message.from_user.id)]['settings'])
        if images:
            image_data = base64.b64decode(images[0])
            random_number = random.randint(1, 10000)
            filename = f'images/image{random_number}.jpg'
            with open(filename, 'wb') as file:
                file.write(image_data)
            await bot.send_photo(message.chat.id, filename, reply_to_message_id=message.id)
            os.remove(filename)
        else:
            await message.reply_text('error, try again', reply_to_message_id=message.id)

@bot.on_message(filters.command('gamble'))
async def gamble(client, message):
    amount = 0
    users = load_users()
    await message.reply_text('chance to win is 1%, losing = wager lost, winning = wager x5')
    await message.reply_text(f'how much to wager? currently you have: {users[str(message.from_user.id)]["tokens"]}')
    try:
        amount = int(message.text.split()[1])
        if amount > 0 and amount <= users[str(message.from_user.id)]["tokens"]:
            gen_num = random.randint(1, 100)
            users[str(message.from_user.id)]["tokens"] -= amount
            await message.reply_text('the 100 sided dice is rolling...')
            await asyncio.sleep(3)
            if gen_num == 77:
                await message.reply_text('you won wager got quintupled')
                users[str(message.from_user.id)]["tokens"] += amount * 5
            else:
                await message.reply_text('you lost everything you wagered..')
            save_users(users)
        else:
            await message.reply_text('invalid amount or insufficient tokens')
    except Exception:
        await message.reply_text('failed to start process, nothing was lost')

@bot.on_message()
async def echo(client, message):
    if not message.text:
        return
    msg = message.text.lower()
    if msg in ['hello', 'hi', 'sup']:
        await message.reply('no')
    elif msg in ['bye', 'goodbye']:
        await message.reply('bye (and stay away)')
    else:
        await message.reply(f'you wrote: {message.text}')

bot.run()