import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

MODEL_SERVER_URL = os.getenv("MODEL_SERVER_URL", "http://model-server:8001/predict")

CONTEXT = (
    "MLOps is a set of practices that aims to deploy and maintain machine learning models "
    "in production reliably and efficiently. It combines Machine Learning, DevOps, and "
    "Data Engineering to automate and monitor the ML lifecycle."
)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Задай мне вопрос, и я постараюсь ответить на него на основе знаний о MLOps."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = update.message.text
    payload = {"question": question, "context": CONTEXT}
    try:
        response = requests.post(MODEL_SERVER_URL, json=payload, timeout=5)
        result = response.json()
        answer = result.get("answer", "No answer")
        score = result.get("score", 0)
        await update.message.reply_text(f"Answer: {answer}\nScore: {score:.3f}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
