from flask import Flask, request
from database import confirmar_pagamento, liberar_vip, PLANOS
import requests

BOT_TOKEN = "8578511352:AAFxiP2PwlZySHpXbYbv_JNZrsXs6mwMjro"
CHAT_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

app = Flask(__name__)

@app.route("/webhook/efi", methods=["POST"])
def efi_webhook():
    data = request.json
    # Evento de PIX recebido
    if data.get("evento") == "PIX_RECEBIDO":
        txid = data["pix"][0]["txid"]
        pagamento = confirmar_pagamento(txid)
        if pagamento:
            user_id, plano = pagamento
            dias = PLANOS[plano]["dias"]
            liberar_vip(user_id, plano, dias)
            # Notificar usuário no Telegram
            requests.post(CHAT_API, json={
                "chat_id": user_id,
                "text": f"✅ Seu VIP {plano} foi liberado automaticamente!"
            })
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
