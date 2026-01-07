import os
import shutil
from bs4 import BeautifulSoup

PASTA_BASE = r"CAMINHO_DA_PASTA_BASE"
PASTA_ELIMINADOS = os.path.join(PASTA_BASE, "_ELIMINADOS")


def extrair_info(index_path):
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
    except UnicodeDecodeError:
        # fallback para arquivos antigos / mal codificados
        with open(index_path, "r", encoding="latin-1") as f:
            soup = BeautifulSoup(f, "html.parser")

    nome = curso = municipio = resultado = None

    for p in soup.find_all("p"):
        texto = p.get_text(strip=True)

        if texto.startswith("Nome:"):
            nome = texto.replace("Nome:", "").strip()
        elif texto.startswith("Curso:"):
            curso = texto.replace("Curso:", "").strip()
        elif texto.startswith("Município:"):
            municipio = texto.replace("Município:", "").strip()

    for table in soup.find_all("table"):
        for tr in table.find_all("tr"):
            th = tr.find("th")
            td = tr.find("td")
            if th and td and th.get_text(strip=True) == "Final":
                resultado = td.get_text(strip=True)

    return nome, curso, municipio, resultado


def processar_pastas():
    os.makedirs(PASTA_ELIMINADOS, exist_ok=True)

    print("\n=== PROCESSAMENTO INICIADO ===\n")

    for pasta in os.listdir(PASTA_BASE):
        caminho_pasta = os.path.join(PASTA_BASE, pasta)
        index_path = os.path.join(caminho_pasta, "index.html")

        if pasta == "_ELIMINADOS":
            continue

        if not os.path.isdir(caminho_pasta) or not os.path.exists(index_path):
            continue

        nome, curso, municipio, resultado = extrair_info(index_path)

        print(f"\nPasta: {pasta}")
        print(f"  Resultado: {resultado}")

        if resultado == "APTO":
            novo_nome = f"{municipio} - {curso} - {nome}".upper()
            novo_caminho = os.path.join(PASTA_BASE, novo_nome)

            if pasta == novo_nome:
                print("  ✔ JÁ ORGANIZADA — pulando")
                continue

            if os.path.exists(novo_caminho):
                print("  ⚠ JÁ EXISTE PASTA COM ESSE NOME — pulando")
                continue

            print(f"  ✔ RENOMEANDO PARA: {novo_nome}")
            os.rename(caminho_pasta, novo_caminho)

        else:
            destino = os.path.join(PASTA_ELIMINADOS, pasta)
            print("  🚫 MOVENDO PARA _ELIMINADOS")
            shutil.move(caminho_pasta, destino)


if __name__ == "__main__":
    processar_pastas()
