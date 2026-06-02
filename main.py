import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

# إعداد البوت
TOKEN = '8896317088:AAGmpySKGgws_FZ0ftxeimj80B-ijcugX_0'
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# --- القوائم الرئيسية ---
def get_main_menu():
    kb = [
        [KeyboardButton(text="👤 حسابي"), KeyboardButton(text="💳 تجديد الاشتراك")],
        [KeyboardButton(text="📈 الاستهلاك"), KeyboardButton(text="⚙️ الإعدادات")],
        [KeyboardButton(text="🎧 الدعم الفني")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# --- الأوامر الأساسية ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "مرحباً بك في أمازون ليبيا للاتصالات والتقنية.\n"
        "الرجاء اختيار الخدمة المطلوبة من القائمة أدناه:",
        reply_markup=get_main_menu()
    )

# --- معالجة الأزرار ---
@dp.message(F.text == "👤 حسابي")
async def show_account(message: Message):
    # هنا سيتم لاحقاً جلب البيانات من قاعدة البيانات باستخدام رقم العقد
    await message.answer("🔍 **جاري استعلام بيانات العقد من السيرفر...**\n\nالاسم: [اسم المشترك]\nحالة الخدمة: فعال ✅")

@dp.message(F.text == "💳 تجديد الاشتراك")
async def renew_subscription(message: Message):
    await message.answer("يرجى إدخال رقم كرت الشحن لتجديد اشتراكك:")

@dp.message(F.text == "🎧 الدعم الفني")
async def support_center(message: Message):
    await message.answer("نحن هنا للمساعدة! تواصل مع فريقنا مباشرة عبر:\n📞 الهاتف: 021-XXXXXXX\n🌐 الموقع: www.amazon.ly")

# --- تشغيل البوت ---
async def main():
    print("البوت يعمل الآن...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
