import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

# إعداد البوت
TOKEN = '8896317088:AAGmpySKGgws_FZ0ftxeimj80B-ijcugX_0'
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# قاعدة بيانات وهمية
users_db = {"1001": {"name": "أحمد الليبي", "expiry": "2026-07-01", "balance": 50}}

# الحالات
class AppStates(StatesGroup):
    waiting_for_contract = State()
    waiting_for_duration = State()
    waiting_for_card = State()

# القوائم
main_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="👤 حسابي"), KeyboardButton(text="💳 تجديد الاشتراك")]
], resize_keyboard=True)

# 1. البدء
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("أهلاً بك في أمازون ليبيا. يرجى إدخال رقم العقد:", reply_markup=main_kb)

# 2. الاستعلام عن الحساب
@dp.message(F.text == "👤 حسابي")
async def show_account(message: Message, state: FSMContext):
    await message.answer("أدخل رقم العقد الخاص بك:")
    await state.set_state(AppStates.waiting_for_contract)

@dp.message(AppStates.waiting_for_contract)
async def process_contract(message: Message, state: FSMContext):
    contract = message.text
    if contract in users_db:
        user = users_db[contract]
        await message.answer(f"✅ بياناتك:\nالاسم: {user['name']}\nانتهاء: {user['expiry']}\nرصيدك: {user['balance']} د.ل")
        await state.update_data(contract=contract)
    else:
        await message.answer("❌ رقم العقد غير موجود.")
    await state.clear()

# 3. التجديد
@dp.message(F.text == "💳 تجديد الاشتراك")
async def ask_duration(message: Message, state: FSMContext):
    await message.answer("اختر مدة التجديد (شهر / 3 أشهر / سنة):")
    await state.set_state(AppStates.waiting_for_duration)

@dp.message(AppStates.waiting_for_duration)
async def process_duration(message: Message, state: FSMContext):
    duration = message.text
    # حساب السعر الوهمي
    price = 50 if "شهر" in duration else 150
    await state.update_data(duration=duration, price=price)
    await message.answer(f"المبلغ المطلوب: {price} د.ل. \nالآن، يرجى إدخال رقم كرت الشحن:")
    await state.set_state(AppStates.waiting_for_card)

@dp.message(AppStates.waiting_for_card)
async def process_card(message: Message, state: FSMContext):
    card = message.text
    if len(card) > 5: # محاكاة للتحقق من الكرت
        data = await state.get_data()
        await message.answer(f"🎉 تم تجديد الاشتراك بنجاح!\nالمدة: {data['duration']}\nتم خصم: {data['price']} د.ل")
    else:
        await message.answer("❌ رقم الكرت غير صحيح.")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
