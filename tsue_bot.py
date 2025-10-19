import asyncio
import json
import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "BOT_TOKEN"
ADMIN_URL = "https://t.me/J0shqin"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")

DATA_FILE = "data.json"

# ----------------------------
# Guruhlar ro'yxati (to'liq)
# ----------------------------
groups = {
    "1-kurs": {
        "I-85/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*169",
        "I-86/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*170",
        "I-87/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*171",
        "I-88/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*172",
        "I-89/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*173",
        "I-80k/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*174",
        "I-81k/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*175",
        "I-82k/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*176",
        "I-83k/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*177",
        "I-84k/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*178",
        "I-85k/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*179",
        "I-86/25i": "https://tsue.edupage.org/timetable/view.php?num=89&class=*180",
        "I-87/25i": "https://tsue.edupage.org/timetable/view.php?num=89&class=*181",
        "I-30/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*182",
        "I-31/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*183",
        "I-32/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*184",
        "I-33/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*185",
        "I-34/25i": "https://tsue.edupage.org/timetable/view.php?num=89&class=*186",
        "IRB-86/25i": "https://tsue.edupage.org/timetable/view.php?num=89&class=*187",
        "IRB-80/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*188",
        "IRB-81/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*189",
        "IRB-82/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*190",
        "IRB-83/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*191",
        "IRB-84/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*192",
        "IRB-85/25": "https://tsue.edupage.org/timetable/view.php?num=89&class=*193"
    },
    "2-kurs": {
        "I-51/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*207",
        "I-52/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*208",
        "I-53/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*209",
        "I-54/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*210",
        "I-55/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*211",
        "I-56/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*212",
        "I-57/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*213",
        "I-58/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*214",
        "I-59/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*215",
        "I-50k/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*216",
        "I-51k/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*217",
        "I-52k/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*218",
        "I-53k/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*219",
        "IRB-50/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*220",
        "IRB-51/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*221",
        "IRB-52/24": "https://tsue.edupage.org/timetable/view.php?num=89&class=*222",
        "IRB-53/24i": "https://tsue.edupage.org/timetable/view.php?num=89&class=*223",
        "I-05/24i": "https://tsue.edupage.org/timetable/view.php?num=89&class=*224",
        "I-54/24i": "https://tsue.edupage.org/timetable/view.php?num=89&class=*225",
        "I-55/24i": "https://tsue.edupage.org/timetable/view.php?num=89&class=*226"
    }
}

# ----------------------------
# JSON saqlash funksiyalari
# ----------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_user(chat_id, kurs=None, group=None, time=None):
    data = load_data()
    data[str(chat_id)] = {"kurs": kurs, "group": group, "time": time}
    save_data(data)

def remove_user_reminder(chat_id):
    data = load_data()
    if str(chat_id) in data:
        data[str(chat_id)]["time"] = None
        data[str(chat_id)]["group"] = None
        save_data(data)

# ----------------------------
# Start menyu
# ----------------------------
@dp.message(CommandStart())
async def start(message: types.Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🏫 Iqtisodiyot fakulteti")],
            [KeyboardButton(text="💬 Takliflar"), KeyboardButton(text="➕ Guruhga qo‘shish")],
            [KeyboardButton(text="⏰ Eslatma sozlash")]
        ],
        resize_keyboard=True
    )
    await message.answer("👋 Salom! TSUE jadval botiga xush kelibsiz!", reply_markup=kb)

# ----------------------------
# Takliflar
# ----------------------------
@dp.message(F.text == "💬 Takliflar")
async def takliflar(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="Adminga yozish", url=ADMIN_URL)
    kb.adjust(1)
    await message.answer("👇 Tugmani bosing:", reply_markup=kb.as_markup())

# ----------------------------
# Guruhga qo‘shish
# ----------------------------
@dp.message(F.text == "➕ Guruhga qo‘shish")
async def guruhga_qoshish(message: types.Message):
    bot_info = await bot.get_me()
    url = f"https://t.me/{bot_info.username}?startgroup=true"
    kb = InlineKeyboardBuilder()
    kb.button(text="Guruhga qo‘shish", url=url)
    kb.adjust(1)
    await message.answer("👇 Tugmani bosing:", reply_markup=kb.as_markup())

# ----------------------------
# Iqtisodiyot fakulteti
# ----------------------------
@dp.message(F.text == "🏫 Iqtisodiyot fakulteti")
async def fak(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="1️⃣ 1-kurs", callback_data="kurs_1")
    kb.button(text="2️⃣ 2-kurs", callback_data="kurs_2")
    kb.adjust(2)
    await message.answer("Kursni tanlang:", reply_markup=kb.as_markup())

# ----------------------------
# Eslatma menyusi
# ----------------------------
@dp.message(F.text == "⏰ Eslatma sozlash")
async def eslatma(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="1️⃣ 1-kurs", callback_data="remind_kurs_1")
    kb.button(text="2️⃣ 2-kurs", callback_data="remind_kurs_2")
    kb.button(text="❌ Eski eslatmalarni o'chirish", callback_data="clear_reminder")
    kb.adjust(2)
    await message.answer("Qaysi kurs uchun eslatma o‘rnatmoqchisiz?", reply_markup=kb.as_markup())
# ----------------------------
# Kurs → Guruh (asosiy menyu)
# ----------------------------
@dp.callback_query(F.data.startswith("kurs_"))
async def kurs_tanlandi(callback: types.CallbackQuery):
    kurs = "1-kurs" if callback.data.endswith("_1") else "2-kurs"
    add_user(callback.message.chat.id, kurs=kurs)
    
    # Inline tugmalar bilan guruhlar ro'yxati
    kb = InlineKeyboardBuilder()
    for nom in groups[kurs]:
        kb.button(text=nom, callback_data=f"group_{nom}")
    kb.adjust(2)
    
    await callback.message.answer(f"{kurs} guruhini tanlang:", reply_markup=kb.as_markup())
# ----------------------------
# Guruh tanlandi (asosiy menyu)
# ----------------------------
@dp.callback_query(F.data.startswith("group_"))
async def group_tanlandi(callback: types.CallbackQuery):
    group = callback.data.replace("group_", "")
    chat_id = callback.message.chat.id
    data = load_data().get(str(chat_id), {})
    kurs = data.get("kurs")
    add_user(chat_id, kurs, group)
    
    link = groups[kurs][group]
    await callback.message.answer(f"📅 {group} uchun bugungi jadval:\n👉 {link}")

# ----------------------------
# Callback handler eslatma o‘chirish
# ----------------------------
@dp.callback_query(F.data == "clear_reminder")
async def clear_reminder(callback: types.CallbackQuery):
    chat_id = callback.message.chat.id
    remove_user_reminder(chat_id)
    for job in scheduler.get_jobs():
        if job.args[0] == chat_id:
            job.remove()
    await callback.message.answer("✅ Sizning eski eslatmalaringiz o‘chirildi.")

# ----------------------------
# Kurs → Guruh (eslatma)
# ----------------------------
@dp.callback_query(F.data.startswith("remind_kurs_"))
async def remind_kurs(callback: types.CallbackQuery):
    kurs = "1-kurs" if callback.data.endswith("_1") else "2-kurs"
    add_user(callback.message.chat.id, kurs=kurs)
    kb = InlineKeyboardBuilder()
    for nom in groups[kurs]:
        kb.button(text=nom, callback_data=f"remind_group_{nom}")
    kb.adjust(2)
    await callback.message.answer(f"{kurs} guruhini tanlang:", reply_markup=kb.as_markup())

# ----------------------------
# Guruh tanlandi (eslatma)
# ----------------------------
@dp.callback_query(F.data.startswith("remind_group_"))
async def remind_group(callback: types.CallbackQuery):
    group = callback.data.replace("remind_group_", "")
    chat_id = callback.message.chat.id
    data = load_data().get(str(chat_id), {})
    kurs = data.get("kurs")
    add_user(chat_id, kurs, group)
    await callback.message.answer("⏰ Eslatma soatini kiriting (masalan: 07:15):")

# ----------------------------
# Soat kiritish (eslatma)
# ----------------------------
@dp.message(F.text.regexp(r"^\d{2}:\d{2}$"))
async def soat_kiritildi(message: types.Message):
    time_str = message.text
    try:
        hour, minute = map(int, time_str.split(":"))
        if 0 <= hour < 24 and 0 <= minute < 60:
            chat_id = message.chat.id
            data = load_data().get(str(chat_id), {})
            kurs = data.get("kurs")
            group = data.get("group")
            add_user(chat_id, kurs, group, time_str)
            scheduler.add_job(send_one, "cron", hour=hour, minute=minute, args=[chat_id])
            await message.answer(f"✅ {group} uchun eslatma har kuni {time_str} da yuboriladi.")
        else:
            await message.answer("❌ Noto‘g‘ri vaqt. Masalan: 07:15")
    except:
        await message.answer("❌ Noto‘g‘ri format. Masalan: 07:15")

# ----------------------------
# Avtomatik yuborish
# ----------------------------
async def send_one(chat_id):
    data = load_data().get(str(chat_id), {})
    kurs = data.get("kurs")
    group = data.get("group")
    if kurs and group:
        link = groups[kurs][group]
        await bot.send_message(chat_id, f"📅 {group} uchun bugungi jadval:\n👉 {link}")

# ----------------------------
# Ishga tushirish
# ----------------------------
async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
