from pathlib import Path

from projeto_pendulo.rastreamento_pendulo import rastrear_pendulo
from projeto_pendulo.dinamica import calcular_angulo
#from projeto_pendulo.simulacao import simular_pendulo

BASE_DIR = Path(__file__).resolve().parent

caminho = BASE_DIR / "dados" / "entrada" / "IMG_1060.MOV"
caminho_saida = BASE_DIR / "dados" / "saida" / "video_rastreamento.MOV"
caminho_csv = BASE_DIR / "dados" / "saida" / "dados_posicoes.csv"
caminho_csv_angulos = BASE_DIR / "dados" / "saida" / "dados_angulos.csv"
#caminho_csv_simulacao = r'C:\Users\pedro\OneDrive\Documentos\Faculdade\LAB VI\dados_angulos.csv'



def main():

    rastrear_pendulo(
        caminho,
        caminho_csv,
        caminho_saida
    )

    dados_angulos = calcular_angulo(caminho_csv)

    dados_angulos.to_csv(
        caminho_csv_angulos,
        index=False
    )

    #dados_simulacao = simular_pendulo(
     #   caminho_csv_angulos
    #)

    #dados_simulacao.to_csv(
    #    caminho_csv_simulacao,
    #    index=False
    #)

if __name__ == "__main__":
    main()