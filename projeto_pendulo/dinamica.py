import pandas as pd
import numpy as np

def calcular_vetor(ponto_inicial, ponto_final):
    """
    Calcula o vetor que vai do ponto inicial ao ponto final
    Exemplo: vetor = P1 - P0
    """

    x_inicial, y_inicial = ponto_inicial
    x_final, y_final = ponto_final

    vx = x_final - x_inicial
    vy = y_final - y_inicial

    return vx, vy

def calcular_angulo_vertical(vetor):
    """
    Calcula o ângulo orientado entre um vetor e a vertical
    O resultado é dado em radianos

    positivo: vetor em direção para a direita
    direita: vetor em direção para a esquerda 
    """

    vx, vy = vetor
    angulo = np.arctan2(vx, vy)

    return angulo

def calcular_angulo(caminho_csv):
    """
    Leitura dos dados das posições e calculo dos ângulos
    das hastes do pêndulo. 
    
    theta_1: ângulo entre P0 - P1 e a vertical
    theta_2: ângulo entre P1 - P2 e a vertical 
    """

    dados = pd.read_csv(caminho_csv)

    resultados = []

    for _, linha in dados.iterrows():
        #
        # POSIÇÕES
        #

        P0 = (linha["P0_x"], linha["P0_y"])
        P1 = (linha["P1_x"], linha["P1_y"])
        P2 = (linha["P2_x"], linha["P2_y"])

        #
        #VETORES DAS HASTES
        #
        
        r1 = calcular_vetor(P0, P1)
        r2 = calcular_vetor(P1, P2)

        #
        # ANGULO ENTRE A VERTICAL 
        #

        theta_1 = calcular_angulo_vertical(r1)
        theta_2 = calcular_angulo_vertical(r2)

        theta_1_graus = np.degrees(theta_1)
        theta_2_graus = np.degrees(theta_2)

        resultados.append({
            "frame": linha["frame"],
            "tempo": linha["tempo"],

            "theta_1": theta_1,
            "theta_2": theta_2,

            "theta_1_graus": theta_1_graus,
            "theta_2_graus": theta_2_graus
        })

    return pd.DataFrame(resultados)