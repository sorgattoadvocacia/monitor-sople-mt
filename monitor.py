import pandas as pd
import os
from datetime import date

MUNICIPIOS = [
    "MATUPÁ",
    "PEIXOTO DE AZEVEDO",
    "GUARANTÃ DO NORTE",
    "TERRA NOVA DO NORTE",
    "NOVO MUNDO",
    "PARANAÍTA",
    "ALTA FLORESTA",
    "APIACÁS"
]

ENTRADA = "input.csv"
PASTA = "data"
BASE = "data/base.csv"

def normaliza(x):
    return str(x).strip().upper()

def carregar():
    df = pd.read_csv(ENTRADA, dtype=str)
    df["Município"] = df["Município"].apply(normaliza)
    df["Processo"] = df["Processo"].astype(str).str.strip()
    return df[df["Município"].isin(MUNICIPIOS)]

def main():
    os.makedirs(PASTA, exist_ok=True)

    hoje = carregar()

    if os.path.exists(BASE):
        ontem = pd.read_csv(BASE, dtype=str)
    else:
        ontem = pd.DataFrame(columns=hoje.columns)

    novos = hoje[~hoje["Processo"].isin(ontem["Processo"])]
    removidos = ontem[~ontem["Processo"].isin(hoje["Processo"])]

    hoje.to_csv(BASE, index=False)

    print("DATA:", date.today())
    print("NOVOS:", len(novos))
    print("REMOVIDOS:", len(removidos))

    if len(novos) or len(removidos):
        print("ALERTA: ESTOQUE ALTERADO")
    else:
        print("SEM ALTERAÇÃO")

if __name__ == "__main__":
    main()
