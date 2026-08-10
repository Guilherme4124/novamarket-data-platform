import os
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import storage

# ==============================
# Configuração do projeto
# ==============================

ROOT_DIR = Path(__file__).resolve().parents[2]

load_dotenv(dotenv_path=ROOT_DIR / ".env", override=True)

ROOT_DIR = Path(__file__).resolve().parents[2]

load_dotenv(ROOT_DIR / ".env")

print(ROOT_DIR)
print((ROOT_DIR / ".env").exists())

print(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
print(os.getenv("BUCKET_NAME"))

CAMINHO_XML = Path("C:/NovaMarket/ERP/SaidaXML")

CAMINHO_CREDENCIAIS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
BUCKET_NAME = os.getenv("BUCKET_NAME")

print("=" * 50)
print("ROOT:", ROOT_DIR)
print("CREDENCIAIS:", CAMINHO_CREDENCIAIS)
print("BUCKET:", BUCKET_NAME)
print("=" * 50)

# ============================== 
# Cliente GCP
# ==============================

client = storage.Client.from_service_account_json(
    CAMINHO_CREDENCIAIS
)


def enviar_xmls():
    bucket = client.bucket(BUCKET_NAME)

    arquivos = list(CAMINHO_XML.glob("*.xml"))

    print(f"\nXMLs encontrados: {len(arquivos)}")

    if not arquivos:
        print("Nenhum XML encontrado.")
        return

    for arquivo in arquivos:
        destino = f"landing/erp/{arquivo.name}"

        blob = bucket.blob(destino)

        blob.upload_from_filename(str(arquivo))

        print(f"✔ {arquivo.name} enviado para {destino}")


if __name__ == "__main__":
    enviar_xmls()