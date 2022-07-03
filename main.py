from pyrogram import Client
from pyrogram import filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
import redis 
import sqlite3
from pyrogram.errors import UserIsBlocked, UserNotParticipant
from pyrogram import enums
import base64

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                                             # 
# first change token and api_key and api_hash (31 tp 33)                                                      #
# admin bot in your channel                                                                                   #
# then change bot_id and channel_id and channel_username (359 to 361)                                         #
# if you don't want to check user is in channel or not, change this 67 line to command and change 314 to pass #
# you can change راجع به ربات text at line 137                                                                #
#                                                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                                                             #
# Telegram : @iliyafaramarzi , iliya_faramarzi                                                                #
# Instagram : faramarziiliya                                                                                  #
# Github : iiyafaramarzi                                                                                      #
#                                                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

token = 'your bot token'
ApiKey = 11111111
ApiHash = 'your api hash'


# # # # # # # # # # # # # # # # # # # # # # # # # # # TOP SECRET # # # # # # # # # # # # # # # # # # # # # # # # # # #  

def encrypt(message):
    cipher = ''
    for letter in message:
        if letter == ' ':
            cipher += ' '
        elif letter == 'z':
            cipher += 'a'
        else:
            cipher += chr(ord(letter) + 1)
    return cipher

def decrypt(cipher):
    message = ''
    for letter in cipher:
        if letter == ' ':
            message += ' '
        elif letter == 'a':
            message += 'z'
        else:
            message += chr(ord(letter) - 1)
    return message

# # # # # # # # # # # # # # # # # # # # # # # # # # # TOP SECRET # # # # # # # # # # # # # # # # # # # # # # # # # # #  

app = Client('unknown caht bot', bot_token = token, api_id = ApiKey, api_hash = ApiHash)
r = redis.Redis(host='localhost', port=6379, db=0)
con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users(user_id TEXT, messages TEXT, blocked_users TEXT)')
con.commit()

print('bot is runing...')

@app.on_message(filters.private)
async def main(client, message):
    global panel_stat
    chat_id = message.chat.id
    message_id = message.id
    user_id = message.from_user.id
    text = message.text
    li = []
    try:
        li = text.split(' ')
    except:
        pass


    encode = encrypt(base64.b64encode(str.encode(str(chat_id))).decode('utf-8'))
    cur.execute(f'SELECT messages FROM users WHERE user_id = "{encode}"')
    if cur.fetchall() == []:
        cur.execute(f'INSERT OR IGNORE INTO users VALUES("{encode}", " ", ", ")')
        con.commit()


    try:
        await app.get_chat_member(int(channel_id), chat_id)

        if li != []:
            if li[0] == '/start' and len(li) == 2:
                cur.execute(f'SELECT blocked_users FROM users WHERE user_id = "{li[1]}"')
                blocked = cur.fetchall()[0][0]
                if str(chat_id) in blocked:
                    await app.send_message(chat_id, 'متاسفانه کاربر مورد نظر شما رو بلاک کرده☹️')

                elif encrypt(base64.b64encode(str.encode(str(chat_id))).decode('utf-8')) == li[1]:
                    await app.send_message(chat_id, 'شما نمیتونید به خودتون پیام بفرستید🤔')
                
                else:

                    about_user = await app.get_chat(base64.b64decode(decrypt(li[1])).decode('utf-8'))
                    await app.send_message(chat_id, f'شما در حال ارسال پیام ناشناس به {about_user.first_name} هستی.\n\nمی‌تونی هر حرف یا انتقادی که تو دلت هست رو بگی چون پیامت به صورت کاملا ناشناس ارسال می‌شه!', reply_markup=ReplyKeyboardMarkup(
                        [
                            ['انصراف']
                        ], resize_keyboard = True
                    ))
                    r.set(f'{user_id}', f'send-{li[1]}')
                
                return ''

            elif len(li) == 3 and li[0] == 'پیام' and li[1] == 'همگانی' and li[2] == '123258':
                panel_stat[chat_id] = 'message'
                await app.send_message(chat_id, 'لطفا پیام خود را ارسال کنید:')

        if panel_stat != {}:
            if panel_stat[chat_id] == 'message' and text != 'پیام همگانی 123258':
                cur.execute(f'SELECT user_id FROM users')
                users = cur.fetchall()

                await app.send_message(chat_id, 'پروسه ارسال پیام همگانی با موفقیت آغاز شد')
                for user in users:
                    user_ = base64.b64decode(decrypt(user[0])).decode('utf-8')
                    await app.copy_message(user_, chat_id, message_id)

                del panel_stat[chat_id]
                await app.send_message(chat_id, 'پروسه ارسال پیام همگانی با به اتمام رسید')  
        
        elif text == '/start':
            await app.send_message(chat_id, 'به ربات پیام ناشناس خوش آمدید.\n\nچه کاری برات انجام بدم؟🤔', reply_markup = ReplyKeyboardMarkup(
                [
                    ['دریافت لینک ناشناس📨', 'راجع به ربات']
                ], resize_keyboard = True
            ))

        elif text == 'راجع به ربات':
            await app.send_message(chat_id, 'Github : [iliyafaramarzi](https://github.com/iliyafaramarzi)\nTelegram : @iliyafaramarzi\nInstagram : [faramarziiliya](https://www.instagram.com/faramarziiliya/)')

        elif text == 'دریافت لینک ناشناس📨':
            encode = encrypt(base64.b64encode(str.encode(str(chat_id))).decode('utf-8'))
            await app.send_message(chat_id, f'سلام {message.from_user.first_name} هستم ✋️\n\nینک زیر رو لمس کن و هر حرفی که تو دلت هست یا هر انتقادی که نسبت به من داری رو با خیال راحت بنویس و بفرست. بدون اینکه از اسمت باخبر بشم پیامت به من می‌رسه. خودتم می‌تونی امتحان کنی و از بقیه بخوای راحت و ناشناس بهت پیام بفرستن، حرفای خیلی جالبی می‌شنوی! 😉\n\n[لینک ناشناس](t.me/{bot_id}?start={encode})')
            
        elif text == '/new':
            encode = encrypt(base64.b64encode(str.encode(str(chat_id))).decode('utf-8'))
            cur.execute(f'SELECT messages FROM users WHERE user_id = "{encode}"')
            messages = cur.fetchall()[0][0]
            if messages.strip() == '':
                await app.send_message(chat_id, 'به ربات پیام ناشناس خوش آمدید.\n\nچه کاری برات انجام بدم؟🤔', reply_markup = ReplyKeyboardMarkup(
                [
                    ['دریافت لینک ناشناس📨', 'راجع به ربات']
                ], resize_keyboard = True
                ))

            else:
                messagess = messages.split('|#')
                for counter, i in enumerate(messagess[1:]):
                    fin_message = i.split('+-+')
                    if len(fin_message) == 3:
                        await app.send_message(chat_id, fin_message[0], reply_to_message_id = int(fin_message[2]) , reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton('پاسخ✍️', callback_data = f'reply-{fin_message[1]}-{fin_message[2]}'),
                                    InlineKeyboardButton('بلاک❌', callback_data = f'block-{chat_id}-{fin_message[1]}')
                                ],
                            ]
                        ))
                        await app.send_message(int(fin_message[1]), 'مخاطب مورد نظرت این پیامت رو دید🥳', reply_to_message_id = int(fin_message[2]))
                        messagess.remove(i)
                        if counter == 9:
                            break

                    elif len(fin_message) == 5:
                        if fin_message[4] == 'voice':
                            await app.send_voice(chat_id, fin_message[3], fin_message[0], reply_to_message_id = int(fin_message[2]), reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton('پاسخ✍️', callback_data = f'reply-{fin_message[1]}-{fin_message[2]}'),
                                    InlineKeyboardButton('بلاک❌', callback_data = f'block-{chat_id}-{fin_message[1]}')
                                ],
                            ]))
                        
                        elif fin_message[4] == 'photo':
                            await app.send_photo(chat_id, fin_message[3], fin_message[0] ,reply_to_message_id = int(fin_message[2]), reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton('پاسخ✍️', callback_data = f'reply-{fin_message[1]}-{fin_message[2]}'),
                                    InlineKeyboardButton('بلاک❌', callback_data = f'block-{chat_id}-{fin_message[1]}')
                                ],
                            ]
                            ))

                        elif fin_message[4] == 'video_note':
                            await app.send_video_note(chat_id, fin_message[3], fin_message[0], fin_message[0] ,reply_to_message_id = int(fin_message[2]), reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton('پاسخ✍️', callback_data = f'reply-{fin_message[1]}-{fin_message[2]}'),
                                    InlineKeyboardButton('بلاک❌', callback_data = f'block-{chat_id}-{fin_message[1]}')
                                ],
                            ]))                                

                        elif fin_message[4] == 'animation':
                            await app.send_animation(chat_id, fin_message[3], fin_message[0], fin_message[0] ,reply_to_message_id = int(fin_message[2]), reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton('پاسخ✍️', callback_data = f'reply-{fin_message[1]}-{fin_message[2]}'),
                                    InlineKeyboardButton('بلاک❌', callback_data = f'block-{chat_id}-{fin_message[1]}')
                                ],
                            ]))

                        elif fin_message[4] == 'audio':
                            await app.send_audio(chat_id, fin_message[3], fin_message[0] ,reply_to_message_id = int(fin_message[2]), reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton('پاسخ✍️', callback_data = f'reply-{fin_message[1]}-{fin_message[2]}'),
                                    InlineKeyboardButton('بلاک❌', callback_data = f'block-{chat_id}-{fin_message[1]}')
                                ],
                            ]
                            ))

                        elif fin_message[4] == 'sticker':
                            await app.send_sticker(chat_id, fin_message[3], fin_message[0] , reply_markup = InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton('پاسخ✍️', callback_data = f'reply-{fin_message[1]}-{fin_message[2]}'),
                                    InlineKeyboardButton('بلاک❌', callback_data = f'block-{chat_id}-{fin_message[1]}')
                                ],
                            ]
                            ))


                        await app.send_message(int(fin_message[1]), 'مخاطب مورد نظرت این پیامت رو دید🥳', reply_to_message_id = int(fin_message[2]))
                        messagess.remove(i)
                        if counter == 9:
                            break

                    a = '|#'.join(messagess)
                    cur.execute(f'UPDATE users SET messages = "{a}" WHERE user_id = "{encode}"')
                    con.commit()

        elif r.exists(f'{user_id}') and text == 'انصراف':
            await app.send_message(chat_id, 'به ربات پیام ناشناس خوش آمدید.\n\nچه کاری برات انجام بدم؟🤔', reply_markup = ReplyKeyboardMarkup(
                [
                    ['دریافت لینک ناشناس📨', 'راجع به ربات']
                ], resize_keyboard = True
            ))

            r.delete(f'{user_id}')
            
        elif r.exists(f'{user_id}') and text != 'انصراف' and text != '/start' and text != '/new':
            user = r.get(f'{user_id}').decode("utf-8") 
            mode = user.split('-')
            try:
                file_id = ''
                if message.media == enums.MessageMediaType.VOICE:
                    file_id = message.voice.file_id
                    text = message.caption
                    file_type = 'voice'

                elif message.media == enums.MessageMediaType.VIDEO_NOTE:
                    file_id = message.video_note.file_id
                    text = message.caption
                    file_type = 'video_note'

                elif message.media == enums.MessageMediaType.STICKER:
                    file_id = message.sticker.file_id
                    text = message.caption
                    file_type = 'sticker'

                elif message.media == enums.MessageMediaType.ANIMATION:
                    file_id = message.animation.file_id
                    text = message.caption
                    file_type = 'animation'

                elif message.media == enums.MessageMediaType.PHOTO:
                    file_id = message.photo.file_id
                    text = message.caption
                    file_type = 'photo'

                elif message.media == enums.MessageMediaType.AUDIO:
                    file_id = message.audio.file_id
                    text = message.caption
                    file_type = 'audio'


                if message.media == enums.MessageMediaType.CONTACT or message.media == enums.MessageMediaType.LOCATION or message.media == enums.MessageMediaType.DOCUMENT or message.media == enums.MessageMediaType.VIDEO or message.media == enums.MessageMediaType.GAME or message.media == enums.MessageMediaType.POLL or message.media == enums.MessageMediaType.VENUE or message.media == enums.MessageMediaType.DICE or message.media == enums.MessageMediaType.WEB_PAGE:
                    await app.send_message(chat_id, 'به علت  حفظ حریم خصوصی کاربر ها شما اجازه ارسال این نوع پیام را ندارید❌')
                
                else:
                    if text == None:
                        text = ""

                    cur.execute(f'SELECT blocked_users FROM users WHERE user_id = "{mode[1]}"')
                    blocked = cur.fetchall()[0][0]
                    if str(chat_id) in blocked:
                        await app.send_message(chat_id, 'متاسفانه کاربر مورد نظر شما رو بلاک کرده☹️')
                    else:
                        if str(mode[0]) == "send":
                            cur.execute(f'SELECT messages FROM users WHERE user_id = "{mode[1]}"')
                            messages = cur.fetchall()[0][0]
                            if file_id == '':
                                messages += f'|#{text}+-+{chat_id}+-+{message_id}'
                            else:
                                messages += f'|#{text}+-+{chat_id}+-+{message_id}+-+{file_id}+-+{file_type}'
                            cur.execute(f'UPDATE users SET messages = "{messages}" WHERE user_id = "{mode[1]}"')
                            con.commit()
                            await app.send_message(int(base64.b64decode(decrypt(mode[1])).decode('utf-8')), 'شما یک پیام جدید دارید!\n\nبرای دیدن پیام های جدید از دستور /new استفاده کنید.')
                            r.delete(f'{user_id}')
                            await app.send_message(chat_id, 'به ربات پیام ناشناس خوش آمدید.\n\nچه کاری برات انجام بدم؟🤔', reply_markup = ReplyKeyboardMarkup(
                            [
                                ['دریافت لینک ناشناس📨', 'راجع به ربات']
                            ], resize_keyboard = True
                            ))

                        elif str(mode[0]) == "reply":
                            cur.execute(f'SELECT messages FROM users WHERE user_id = "{mode[1]}"')
                            messages = cur.fetchall()[0][0]
                            if file_id == '':
                                messages += f'|#{text}+-+{chat_id}+-+{message_id}'
                            else:
                                messages += f'|#{text}+-+{chat_id}+-+{message_id}+-+{file_id}+-+{file_type}'
                            cur.execute(f'UPDATE users SET messages = "{messages}" WHERE user_id = "{mode[1]}"')
                            con.commit()
                            await app.send_message(int(base64.b64decode(decrypt(mode[1])).decode('utf-8')), 'شما یک پیام جدید دارید!\n\nبرای دیدن پیام های جدید از دستور /new استفاده کنید.', reply_to_message_id = int(mode[2]))
                            r.delete(f'{user_id}')
                            await app.send_message(chat_id, 'به ربات پیام ناشناس خوش آمدید.\n\nچه کاری برات انجام بدم؟🤔', reply_markup = ReplyKeyboardMarkup(
                            [
                                ['دریافت لینک ناشناس📨', 'راجع به ربات']
                            ], resize_keyboard = True
                            ))

            except UserIsBlocked:
                await app.send_message(chat_id, 'ظاهرا کاربر مورد نظر ربات رو بلاک کرده☹️\n\nهروقت دوباره وارد ربات بشه حتما پیامت رو میبینه.')

        else:
            await app.send_message(chat_id, 'متوجه نشدم🧐')

    except UserNotParticipant: 
        await app.send_message(chat_id, f'برای کار کردن با ربات ابتدا در چنل زیر جوین شید: \n\n{channel_username}')


@app.on_callback_query()
async def main(client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    data = callback_query.data

    li = data.split('-')

    if li[0] == 'reply':
        encode = encrypt(base64.b64encode(str.encode(str(chat_id))).decode('utf-8'))
        cur.execute(f'SELECT blocked_users FROM users WHERE user_id = "{encode}"')
        blocked = cur.fetchall()[0][0]

        if str(chat_id) in blocked:
            await app.send_message(chat_id, 'مخاطب مورد نظر شما رو بلاک کرده☹️')
        else:
            about_user = await app.get_chat(li[1])
            await app.send_message(chat_id, f'شما در حال ارسال پیام ناشناس به {about_user.first_name} هستی.\n\nمی‌تونی هر حرف یا انتقادی که تو دلت هست رو بگی چون پیامت به صورت کاملا ناشناس ارسال می‌شه!', reply_markup=ReplyKeyboardMarkup(
                [
                    ['انصراف']
                ], resize_keyboard = True
            ))

            a = encrypt(base64.b64encode(str.encode(str(li[1]))).decode('utf-8'))
            r.set(f'{user_id}', f'reply-{a}-{li[2]}')

    elif li[0] == 'block':
        encode = encode = encrypt(base64.b64encode(str.encode(str(chat_id))).decode('utf-8'))
        cur.execute(f'SELECT blocked_users FROM users WHERE user_id = "{encode}"')
        blocked = cur.fetchall()[0][0]

        if not li[2] in blocked:
            blocked += f'{li[2]}, '
            cur.execute(f'UPDATE users SET blocked_users = "{blocked}" WHERE user_id = "{encode}"')
            con.commit()
            await app.answer_callback_query(callback_query.id, 'کاربر مورد نظر با موفقیت بلاک شد✅')

        else:
            blocked = blocked.replace(li[2], ', ')
            cur.execute(f'UPDATE users SET blocked_users = "{blocked}" WHERE user_id = "{encode}"')
            con.commit()
            await app.answer_callback_query( callback_query.id, 'کاربر مورد نظر با موفقیت آزاد شد✅')


bot_id = 'Hsuvsuxjdbudhdisbot'
channel_id = 'channel id to check user is joined or not' # if you don't want to check this you can command line 55 
channel_username = 'your channel username' # user name that bot send for users if they don't joined in channel 
panel_stat = {}
app.run()