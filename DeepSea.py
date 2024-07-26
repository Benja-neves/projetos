import os
import random
import json

#           azul        verde      amarelo     rosa      laranja      azul claro
cores = ['\033[94m', '\033[92m', '\033[93m', '\033[95m', '\033[91m', '\033[96m']
reset_cor = '\033[0m' # Branco
min_j = 4
max_j = 6
tamanhomapa = [15, 30, 45]
oxigenio_opcoes = list(range(45, 121))
RECORDS_FILE = "records.json"

def menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print("\033[1m\033[0m========\033[96m    DEEP SEA    \033[0m=========\033[1m\033[0m")

        print("\n1. Iniciar\n2. Regras\n3. Recordes\n4. Sair")
        escolha = input("\nEscolha uma opção: ")

        if escolha == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            Start()
        elif escolha == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            regras()
            input("")
        elif escolha == '3':
            os.system('cls' if os.name == 'nt' else 'clear')
            recordes()
            input("")
        elif escolha == '4':
            print("Bye")
            break
        else:
            input("Opção inválida")

def regras():

    print("\033[1m************************************************************************************************************\033[0m\n")
    print('\033[1mREGRAS:\033[0m\n')
    print(' - Você pode jogar com até 6 jogadores, sendo o mínimo 4.\n'
          ' - O mapa pode ser de 15, 30 ou 45 blocos.\n'
          ' - Existem tesouros pelo percurso (a cada 1/3 de profundidade os tesouros dobram de valor).\n'
          ' - Cada quilo de tesouro consome respectivamente seu oxigênio (1kg = 1 unidade de oxigênio consumido).\n'
          ' - Ganha aquele que ao final do oxigênio (compartilhado com todos os jogadores) tiver mais quilos de tesouros.\n'
          ' - Use as teclas A e D para se mover e S ou N para negar ou permitir uma ação\n')

    print("\033[1m************************************************************************************************************\033[0m")

def recordes():
    recordes = carregar_recordes()
    print("\033[1m************************************************************************************************************\033[0m\n")
    print('\033[1mRECORDES:\033[0m\n')
    if not recordes:
        print("Nenhum recorde registrado.")
    else:
        for i, recorde in enumerate(recordes):
            if i == 0:
                print(f"{cores[i]}👑 1º lugar: {recorde['jogador']} - Tesouros: {recorde['tesouros']} - Peso: {recorde['peso']}kg{reset_cor}")
            else:
                print(f"  {i+1:2}º lugar: {recorde['jogador']} - Tesouros: {recorde['tesouros']} - Peso: {recorde['peso']}kg")
    print("\033[1m************************************************************************************************************\033[0m\n")

def carregar_recordes():
    try:
        with open(RECORDS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvarrecordes(recordes):
    with open(RECORDS_FILE, 'w') as file:
        json.dump(recordes, file, indent=4)

def atualizarrecordes(novo_recorde):
    recordes = carregar_recordes()
    recordes.append(novo_recorde)
    recordes = sorted(recordes, key=lambda x: x['peso'], reverse=True)[:5]
    salvarrecordes(recordes)

def criarmapa(tamanho):

    if tamanho not in tamanhomapa:
        print("Digite um valor coerente.")
        return None

    bloco = tamanho + 1
    mapa = ['_' for _ in range(bloco)]
    ptesouro = []
    profundidade = bloco - 1
    dtesouro = profundidade // 3
    ptesouro.extend([0] + [1] * dtesouro + [2] * dtesouro + [4] * (profundidade - 2 * dtesouro))
    return mapa, ptesouro

def mostrarmapa(mapa, tesouros, jogadores, tamanho_mapa):

    colunas = tamanho_mapa // 3

    linhas = (len(mapa) - 1) // colunas
    print("\nSubmarino")

    print("----" * colunas + '-')

    for i in range(linhas):
        linha = []
        for j in range(colunas):
            posicao = 1 + i * colunas + j
            jogador_na_posicao = [idx for idx, pos in enumerate(jogadores) if pos == posicao]
            if jogador_na_posicao:
                cor = cores[jogador_na_posicao[0]]
                linha.append(f'{cor}X{reset_cor}')
            elif tesouros[posicao] > 0:
                linha.append(f'{tesouros[posicao]}')
            else:
                linha.append('_')
        print("| " + " | ".join(linha) + " | ")
        print("----" * colunas + '-')

def oxigenio(ptotal_tesouros):

    return ptotal_tesouros + 1

def dado():
    num = random.randint(1, 3)
    print(f"\nDADOS ROLANDO!\nVc tioru {num}!\n")
    return num

def Start():

    tamanho = num_jogadores = jogador_atual = submarino = 0

    # tamanho mapa
    while tamanho not in tamanhomapa:
        tamanho = int(input("Digite o tamanho do mapa (15, 30 ou 45 blocos):\n"))
        if tamanho not in tamanhomapa:
            print("Tamanho inválido! Escolha entre 15, 30 ou 45.")

    mapa, tesouros = criarmapa(tamanho)
    
    if not mapa:
        print("Erro ao criar o mapa. Tente novamente.")
        return
    
    # numero jogadores
    while num_jogadores < min_j or num_jogadores > max_j:
        num_jogadores = int(input(f"Digite o número de jogadores ({min_j} a {max_j}):\n"))

    jogadores = [0] * num_jogadores
    tesouros_coletados = [0] * num_jogadores
    ptotal_tesouros = [0] * num_jogadores
    oxigenio_gasto = [0] * num_jogadores
    voltando = [False] * num_jogadores

    # quantidade de oxigenio
    oxigenio_disponivel = int(input(f"Digite a quantidade de tanques de oxigênio desejada (entre {min(oxigenio_opcoes)} e {max(oxigenio_opcoes)}):\n"))

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        if jogadores[jogador_atual] == submarino:
            print(f"{cores[jogador_atual]}Você está no submarino, só pode ir para direita ->.{reset_cor}")
            direcao = 'd' 
        else:
            consumo_oxigenio = oxigenio(ptotal_tesouros[jogador_atual])
            oxigenio_disponivel -= consumo_oxigenio
            oxigenio_gasto[jogador_atual] += consumo_oxigenio

        mostrarmapa(mapa, tesouros, jogadores, tamanho)

        print(f"Oxigênio restante: {oxigenio_disponivel} tanques")

        print(f"Tesouros coletados por jogador:")
        for i in range(num_jogadores):
            print(f"{cores[i]}Jogador {i+1}:{reset_cor} {tesouros_coletados[i]} tesouros ({ptotal_tesouros[i]} kg)")

        # Verificar oxigenio e se o jogo acabou

        if oxigenio_disponivel <= 0:
            print('\033[1;31mGAME OVER\033[0m\n\nPLACAR:\n')
            for i in range(num_jogadores):
                print(f"{cores[i]}Jogador {i+1}:{reset_cor}- {oxigenio_gasto[i]} tanques de oxigênio gastos")
                print(f"          - {tesouros_coletados[i]} tesouros coletados ({ptotal_tesouros[i]}kg)\n")
            
            max_tesouro = max(ptotal_tesouros)
            vencedores = [i + 1 for i, peso in enumerate(ptotal_tesouros) if peso == max_tesouro]

            for vencedor in vencedores:
                nome_vencedor = input(f"{cores[vencedor-1]}Jogador {vencedor} venceu com {ptotal_tesouros[vencedor-1]} kg de tesouros!\nDigite seu nome: {reset_cor}")
                while not nome_vencedor:
                    nome_vencedor = input(f"{cores[vencedor-1]}Por favor, digite seu nome: {reset_cor}")
                atualizarrecordes({'jogador': nome_vencedor, 'tesouros': tesouros_coletados[vencedor-1], 'peso': ptotal_tesouros[vencedor-1]})

            input('Aperte Enter para voltar ao menu')
            break

        # Movimento de so poder andar para atrás
        passos = dado()
        if voltando[jogador_atual]:
            while True:
                direcao = input(f"{cores[jogador_atual]}Jogador {jogador_atual+1}, só é possível andar para esquerda <- . Deseja se mover? (A/N):\n{reset_cor}").lower()
                if direcao == 'a':
                    break
                else:
                    print("\033[91mIsso não é uma das opções, tente novamente.\033[0m")
                    continue
        else:
            direcao = input(f"{cores[jogador_atual]}Jogador {jogador_atual+1}, qual direção deseja se mover? (A/D):\n{reset_cor}").lower()
            if direcao not in ['a', 'd']:
                print("\033[91mIsso não é uma das opções, tente novamente.\033[0m")
                continue

        # Movimento comum
        # Direita 
        if direcao == 'a':
            proxima_posicao = jogadores[jogador_atual] - passos
            while proxima_posicao > 0 and proxima_posicao in jogadores:
                proxima_posicao -= 1
            if proxima_posicao >= 0:
                jogadores[jogador_atual] = proxima_posicao
                voltando[jogador_atual] = True
            else:
                print("\033[91mVocê está no limite do mapa! De meia volta.\033[0m")
                voltando[jogador_atual] = False
                continue

        # Esquerda 
        elif direcao == 'd':
            proxima_posicao = jogadores[jogador_atual] + passos
            while proxima_posicao < len(mapa) and proxima_posicao in jogadores:
                proxima_posicao += 1
            if proxima_posicao < len(mapa):
                jogadores[jogador_atual] = proxima_posicao
                voltando[jogador_atual] = False
            else:
                print("\033[91mVocê está no limite do mapa! De meia volta.\033[0m")
                voltando[jogador_atual] = True
                continue

        # Tesouro (pegar e verificar se tem no bloco)
        if tesouros[jogadores[jogador_atual]] > 0:
            coletar = input(f"{cores[jogador_atual]}Jogador {jogador_atual+1}, você encontrou um tesouro de {tesouros[jogadores[jogador_atual]]}kg. Deseja pegar? (S/N):\n{reset_cor}").lower()
            if coletar == 's':
                ptotal_tesouros[jogador_atual] += tesouros[jogadores[jogador_atual]]
                tesouros_coletados[jogador_atual] += 1
                tesouros[jogadores[jogador_atual]] = 0
        
        jogador_atual = (jogador_atual + 1) % num_jogadores

menu()