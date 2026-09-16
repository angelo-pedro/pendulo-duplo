from projeto_pendulo.rastreamento_pendulo import rastrear_pendulo
from projeto_pendulo.dinamica import calcular_angulo

def main():

    caminho = r'C:\Users\pedro\OneDrive\Documentos\Faculdade\LAB VI\IMG_1020.MOV'
    caminho_saida = r'C:\Users\pedro\OneDrive\Documentos\Faculdade\LAB VI\video_rastreamento.mp4'
    caminho_csv = r'C:\Users\pedro\OneDrive\Documentos\Faculdade\LAB VI\dados_posicoes.csv'
    caminho_csv_angulos = r'C:\Users\pedro\OneDrive\Documentos\Faculdade\LAB VI\dados_angulos.csv'

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

if __name__ == "__main__":
    main()