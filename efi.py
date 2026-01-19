import requests
import json
import base64

CLIENT_ID = "Client_Id_adceab6c17904de72da0c7e6ad0770aa8ff38c9e"
CLIENT_SECRET = "Client_Secret_c73efe6a3ca148c13b0fe96749000f65eaff76ef"
CERT_PATH = "certificado.p12"  # Seu certificado do EFI
KEY_PATH = "certificado.key"   # Sua chave privada do certificado
CHAVE_PIX = "70a914e6-7ac4-43dc-95ef-daa4e0d2d76e"

AUTH_URL = "https://pix.api.efipay.com.br/oauth/token"
PIX_URL = "https://pix.api.efipay.com.br/v2/cob"

def get_token():
    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }
    data = {"grant_type": "client_credentials"}
    r = requests.post(AUTH_URL, headers=headers, json=data, cert=(CERT_PATH, KEY_PATH))
    return r.json()["access_token"]

def criar_pix(valor, descricao, txid):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "calendario": {"expiracao": 1200},  # 20 minutos
        "valor": {"original": f"{valor:.2f}"},
        "chave": CHAVE_PIX,
        "solicitacaoPagador": descricao
    }
    r = requests.put(f"{PIX_URL}/{txid}", headers=headers, json=payload, cert=(CERT_PATH, KEY_PATH))
    return r.json()  # Retorna dados do Pix
