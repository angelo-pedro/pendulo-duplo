import cv2
import numpy as np
import csv

def centro_da_mascara(mascara, 
                      area_minima=20):
    """
    Encontra o centro da maior região colorida presente na máscara.

    Parâmetros:
        mascara: imagem binária produzida pelo HSV (Matiz (Hue), Saturação (Saturation) e Valor/Brilho (Value))
        area_minima: área mínima para considerar uma região válida
    
    Retorno:
    (x, y): coordenadas do centro
    None: caso nenhuma região válida seja encontrada
    """

    # Encontra os contornos da máscara
    contornos, _ = cv2.findContours(
        mascara,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    ) 

    if not contornos:
        return None

    #seleciona o maior contorno
    maior_contorno = max(contornos, key=cv2.contourArea)

    #verifica se é suficientemente grande
    area = cv2.contourArea(maior_contorno)

    if area < area_minima:
        return None

    M = cv2.moments(maior_contorno)

    #evitar divisão por zero

    if M['m00'] == 0:
        return None 

    x = int(M['m10']/M['m00'])
    y = int(M['m01']/M['m00'])

    return (x,y)

def detectar_pontos(frame):
    """
    Detecção de P0, P1, P2 e V

    P0: Ponto Azul
    P1: Ponto Vermelho
    P2: Ponto Verde
    V: Ponto Laranja


    Retorno:
    Dicionário com as quatro posições
    """

    #Converte RGB para HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #
    # VERMELHO
    #

    vermelho_1 = cv2.inRange(
        hsv,
        np.array([0,100,100]),
        np.array([10,255,255])
    )

    vermelho_2 = cv2.inRange(
        hsv,
        np.array([170, 100, 100]),
        np.array([179, 255, 255])
    )

    mascara_vermelha = cv2.bitwise_or(
        vermelho_1,
        vermelho_2
    )

    #
    # VERDE
    #

    mascara_verde = cv2.inRange(
        hsv,
        np.array([35, 80, 80]),
        np.array([85, 255, 255])
    )

    #
    # AZUL
    #

    mascara_azul = cv2.inRange(
        hsv,
        np.array([90, 100, 100]),
        np.array([140, 255, 255])
    )

    #
    # LARANJA
    #
    mascara_laranja = cv2.inRange(
        hsv,
        np.array([9, 100, 100]),
        np.array([16, 255, 255])
    )

    #Encontrar os pontos 
    
    V = centro_da_mascara(mascara_laranja)
    P2 = centro_da_mascara(mascara_verde)
    P1 = centro_da_mascara(mascara_vermelha)
    P0 = centro_da_mascara(mascara_azul)

    pontos = {
        "P0": P0,
        "P1": P1,
        "P2": P2,
        "V": V
    }

    return pontos

def desenhar_pontos(frame, 
                    pontos):
    """
    Desenha os pontos detectados sobre o frame
    """

    for nome, ponto in pontos.items():
        if ponto is None:
            continue
        x, y = ponto

        #Desenha um círculo 
        cv2.circle(
            frame,
            (x,y),
            10,
            (255, 255, 255),
            2
        )

    #Escreve o nome do ponto

        cv2.putText(
            frame,
            nome,
            (x + 15, y - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    return frame 


def salvar_posicoes(
        posicoes, 
        caminho_csv, 
        fps):
    """
    Salva a posição dos pontos em um arquivo CSV
    Cada linha correpsonde a um ponto
    """

    with open(
        caminho_csv,
        "w",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        escritor = csv.writer(arquivo)

        #cabeçalho
        escritor.writerow([
            "frame",
            "tempo",
            "P0_x",
            "P0_y",
            "P1_x",
            "P1_y",
            "P2_x",
            "P2_y",
            "V_x",
            "V_y" 
        ])

        for i, pontos in enumerate(posicoes):
            tempo = i / fps

            linha = [i, tempo]

            for nome in ["P0", "P1", "P2", "V"]:
                ponto = pontos[nome]

                if ponto is None:
                    linha.extend([
                        np.nan,
                        np.nan
                    ])

                else:
                    x, y = ponto

                    linha.extend([
                        x,
                        y
                    ])
            escritor.writerow(linha)


def rastrear_pendulo(caminho,
                     caminho_csv = "dados_posicoes.csv",
                     caminho_saida="video_rastreamento.mp4"):
    """
    Abre o vídeo e rastreia P0, P1, P2 e V frame a frame e salva um arquivo em mp4
    """

    video = cv2.VideoCapture(caminho)

    if not video.isOpened():
        print('Não foi possível abrir o vídeo')
        return

    largura = int(
        video.get(cv2.CAP_PROP_FRAME_WIDTH)
    )

    altura = int(
        video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    )

    fps = int(
        video.get(cv2.CAP_PROP_FPS)
    )

    total_frames = int(
        video.get(cv2.CAP_PROP_FRAME_COUNT)
    )

    print("Total de frames: ", total_frames)

    #
    # CRIAR O ARQUIVO DE SAÍDA
    #

    fourcc = cv2.VideoWriter_fourcc(
        *"mp4v"
    )

    saida = cv2.VideoWriter(
        caminho_saida,
        fourcc,
        fps,
        (largura, altura)
    )

    if not saida.isOpened():
        print(
            "ERRO: não foi possível criar o vídeo de saída"
        )

        video.release()

    print(
        "Vídeo de saída foi concluído"
    )

    #
    # LISTA DE POSIÇÕES
    #

    posicoes = []

    #
    #PROCESSAR O VÍDEO
    #

    contador = 0 
    while True:

        #enquanto o vídeo não acaba
        sucesso, frame = video.read()

        if not sucesso:
            print("Falha na leitura do frame.")
            break

        #detecta os pontos
        pontos = detectar_pontos(frame)

        #guardar as posições

        posicoes.append(
            pontos
        )
        
        #desenha os pontos
        frame_com_pontos = desenhar_pontos(
            frame,
            pontos
        )

        saida.write(
            frame_com_pontos
        )

        #Mostra o frame
        cv2.imshow(
            "Rastreamento do Pêndulo",
            frame_com_pontos
        )

        contador += 1

        if contador % 50 == 0:
            print(
                f"Processando frame {contador}/{total_frames}"
            )

        #Encerrar manualmente
        tecla = cv2.waitKey(1) & 0xFF

        if tecla == 27:
            print("Processamento interrompido pela tecla ESC.")
            break

    video.release()
    saida.release()
    cv2.destroyAllWindows()

    salvar_posicoes(
        posicoes,
        caminho_csv,
        fps
    )

    print()
    print("Processamento terminado.")
    print("Frames processados:", contador)
    print("Vídeo salvo em:")
    print(caminho_saida)
