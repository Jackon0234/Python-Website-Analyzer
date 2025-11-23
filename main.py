import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.analyzer import WebAnalyzer
from core.report_builder import ReportBuilder
from config import settings

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

analyzer = WebAnalyzer()
reporter = ReportBuilder()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "🕵️‍♂️ <b>Web X-RAY Bot</b>\n\n"
        "Analiz etmek istediğiniz site adresini gönderin.\n"
        "<i>Örnek: r10.net</i>"
    )

@dp.message(F.text)
async def handle_analysis(message: types.Message):
    url = message.text.strip()
    
    status_msg = await message.answer("🔍 <b>Hedef site taranıyor...</b>")
    await bot.send_chat_action(message.chat.id, action="typing")

    try:
        result = await asyncio.to_thread(analyzer.analyze, url)
        report_text = reporter.build_telegram_report(result)
        
        builder = InlineKeyboardBuilder()
        if "http" not in url: url = "https://" + url
        builder.button(text="🔗 Siteye Git", url=url)
        
        await status_msg.edit_text(report_text, reply_markup=builder.as_markup())
        
    except Exception as e:
        await status_msg.edit_text(f"⚠️ <b>Hata:</b> {str(e)}")

async def main():
    print("Bot başlatıldı...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot kapatıldı.")