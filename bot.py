from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
)
from aiogram.fsm.storage.memory import MemoryStorage
import json
import os

TOKEN = '8873507987:AAE04VR6t0upXTWi1_7mEFeRLFEUfgnp7pU'
ADMIN_ID = 6903327854  # آیدی عددی شما برای دسترسی به آمار

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

DATA_FILE = 'users.json'
CHANNELS = [
    '@cod_manii_yt',
    '@TRUST1_MANI',
]  # کانال‌های جوین اجباری (کانال اصلی و کانال اعتماد)


def load_data():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'r') as f:
      return json.load(f)
  return {}


def save_data(data):
  with open(DATA_FILE, 'w') as f:
    json.dump(data, f)


# تابع بررسی عضویت کاربر در کانال‌ها
async def check_membership(user_id: int) -> bool:
  try:
    for channel in CHANNELS:
      member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
      if member.status not in ['member', 'administrator', 'creator']:
        return False
    return True
  except Exception:
    return False


# دکمه‌های عضویت در کانال‌ها (شیشه‌ای)
def not_joined_markup():
  return InlineKeyboardMarkup(inline_keyboard=[
      [
          InlineKeyboardButton(
              text='📢 عضويت در کانال اول',
              url='https://t.me/cod_manii_yt?start=join',
          )
      ],
      [
          InlineKeyboardButton(
              text='📢 عضويت در کانال دوم (اعتماد)',
              url='https://t.me/TRUST1_MANI?start=join',
          )
      ],
      [
          InlineKeyboardButton(
              text='🔄 بررسی عضویت', callback_data='check_join'
          )
      ],
  ])


def main_menu(user_id: int):
  # تعریف دکمه خرید اکانت شخصی با استایل قرمز (destructive) در aiogram
  red_buy_button = KeyboardButton(
      text='🔸️خرید اکانت شخصی🔸️', style='destructive'
  )

  kb = [
      [red_buy_button, KeyboardButton(text='🎁پست تمپلار🎁')],
      [
          KeyboardButton(text='🎁 اکانت ۱۱ متیک رایگان🎁'),
          KeyboardButton(text='🎁 اکانت ۳۰ فول رایگان🎁'),
      ],
      [
          KeyboardButton(text='🎁 اکانت ارتری رایگان🎁'),
          KeyboardButton(text='🔥اکانت 10 فول رایگان🔥'),
      ],
      [
          KeyboardButton(text='💥اکانت 20 فول رایگان💥'),
          KeyboardButton(text='🎁 اکانت روزانه 🎁'),
      ],
      [
          KeyboardButton(text='🎁 40 فول رایگان'),
          KeyboardButton(text='💥جایزه ویژه💥'),
      ],
      [
          KeyboardButton(text='🎁اکانت خام 117🎁'),
          KeyboardButton(text='🎁 اکانت KRM 🎁'),
      ],
      [
          KeyboardButton(text='🎁 پست سایرن رایگان'),
          KeyboardButton(text='🎁 پست گوست متیک رایگان🎁'),
      ],
      [
          KeyboardButton(text='🎁پست اکانت مهندسی🎁'),
          KeyboardButton(text='🎁 اکانت ۸۰ میلیونی رایگان🎁'),
      ],
      [
          KeyboardButton(text='🎁 ردیم کد کالاف'),
          KeyboardButton(text='📊 لینک دعوت (رفرال)'),
      ],
      [
          KeyboardButton(text='🌐 DNS اختصاصی رایگان'),
          KeyboardButton(text='📢 کانال تلگرام'),
      ],
      [
          KeyboardButton(text='📸 پیج اینستاگرام'),
          KeyboardButton(text='🔄 بروزرسانی منو'),
      ],
  ]

  if user_id == ADMIN_ID:
    kb.append([KeyboardButton(text='📊 اطلاعات و آمار ربات (ادمین)')])

  return ReplyKeyboardMarkup(
      keyboard=kb,
      resize_keyboard=True,
      input_field_placeholder='یک گزینه انتخاب کنید...',
  )


@router.message(Command('start'))
async def start(message: Message):
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
          await bot.send_message(
              chat_id=int(inviter_id),
              text=f'🎉 یک نفر با لینک دعوت شما وارد ربات شد!\n\n👥 تعداد کل دعوت‌های'
              f' شما: {current_invites_inviter} نفر',
          )
        except Exception:
          pass
    save_data(data)

  if not await check_membership(numeric_user_id):
    await message.answer(
        '⚠️ برای استفاده از ربات، ابتدا باید در کانال‌های ما عضو شوید!\n\nپس از'
        ' عضویت در تمام کانال‌ها، روی دکمه‌ی «بررسی عضویت» بزنید:',
        reply_markup=not_joined_markup(),
    )
    return

  await message.answer(
      'سلام! منوی ربات بروز شد:', reply_markup=main_menu(numeric_user_id)
  )


@router.callback_query(lambda c: c.data == 'check_join')
async def callback_check_join(callback_query):
  user_id = callback_query.from_user.id
  if await check_membership(user_id):
    await callback_query.answer(
        '✅ تایید شد! حالا می‌‌تونید از ربات استفاده کنید.'
    )
    try:
      await bot.delete_message(
          chat_id=callback_query.message.chat.id,
          message_id=callback_query.message.message_id,
      )
    except Exception:
      pass
    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text='سلام! به ربات خوش آمدید:',
        reply_markup=main_menu(user_id),
    )
  else:
    await callback_query.answer(
        '❌ شما هنوز در تمام کانال‌ها عضو نشده‌اید!', show_alert=True
    )


@router.message()
async def handle(message: Message):
  user_id = str(message.from_user.id)
  numeric_user_id = message.from_user.id

  data = load_data()

  if user_id not in data:
    data[user_id] = {'invites': 0, 'last_daily': None}
    save_data(data)

  if not await check_membership(numeric_user_id):
    await message.answer(
        '⚠️ برای استفاده از ربات، ابتدا باید در کانال‌های ما عضو شوید!',
        reply_markup=not_joined_markup(),
    )
    return

  current_invites = data[user_id].get('invites', 0)
  text = message.text

  if text == '🔄 بروزرسانی منو':
    await message.answer(
        '✅ منوی شما با موفقیت بروزرسانی شد و آخرین تغییرات اعمال گردید:',
        reply_markup=main_menu(numeric_user_id),
    )

  elif text == '🔸️خرید اکانت شخصی🔸️':
    personal_buy_msg = (
        'اگر اکانت شخصی میخوایید فقط خودتون روش پلی بدین با هزینه مناسب فقط کافیه'
        ' تو پی وی بگین تو چه رنج قیمتی اکانت میخوایید.\n@Ssmmssllpp\n\nلطفا قبل'
        ' هرچیزی قوانین قبل خرید رو با حوصله چک مرور چک کنین📛👇\n'
        'https://t.me/TRUST1_MANI/31'
    )
    await message.answer(personal_buy_msg)

  elif text == '🎁پست تمپلار🎁':
    templar_msg = (
        '🎁 اطلاعات اکانت پست تمپلار شما:\n\ncarlos11cod@hotmail.com\ncarlos11cod'
    )
    await message.answer(templar_msg)

  elif text == '🎁 اکانت ۱۱ متیک رایگان🎁':
    if current_invites >= 40:
      mythic_11_delivered_msg = (
          'دوست عزیز قبل شما این اکانت به برندش تحویل داده شده دیر اقدام کردی❤️'
          ' این شخص اکانت تحویل گرفته 𝗞𝗔𝗠𝗜 | 𝗡Ø𝗫'
      )
      await message.answer(mythic_11_delivered_msg)
    else:
      remaining = 40 - current_invites
      bot_info = await bot.get_me()
      ref_link = f'https://t.me/{bot_info.username}?start={user_id}'
      mythic_11_ref_msg = (
          'عشقا این اکانت به ارزش ۱۵ میلیون قیمت داره بخاطر این رفرالش بالاس'
          ' ارزش داره ممنون که درک میکنین توجه کنین شما میتونین نه پولی هزینه'
          ' کنین نه کاری کنین فقط با رفرال گیری اکانت برنده بشین.\n\n⚠️ برای'
          ' دریافت اکانت ۱۱ متیک رایگان باید ۴۰ نفر را دعوت کنید!\n\n👥 تعداد'
          f' دعوت‌های فعلی شما: {current_invites} نفر\n❌ تعداد باقی‌مانده:'
          f' {remaining} نفر\n\n🔗 برای دریافت اکانت، لینک زیر را برای دوستان'
          f' خود بفرستید:\n{ref_link}'
      )
      await message.answer(mythic_11_ref_msg)

  elif text == '🎁 اکانت ۳۰ فول رایگان🎁':
    prize_30_msg = (
        '❌ این اکانت به برنده اش تعلق گرفته برای دیدن تحویل اکانت هم این لینک'
        ' رو چک کنین رضایت تحویل 👇\nhttps://t.me/TRUST1_MANI/33\n\nاگر میخوای'
        ' برنده بعدی تو باشی بزن رو گزینه 🎁 اکانت ۱۱ متیک رایگان🎁'
    )
    await message.answer(prize_30_msg)

  elif text == '🎁 اکانت ارتری رایگان🎁':
    artery_delivered_msg = (
        '❌ این اکانت به برنده اش تعلق گرفته برای دیدن تحویل اکانت هم این لینک'
        ' رو چک کنین رضایت تحویل 👇\nhttps://t.me/TRUST1_MANI/36\n\nاگر میخوای'
        ' برنده بعدی تو باشی بزن رو گزینه 🎁 اکانت 11 متیک رایگان🎁'
    )
    await message.answer(artery_delivered_msg)

  elif text == '🔥اکانت 10 فول رایگان🔥':
    msg_10 = (
        '❌ این اکانت به برنده اش تعلق گرفته برای دیدن تحویل اکانت هم این لینک'
        ' رو چک کنین رضایت تحویل 👇\nhttps://t.me/TRUST1_MANI/30\n\nاگر میخوای'
        ' برنده بعدی تو باشی بزن رو گزینه 🎁 اکانت ۱۱ متیک رایگان🎁'
    )
    await message.answer(msg_10)

  elif text == '🎁 اکانت روزانه 🎁':
    await message.answer('❌ این گزینه فعلا خاموش شده است.')

  elif text == '🎁 40 فول رایگان':
    msg_40 = (
        '❌ این اکانت به برنده اش تعلق گرفته برای دیدن تحویل اکانت هم این لینک'
        ' رو چک کنن چک رضایت تحویل رو چک کنن:\nhttps://t.me/TRUST1_MANI/28\n\nاگر'
        ' میخوای برنده بعدی تو باشی بزن رو گزینه 🎁 اکانت ۱۱ متیک رایگان🎁'
    )
    await message.answer(msg_40)

  elif text == '💥اکانت 20 فول رایگان💥':
    msg_20 = (
        '❌ این اکانت به برنده اش تعلق گرفته برای دیدن تحویل اکانت هم این لینک'
        ' رو چک کنین رضایت تحویل 👇\nhttps://t.me/TRUST1_MANI/29\n\nاگر میخوای'
        ' برنده بعدی تو باشی بزن رو گزینه 🎁 اکانت ۱۱ متیک رایگان🎁'
    )
    await message.answer(msg_20)

  elif text == '💥جایزه ویژه💥':
    special_prize_msg = (
        'برای شرکت در جایزه ویژه لطفا ۳ پست اخر اینستاگرام لایک سیو شیر کنین به'
        ' 10 نفر هم ارسال کنین اسکرین شات شو به این ایدی زیر ارسال کنین و جایزه'
        ' تون تحویل بگیرین❤️\n\n🆔 @Ssmmssllpp'
    )
    await message.answer(special_prize_msg)

  elif text == '🎁اکانت خام 117🎁':
    post_117_msg = (
        '🎁 اطلاعات اکانت خام 117 شما:\n\nparsa.parsa.92@gmail.com\nparsacallaf92'
    )
    await message.answer(post_117_msg)

  elif text == '🎁 اکانت KRM 🎁':
    krm_msg = (
        '🎁 اطلاعات اکانت KRM شما:\n\narashmehrabi138712@gmail.com\nmahdiznj1386\n\n⚠️'
        ' لطفاً پس از ورود اطلاعات را تغییر دهید.'
    )
    await message.answer(krm_msg)

  elif text == '🎁 پست سایرن رایگان':
    siren_msg = (
        '🎁 اطلاعات اکانت پست سایرن رایگان شما:\n\n📧 ایمیل:'
        ' Giselhrndz@gmail.com\n🔑 پسورد: Liam180420\n\n⚠️ لطفاً پس از ورود'
        ' اطلاعات را تغییر دهید.'
    )
    await message.answer(siren_msg)

  elif text == '🎁 پست گوست متیک رایگان🎁':
    ghost_msg = (
        '🎁 اطلاعات اکانت پست گوست متیک رایگان شما:\n\n📧 ایمیل:'
        ' keyvan.hozouri@yahoo.com\n🔑 پسورد: Kh112288\n\n⚠️ لطفاً پس از ورود'
        ' اطلاعات را تغییر دهید.'
    )
    await message.answer(ghost_msg)

  elif text == '🎁پست اکانت مهندسی🎁':
    engineering_acc_msg = 'arshiamalekshahi07@gmail.com\nmehdi2020'
    await message.answer(engineering_acc_msg)

  elif text == '🎁 اکانت ۸۰ میلیونی رایگان🎁':
    account_85m_msg = (
        '🎁 اطلاعات اکانت ۸۰ میلیونی رایگان شما:\n\n📧 ایمیل:'
        ' imamirnazari@gmail.com\n🔑 پسورد: meysam2020\n\n⚠️ لطفاً پس از ورود'
        ' اطلاعات را تغییر دهید.'
    )
    await message.answer(account_85m_msg)

  elif text == '🎁 ردیم کد کالاف':
    if current_invites >= 1:
      codes = (
          'DCEPZBZKFD\nDCCKZBZNB5\nDCCJZBZN4J\nDCCHZBZR3K\nDCCGZBZNCX\nDBGOZBZD8M\n'
          'DAVAZBZ9EP\nDAVCZBZA9M\nDAVBZBZX5A\nDBDKZBZQUU\nDBDJZBZAJU\nDAVGZBZRN6\n'
          'DBVPZBZNDX\nDBVHZBZUF3\nDBVNZBZBQW\nWELOVEMOM\nDCUPZBZ84M\nCTULZBZBXP\n'
          'CTJQZBZAFS\nCTJNZBZKJ8\nCUAMZBZFCF\n\n⚠️ نکته: اگر موقع زدن بعضی از'
          ' این کدها ارور داد، یعنی ظرفیت آن کد پر شده یا منقضی شده است؛ چون'
          ' کدهای اینستاگرام و بازی‌ها ظرفیت محدودی دارند. اول کدهای بالای لیست را'
          ' تست کنید.'
      )
      await message.answer(codes)
    else:
      bot_info = await bot.get_me()
      ref_link = f'https://t.me/{bot_info.username}?start={user_id}'
      ref_msg = (
          f'⚠️ برای دریافت ردیم کدهای کالاف، باید حداقل ۱ نفر را دعوت کرده'
          f' باشید!\n\n👥 تعداد دعوت‌های فعلی شما: {current_invites} نفر\n❌'
          f' تعداد باقی‌مانده: ۱ نفر\n\n🔗 لینک دعوت اختصاصی شما:\n{ref_link}'
      )
      await message.answer(ref_msg)

  elif text == '📊 لینک دعوت (رفرال)':
    bot_info = await bot.get_me()
    ref_link = f'https://t.me/{bot_info.username}?start={user_id}'
    await message.answer(
        f'📊 وضعیت دعوت‌های شما: {current_invites} نفر\n\n🔗 لینک اختصاصی'
        f' شما:\n{ref_link}'
    )

  elif text == '🌐 DNS اختصاصی رایگان':
    dns_msg = (
        '🌐 DNS اختصاصی و پرسرعت رایگان:\n\nPrimary DNS: 77.88.8.8\nSecondary'
        ' DNS: 88.198.220.33'
    )
    await message.answer(dns_msg)

  elif text == '📢 کانال تلگرام':
    await message.answer(
        '📢 کانال‌های ما:\n1️⃣ https://t.me/cod_manii_yt\n2️⃣'
        ' https://t.me/TRUST1_MANI'
    )

  elif text == '📸 پیج اینستاگرام':
    await message.answer(
        '📸 پیج اینستاگرام'
        ' ما:\nhttps://www.instagram.com/maniiii.yt?igsh=ZWp6ZHdhMjloY2Jh'
    )

  elif text == '📊 اطلاعات و آمار ربات (ادمین)':
    if numeric_user_id == ADMIN_ID:
      total_users = len(data)
      await message.answer(
          f'📊 آمار ربات:\n\n👥 کل کاربرانی که ربات را استارت کرده‌اند:'
          f' {total_users} نفر'
      )
    else:
      await message.answer('❌ شما به این بخش دسترسی ندارید.')


async def main():
  dp.include_router(router)
  await bot.delete_webhook(drop_pending_updates=True)
  print('Bot is running with Aiogram and styled buttons...')
  await dp.start_polling(bot)


if __name__ == '__main__':
  import asyncio

  asyncio.run(main())
