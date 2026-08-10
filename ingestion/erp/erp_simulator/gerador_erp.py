from pathlib import Path
from datetime import datetime
import xml.etree.ElementTree as ET

# Caminho onde o ERP "salva" os XMLs
PASTA_SAIDA = Path("C:/NovaMarket/ERP/SaidaXML")


def criar_pastas():
    """Cria a estrutura de pastas do ERP."""
    PASTA_SAIDA.mkdir(parents=True, exist_ok=True)


def criar_nota():
    """Simula uma nota fiscal gerada pelo ERP."""

    return {
        "numero": "000001",
        "data_emissao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cliente": "João da Silva",
        "cnpj": "12.345.678/0001-90",
        "produto": "Notebook Dell",
        "quantidade": 2,
        "valor_unitario": 3500.00
    }


def gerar_xml(nota: dict):
    """Converte o dicionário em XML."""

    raiz = ET.Element("notaFiscal")

    for chave, valor in nota.items():
        elemento = ET.SubElement(raiz, chave)
        elemento.text = str(valor)

    arvore = ET.ElementTree(raiz)

    caminho_arquivo = PASTA_SAIDA / f"NFE_{nota['numero']}.xml"

    arvore.write(
        caminho_arquivo,
        encoding="utf-8",
        xml_declaration=True
    )

    print(f"XML criado com sucesso em:\n{caminho_arquivo}")


if __name__ == "__main__":
    criar_pastas()

    nota = criar_nota()

    gerar_xml(nota)