from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import logging, random
from database import init_db, salvar_pagamento
from efi import criar_pix
from datetime import datetime
import PLANOS  # Importar seus planos

TOKEN = "8578511352:AAFxiP2PwlZySHpXbYbv_JNZrsXs6mwMjro"
init_db()

logging.basicConfig(level=logging.INFO)
logging.info("Bot rodando")

def codigo():
    return ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=12))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [[InlineKeyboardButton("⭐ Seja VIP", callback_data="vip")]]
    await update.message.reply_text("Bem-vindo! Clique abaixo:", reply_markup=InlineKeyboardMarkup(teclado))

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    teclado = [[InlineKeyboardButton(p, callback_data=f"buy_{p}")] for p in PLANOS]
    await update.callback_query.edit_message_text("Escolha seu plano VIP:", reply_markup=InlineKeyboardMarkup(teclado))

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    plano = update.callback_query.data.replace("buy_", "")
    txid = codigo()
    valor = PLANOS[plano]["valor"]
    pix = criar_pix(valor, f"Compra VIP {plano}", txid)
    salvar_pagamento(txid, str(update.callback_query.from_user.id), plano, valor)

    await update.callback_query.edit_message_text(
        f"💰 PIX gerado:\n\n`{pix['pixCopiaECola']}`\n\n"
        f"Valor: R$ {valor}\nSeu VIP será liberado automaticamente após o pagamento.",
        parse_mode="Markdown"
    )

async def cb(update, context):
    d = update.callback_query.data
    if d == "vip":
        await vip(update, context)
    elif d.startswith("buy_"):
        await buy(update, context)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(cb))
app.run_polling()
