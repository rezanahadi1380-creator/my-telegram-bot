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
ADMIN_ID = 6903327854  # آیدی عددی شما برای دسترسی به آمار
bot = telebot.TeleBot(TOKEN)

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
def check_membership(user_id):
  for channel in CHANNELS:
    try:
      member = bot.get_chat_member(channel, user_id)
      if member.status not in ['member', 'administrator', 'creator']:
        return False
    except Exception:
      return False
  return True


# دکمه‌های عضویت در کانال‌ها (شیشه‌ای)
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
  markup.add(
      KeyboardButton('🔸️خرید اکانت شخصی🔸️'),
      KeyboardButton('🎁پست تمپلار🎁'),
      KeyboardButton('🎁 اکانت ۱۱ متیک رایگان🎁'),
      KeyboardButton('🎁 اکانت ۳۰ فول رایگان🎁'),
      KeyboardButton('🎁 اکانت ارتری رایگان🎁'),
      KeyboardButton('🔥اکانت 10 فول رایگان🔥
