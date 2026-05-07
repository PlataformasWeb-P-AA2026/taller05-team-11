# ===============================================
# TALLER 05 - ETL
# HTML + CSV + PDF -> mundial_2026.json
# ===============================================

import pandas as pd
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import json
import os

# ===============================================
# RUTAS
# ===============================================
BASE = "data"

CSV_FILE = os.path.join(BASE, "fuente_csv_sudamerica.csv")
HTML_FILE = os.path.join(BASE, "fuente_html_europa.html")
PDF_FILE = os.path.join(BASE, "fuente_pdf_norteamerica_asia.pdf")

OUTPUT = "mundial_2026.json"

# ===============================================
# EXTRACT + TRANSFORM CSV
# ===============================================
def procesar_csv():
    df = pd.read_csv(CSV_FILE)

    docs = []
    for _, row in df.iterrows():
        docs.append({
            "nombre": row["nombre"],
            "seleccion": row["seleccion"],
            "posicion": row["posicion"],
            "edad": int(row["edad"]),
            "partidos": int(row["partidos"])
        })

    return docs


# ===============================================
# EXTRACT + TRANSFORM HTML
# ===============================================
def procesar_html():
    with open(HTML_FILE, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    filas = soup.find_all("tr")[1:]  # saltar encabezado

    docs = []

    for fila in filas:
        celdas = fila.find_all("td")

        docs.append({
            "nombre": celdas[0].text.strip(),
            "seleccion": celdas[1].text.strip(),
            "posicion": celdas[2].text.strip(),
            "edad": int(celdas[3].text.strip()),
            "club_actual": celdas[4].text.strip()
        })

    return docs


# ===============================================
# EXTRACT + TRANSFORM PDF
# ===============================================
def procesar_pdf():
    reader = PdfReader(PDF_FILE)

    texto = ""
    for page in reader.pages:
        texto += page.extract_text() + "\n"

    lineas = [x.strip() for x in texto.split("\n") if x.strip()]

    # quitar encabezados
    encabezados = {"Nombre", "Seleccion", "Posicion", "Edad", "Goles"}
    datos = [x for x in lineas if x not in encabezados]

    docs = []

    # grupos de 5 campos
    for i in range(0, len(datos), 5):
        if i + 4 < len(datos):
            docs.append({
                "nombre": datos[i],
                "seleccion": datos[i+1],
                "posicion": datos[i+2],
                "edad": int(datos[i+3]),
                "goles": int(datos[i+4])
            })

    return docs


# ===============================================
# LOAD JSON
# ===============================================
def guardar_json(docs):
    estructura = {
        "docs": docs
    }

    with open(OUTPUT, "w", encoding="utf-8") as file:
        json.dump(estructura, file, indent=4, ensure_ascii=False)


# ===============================================
# MAIN ETL
# ===============================================
def main():
    documentos = []

    documentos.extend(procesar_csv())
    documentos.extend(procesar_html())
    documentos.extend(procesar_pdf())

    guardar_json(documentos)

    print("Proceso ETL completado.")
    print("Archivo generado:", OUTPUT)
    print("Total registros:", len(documentos))


if __name__ == "__main__":
    main()