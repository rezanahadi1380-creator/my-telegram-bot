from datetime import datetime
import json
import os
from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
import telebot

# توکن جدید شما
TOKEN = '8873507987:AAF6GbA-Qb1-oToegf99m91xnUTsSC07zEI'
ADMIN_ID = 6903327854
bot = telebot.TeleBot(TOKEN)

DATA_FILE = 'users.json'
CHANNELS = ['@cod_manii_yt', '@TRUST1_MANI']


def load_data():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
      return json.load(f)
  return {}


def save_data(data):
  with open(DATA_FILE, 'w') as f:
    json.dump(data, f)


def check_membership(user_id):
  for channel in CHANNELS:
    try:
      member = bot.get_chat_member(channel, user_id)
      if member.status not in ['member', 'administrator', 'creator']:
        return False
    except Exception:
      return False
  return True


def not_joined_markup():
  markup = InlineKeyboardMarkup()
  markup.add(
      InlineKeyboardButton(
          '📢 عضويت در کانال اول',
          url='https://t.me/cod_manii_yt?start=join',
      ),
      InlineKeyboardButton(
          '📢 عضويت در کانال دوم (اعتماد)',
          url='https://t.me/TRUST1_MANI?start=join',
      ),
  )
  markup.add(
      InlineKeyboardButton('🔄 بررسی عضویت', callback_data='check_join')
  )
  return markup


def main_menu(user_id):
  markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
  # گزینه خرید اکانت شخصی آمد اول تا کاملاً تو چشم باشد
  markup.add(
      KeyboardButton('🔸️خرید اکانت شخصی🔸️'),
      KeyboardButton('🎁اکانت مهندسی خفن🎁'),
      KeyboardButton('🎁اکانت by خام🎁'),
      KeyboardButton('🎁پست تمپلار🎁'),
      KeyboardButton('🎁 اکانت ۱۱ متیک رایگان🎁'),
      KeyboardButton('🎁 اکانت ۳۰ فول رایگان🎁'),
      KeyboardButton('🎁 اکانت ارتری رایگان🎁'),
      KeyboardButton('🔥اکانت 10 فول رایگان🔥'),
      KeyboardButton('💥اکانت 20 فول رایگان💥'),
      KeyboardButton('🎁 اکانت روزانه 🎁'),
      KeyboardButton('🎁 40 فول رایگان'),
      KeyboardButton('💥جایزه ویژه💥'),
      KeyboardButton('🎁اکانت خام 117🎁'),
      KeyboardButton('🎁 اکانت KRM 🎁'),
      KeyboardButton('🎁 پست سایرن رایگان'),
      KeyboardButton('🎁 پست گوست متیک رایگان🎁'),
      KeyboardButton('🎁پست اکانت مهندسی🎁'),
      KeyboardButton('🎁 اکانت ۸۰ میلیونی رایگان🎁'),
      KeyboardButton('🎁 ردیم کد کالاف'),
      KeyboardButton('📊 لینک دعوت (رفرال)'),
      KeyboardButton('🌐 DNS اختصاصی رایگان'),
      KeyboardButton('📢 کانال تلگرام'),
      KeyboardButton('📸 پیج اینستاگرام'),
      KeyboardButton('🔄 بروزرسانی منو'),
  )
  if user_id == ADMIN_ID:
    markup.add(KeyboardButton('📊 اطلاعات و آمار ربات (ادمین)'))
  return markup


@bot.message_handler(commands=['start'])
def start(message):
  user_id = str(message.from_user.id)
  numeric_user_id = message.from_user.id

  args = message.text.split()
  data = load_data()

  if user_id not in data:
    data[user_id] = {'invites': 0, 'last_daily': None}
    if len(args) > 1:
      inviter_id = args[1]
      if inviter_id != user_id and inviter_id in data:
        data[inviter_id]['invites'] += 1
        current_invites_inviter = data[inviter_id]['invites']
        try:
          bot.send_message(
              inviter_id,
              f'🎉 یک نفر با لینک دعوت شما وارد ربات شد!\n\n👥 تعداد کل دعوت‌های'
              f' شما: {current_invites_inviter} نفر',
          )
        except Exception:
          pass
    save_data(data)

  if not check_membership(numeric_user_id):
    bot.send_message(
        message.chat.id,
        '⚠️ برای استفاده از ربات، ابتدا باید در کانال‌های ما عضو شوید!\n\nپس از'
        ' عضویت در تمام کانال‌ها، روی دکمه‌ی «بررسی عضویت» بزنید:',
        reply_markup=not_joined_markup(),
    )
    return

  bot.send_message(
      message.chat.id,
      'سلام! منوی ربات بروز شد:',
      reply_markup=main_menu(numeric_user_id),
  )


@bot.callback_query_handler(func=lambda call: call.data == 'check_join')
def callback_check_join(call):
  user_id = call.from_user.id
  if check_membership(user_id):
    bot.answer_callback_query(
        call.id, '✅ تایید شد! حالا می‌‌تونید از ربات استفاده کنید.'
    )
    try:
      bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception:
      pass
    bot.send_message(
        call.message.chat.id,
        'سلام! به ربات خوش آمدید:',
        reply_markup=main_menu(user_id),
    )
  else:
    bot.answer_callback_query(
        call.id, '❌ شما هنوز در تمام کانال‌ها عضو نشده‌اید!', show_alert=True
    )


@bot.message_handler(func=lambda message: True)
def handle(message):
  user_id = str(message.from_user.id)
  numeric_user_id = message.from_user.id

  data = load_data()

  if user_id not in data:
    data[user_id] = {'invites': 0, 'last_daily': None}
    save_data(data)

  if not check_membership(numeric_user_id):
    bot.send_message(
        message.chat.id,
        '⚠️ برای استفاده از ربات، ابتدا باید در کانال‌های ما عضو شوید!',
        reply_markup=not_joined_markup(),
    )
    return

  current_invites = data[user_id].get('invites', 0)

  if message.text == '🔄 بروزرسانی منو':
    bot.send_message(
        message.chat.id,
        '✅ منوی شما با موفقیت بروزرسانی شد و آخرین تغییرات اعمال گردید:',
        reply_markup=main_menu(numeric_user_id),
    )

  elif message.text == '🔸️خرید اکانت شخصی🔸️':
    bot.send_message(
        message.chat.id,
        'اگر اکانت شخصی میخوایید فقط خودتون روش پلی بدین با هزینه مناسب فقط'
        ' کافیه تو پی وی بگین تو چه رنج قیمتی اکانت میخوایید.\n@Ssmmssllpp\n\nلطفا'
        ' قبل هرچیزی قوانین قبل خرید رو با حوصله چک مرور چک کنین📛👇\n'
        'https://t.me/TRUST1_MANI/31',
    )

  elif message.text == '🎁اکانت مهندسی خفن🎁':
    bot.send_message(
        message.chat.id,
        '🎁 اطلاعات اکانت مهندسی خفن:\n\ncatarinaloboo2@gmail.com\n253418873',
    )

  elif message.text == '🎁اکانت by خام🎁':
    bot.send_message(
        message.chat.id,
        '🎁 اطلاعات اکانت by خام:\n\nfallahail240@gmail.com\n29121356',
    )

  elif message.text == '🎁پست تمپلار🎁':
    bot.send_message(
        message.chat.id,
        '🎁 اطلاعات اکانت پست تمپلار شما:\n\ncarlos11cod@hotmail.com\ncarlos11cod',
    )

  elif message.text == '🎁 اکانت ۱۱ متیک رایگان🎁':
    if current_invites >= 40:
      bot.send_message(
          message.chat.id,
          'دوست عزیز قبل شما این اکانت به برندش تحویل داده شده دیر اقدام'
          ' کردی❤️ این شخص اکانت تحویل گرفته 𝗞𝗔𝗠𝗜 | 𝗡Ø𝗫',
      )
    else:
      remaining = 40 - current_invites
      ref_link = f'https://t.me/{(bot.get_me()).username}?start={user_id}'
      bot.send_message(
          message.chat.id,
          'عشقا این اکانت به ارزش ۱۵ میلیون قیمت داره بخاطر این رفرالش بالاس'
          ' ارزش داره ممنون که درک میکنین توجه کنین شما میتونین نه پولی هزینه'
          ' کنین نه کاری کنین فقط با رفرال گیری اکانت برنده بشین.\n\n⚠️ برای'
          ' دریافت اکانت ۱۱ متیک رایگان باید ۴۰ نفر را دعوت کنید!\n\n👥 تعداد'
          f' دعوت‌های فعلی شما: {current_invites} نفر\n❌ تعداد باقی‌مانده:'
          f' {remaining} نفر\n\n🔗 برای دریافت اکانت، لینک زیر را برای دوستان'
          f' خود بفرستید:\n{ref_link}',
      )

  elif message.text == '🎁 اکانت ۳۰ فول رایگان🎁':
    bot.send_message(
        message.chat.id,
        '❌ این اکانت به برنده اش تعلق گرفته برای دیدن تحویل اکانت هم این لینک'
        ' رو چک کنین رضایت تحویل 👇\nhttps://t.me/TRUST1_MANI/33\n\nاگر میخوای'
        ' برنده بعدی تو باشی بزن رو گزینه 🎁 اکانت ۱۱ متیک رایگان🎁',
    )

  elif message.text == '🎁 اکانت ارتری رایگان🎁':
    bot.send_message(
        message.chat.id,
        '❌ این اکانت به برنده اش تعلق گرفته برای دیدن تحویل اکانت هم این لینک'
        ' رو چک کنین رضایت تحویل 👇\nhttps://t.me/TRUST1_MANI/36\n\nاگر میخوای'
        ' برنده بعدی تو باشی بزن رو گزینه 🎁 اکانت 11 متیک رایگان🎁',
    )

  elif message.text == '🔥اکانت 10 فول رایگان🔥':
    bot.send_message(
        message.chat.id,
        '❌ این اکانت به برنده اش تعلق گرفته برای دیدن تحویل اکانت هم این لینک'
        ' رو چک کنین رضایت تحویل 👇\nhttps://t.me/TRUST1_MANI/30\n\nاگر میخوای'
        ' برنده بعدی تو باشی بزن رو گزینه 🎁 اکانت ۱۱ متیک رایگان🎁',
    )

  elif message.text == '🎁 اکانت روزانه 🎁':
    bot.send_message(message.chat.id, '❌ این گزینه فعلا خاموش شده است.')

  elif message.text == '🎁 40 فول رایگان':
    bot.send_message(
        message.chat.id,
        '❌ این اکانت به برنده اش تعلق گرفته برای دیدن تحویل اکانت هم این لینک'
        ' رو چک کنن چک رضایت تحویل رو چک کنن:\nhttps://t.me/TRUST1_MANI/28\n\nاگر'
        ' میخوای برنده بعدی تو باشی بزن رو گزینه 🎁 اکانت ۱۱ متیک رایگان🎁',
    )

  elif message.text == '💥اکانت 20 فول رایگان💥':
    bot.send_message(
        message.chat.id,
        '❌ این اکانت به برنده اش تعلق گرفته برای دیدن تحویل اکانت هم این لینک'
        ' رو چک کنین رضایت تحویل 👇\nhttps://t.me/TRUST1_MANI/29\n\nاگر میخوای'
        ' برنده بعدی تو باشی بزن رو گزینه 🎁 اکانت ۱۱ متیک رایگان🎁',
    )

  elif message.text == '💥جایزه ویژه💥':
    bot.send_message(
        message.chat.id,
        'برای شرکت در جایزه ویژه لطفا ۳ پست اخر اینستاگرام لایک سیو شیر کنین به'
        ' 10 نفر هم ارسال کنین اسکرین شات شو به این ایدی زیر ارسال کنین و جایزه'
        ' تون تحویل بگیرین❤️\n\n🆔 @Ssmmssllpp',
    )

  elif message.text == '🎁اکانت خام 117🎁':
    bot.send_message(
        message.chat.id,
        '🎁 اطلاعات اکانت خام 117 شما:\n\nparsa.parsa.92@gmail.com\nparsacallaf92',
    )

  elif message.text == '🎁 اکانت KRM 🎁':
    bot.send_message(
        message.chat.id,
        '🎁 اطلاعات اکانت KRM شما:\n\narashmehrabi138712@gmail.com\nmahdiznj1386\n\n⚠️'
        ' لطفاً پس از ورود اطلاعات را تغییر دهید.',
    )

  elif message.text == '🎁 پست سایرن رایگان':
    bot.send_message(
        message.chat.id,
        '🎁 اطلاعات اکانت پست سایرن رایگان شما:\n\n📧 ایمیل:'
        ' Giselhrndz@gmail.com\n🔑 پسورد: Liam180420\n\n⚠️ لطفاً پس از ورود'
        ' اطلاعات را تغییر دهید.',
    )

  elif message.text == '🎁 پست گوست متیک رایگان🎁':
    bot.send_message(
        message.chat.id,
        '🎁 اطلاعات اکانت پست گوست متیک رایگان شما:\n\n📧 ایمیل:'
        ' keyvan.hozouri@yahoo.com\n🔑 پسورد: Kh112288\n\n⚠️ لطفاً پس از ورود'
        ' اطلاعات را تغییر دهید.',
    )

  elif message.text == '🎁پست اکانت مهندسی🎁':
    bot.send_message(
        message.chat.id, 'arshiamalekshahi07@gmail.com\nmehdi2020'
    )

  elif message.text == '🎁 اکانت ۸۰ میلیونی رایگان🎁':
    bot.send_message(
        message.chat.id,
        '🎁 اطلاعات اکانت ۸۰ میلیونی رایگان شما:\n\n📧 ایمیل:'
        ' imamirnazari@gmail.com\n🔑 پسورد: meysam2020\n\n⚠️ لطفاً پس از ورود'
        ' اطلاعات را تغییر دهید.',
    )

  elif message.text == '🎁 ردیم کد کالاف':
    if current_invites >= 1:
      bot.send_message(
          message.chat.id,
          'DCEPZBZKFD\nDCCKZBZNB5\nDCCJZBZN4J\nDCCHZBZR3K\nDCCGZBZNCX\nDBGOZBZD8M\n'
          'DAVAZBZ9EP\nDAVCZBZA9M\nDAVBZBZX5A\nDBDKZBZQUU\nDBDJZBZAJU\nDAVGZBZRN6\n'
          'DBVPZBZNDX\nDBVHZBZUF3\nDBVNZBZBQW\nWELOVEMOM\nDCUPZBZ84M\nCTULZBZBXP\n'
          'CTJQZBZAFS\nCTJNZBZKJ8\nCUAMZBZFCF\n\n⚠️ نکته: اگر موقع زدن بعضی از'
          ' این کدها ارور داد، یعنی ظرفیت آن کد پر شده یا منقضی شده است؛ چون'
          ' کدهای اینستاگرام و بازی‌ها ظرفیت محدودی دارند. اول کدهای بالای لیست را'
          ' تست کنید.',
      )
    else:
      ref_link = f'https://t.me/{(bot.get_me()).username}?start={user_id}'
      bot.send_message(
          message.chat.id,
          f'⚠️ برای دریافت ردیم کدهای کالاف، باید حداقل ۱ نفر را دعوت کرده'
          f' باشید!\n\n👥 تعداد دعوت‌های فعلی شما: {current_invites} نفر\n❌'
          f' تعداد باقی‌مانده: ۱ نفر\n\n🔗 لینک دعوت اختصاصی شما:\n{ref_link}',
      )

  elif message.text == '📊 لینک دعوت (رفرال)':
    ref_link = f'https://t.me/{(bot.get_me()).username}?start={user_id}'
    bot.send_message(
        message.chat.id,
        f'📊 وضعیت دعوت‌های شما: {current_invites} نفر\n\n🔗 لینک اختصاصی'
        f' شما:\n{ref_link}',
    )

  elif message.text == '🌐 DNS اختصاصی رایگان':
    bot.send_message(
        message.chat.id,
        '🌐 DNS اختصاصی و پرسرعت رایگان:\n\nPrimary DNS: 77.88.8.8\nSecondary'
        ' DNS: 88.198.220.33',
    )

  elif message.text == '📢 کانال تلگرام':
    bot.send_message(
        message.chat.id,
        '📢 کانال‌های ما:\n1️⃣ https://t.me/cod_manii_yt\n2️⃣'
        ' https://t.me/TRUST1_MANI',
    )

  elif message.text == '📸 پیج اینستاگرام':
    bot.send_message(
        message.chat.id,
        '📸 پیج اینستاگرام'
        ' ما:\nhttps://www.instagram.com/maniiii.yt?igsh=ZWp6ZHdhMjloY2Jh',
    )

  elif message.text == '📊 اطلاعات و آمار ربات (ادمین)':
    if numeric_user_id == ADMIN_ID:
      total_users = len(data)
      bot.send_message(
          message.chat.id,
          f'📊 آمار ربات:\n\n👥 کل کاربرانی که ربات را استارت کرده‌اند:'
          f' {total_users} نفر',
      )
    else:
      bot.send_message(message.chat.id, '❌ شما به این بخش دسترسی ندارید.')


print('Bot is running perfectly...')
bot.remove_webhook()
bot.infinity_polling()
