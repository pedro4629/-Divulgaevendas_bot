from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Webhook ativo", 200

@app.route("/webhook/efi", methods=["POST"])
def webhook_efi():
    data = request.json
    print("Webhook EFI recebido:", data)
    return jsonify({"status": "ok"}), 200
