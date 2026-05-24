"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


#def clean_campaign_data():
"""
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



"""

    #      return



import os
import glob
import pandas as pd
from zipfile import ZipFile


def clean_campaign_data():

    # se lee los archivos zip en la carpeta de entrada
    zips = glob.glob("./files/input/*.zip")
    print(f"Archivos encontrados: {len(zips)}")

    frames = []
    for z_path in zips:
        with ZipFile(z_path) as z:
            for name in z.namelist():
                if name.endswith(".csv"):
                    print(f"Leyendo: {name}")
                    with z.open(name) as f:
                        frames.append(pd.read_csv(f))

    df = pd.concat(frames, ignore_index=True)
    print(f"Total filas cargadas: {len(df)}")
    print(f"Columnas: {list(df.columns)}")

    os.makedirs("./files/output", exist_ok=True)

    # --- client.csv ---
    client = df[["client_id", "age", "job", "marital",
                 "education", "credit_default", "mortgage"]].copy()

    client["job"] = client["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)

    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].replace("unknown", pd.NA)

    # se coniverte yes/no a 1/0 para estas dos columnas
    for col in ["credit_default", "mortgage"]:
        client[col] = (client[col].str.strip().str.lower() == "yes").astype(int)

    client.to_csv("./files/output/client.csv", index=False)
    print(f"client.csv guardado con {len(client)} filas")

    # --- campaign.csv ---
    campaign = df[["client_id", "number_contacts", "contact_duration",
                   "previous_campaign_contacts", "previous_outcome",
                   "campaign_outcome", "day", "month"]].copy()

    campaign["previous_outcome"] = (campaign["previous_outcome"].str.lower() == "success").astype(int)
    campaign["campaign_outcome"] = (campaign["campaign_outcome"].str.lower() == "yes").astype(int)

    # se arma la fecha con day, month y el año 2022
    campaign["last_contact_date"] = pd.to_datetime(
        campaign["day"].astype(str) + " " + campaign["month"] + " 2022",
        format="%d %b %Y"
    ).dt.strftime("%Y-%m-%d")

    campaign.drop(columns=["day", "month"], inplace=True)

    campaign.to_csv("./files/output/campaign.csv", index=False)
    print(f"campaign.csv guardado con {len(campaign)} filas")

    # --- economics.csv ---
    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    economics.to_csv("./files/output/economics.csv", index=False)
    print(f"economics.csv guardado con {len(economics)} filas")


if __name__ == "__main__":
    clean_campaign_data()
