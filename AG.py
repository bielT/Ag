import random
import re
import time
import numpy as np
import tqdm 

def AG(n, value, weight, capacity, dp):
    num_items = n
    peso_limite = capacity

    valores = value
    pesos = weight

    tamanho_populacao = 1000
    taxa_mutacao = 0.001 
    num_geracoes = 100  # Aumente o número de gerações

    def aptidao(individuo):
        valor_total = sum(valores[i] for i in range(num_items) if individuo[i] == 1)
        peso_total = sum(pesos[i] for i in range(num_items) if individuo[i] == 1)

        if peso_total > peso_limite:
            return -1 # Penalizar soluções inválidas
        else:
            return valor_total

    def filhos_val(filho):
        while aptidao(filho) == -1: 
            a = [i for i in range(num_items) if filho[i] == 1] 

            numero_aleatorio = random.choice(a)  
            filho[numero_aleatorio] = 0
        return filho
    populacao = []
    for _ in range(tamanho_populacao):
        populacao.append([random.randint(0, 1) for _ in range(num_items)])

    for geracao in tqdm.tqdm(range(num_geracoes)): 
    #for geracao in range(num_geracoes):
        

        pais = populacao
        
   
        filhos = []

        for i in range(0, len(pais), 2):
            gabarito = [random.randint(0, 1) for _ in range(num_items)]
            filho1 = []
            filho2 = []
            for j in gabarito:
                filho1 =  pais[i] if j == 0 else   pais[i + 1]
                filho2 =  pais[i] if j == 1 else   pais[i + 1]


            filhos.append(filhos_val(filho1))
            filhos.append(filhos_val(filho2))

        

        for i in range(len(filhos)):
            for j in range(num_items):
                if random.random() < taxa_mutacao:
                    filhos[i][j] = 1 - filhos[i][j]
       
        populacao = filhos
        aptidoes = [aptidao(individuo) for individuo in populacao]
        for _ in range(tamanho_populacao // 2):
            torneio = random.sample(range(tamanho_populacao), 2)
            vencedor = max(torneio, key=lambda x: aptidoes[x])
            pais.append(populacao[vencedor])
        
    melhor_individuo = max(populacao, key=aptidao)

    melhor_valor = aptidao(melhor_individuo)

    print("Melhor solução encontrada:")
    print("Itens na mochila:", [i for i in range(num_items) if melhor_individuo[i] == 1])
    print("Valor total:", melhor_valor)
    print("peso:", [ sum(pesos[i] for i in range(num_items) if melhor_individuo[i] == 1)])
    print("peso limite:", peso_limite)
    return melhor_valor

def solve_AG_problem(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    n = int(lines[0].strip())
    capacity = int(lines[-1].strip())

    id, value, weight = [], [], []
    for line in lines[1:-1]:
        numbers = re.findall(r"[0-9]+", line)
        id.append(int(numbers[0]) - 1)
        value.append(int(numbers[1]))
        weight.append(int(numbers[2]))

    dp = np.full((n, capacity + 1), -1, dtype=int)
    max_value = AG(n, value, weight, capacity, dp)
    return max_value

def main():
    output_max_values = []

    for iterator in range(1, 6):
        input_file_path = f"input/input{iterator}.in"
        max_value = solve_AG_problem(input_file_path)
        output_max_values.append(max_value)
        output_line = f"Instancia {iterator} : {max_value}\n"

        with open("output/ag.out", "a+") as output_file:
            output_file.write(output_line)

if __name__ == "__main__":
    start_time = time.time()
    main()
    execution_time = time.time() - start_time
    print(f"Execution time: {execution_time} seconds")