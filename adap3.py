import random
import time
import matplotlib.pyplot 
import numpy as np
import cv2 as cv
import os

pasta = "C:\comp_evo"
N_Circulos = [52, 305, 4, 160, 18, 64, 30, 92, 76, 104, 3, 37, 146, 60, 56, 52, 76, 95, 68, 51] 
tempo_inicio = time.time()
parametro = [0,0,0,0,0,0,0,0]

def count_circles_in_image(image_path, param1, param2, min_radius, max_radius):
    # Carregar a imagem
    img = cv.imread(image_path)
    if img is None:
        print(f"Erro ao carregar a imagem: {image_path}")
        return 0, []

    # Converter a imagem para escala de cinza
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Aplicar uma operação de abertura para remover ruídos
    kernel = np.ones((5, 5), np.uint8)
    processed_gray = cv.morphologyEx(gray, cv.MORPH_OPEN, kernel)

    # Detectar círculos usando o método HoughCircles
    circles = cv.HoughCircles(
        processed_gray,
        cv.HOUGH_GRADIENT,
        dp=1.1,
        minDist=20,
        param1=param1,
        param2=param2,
        minRadius=min_radius,
        maxRadius=max_radius
    )

    # Se círculos forem detectados, retornar o número de círculos e os raios
    if circles is not None:
        circles = np.uint16(np.around(circles))
        radii = [circle[2] for circle in circles[0, :]]
        return len(circles[0]), radii

    return 0, []

# Função principal para processar todas as imagens de uma pasta
def process_images_in_folder(folder_path, param1, param2, min_radius, max_radius):
    # Listar todos os arquivos na pasta
    raios = []
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]

    if not image_files:
        print("Nenhuma imagem .jpg encontrada na pasta.")
        return
    jooj = 0
    #with open(output_txt_path, 'w') as output_file:
    for image_file in image_files:
            if jooj >= 6:
                break
            image_path = os.path.join(folder_path, image_file)
            num_circles, radii = count_circles_in_image(image_path, param1, param2, min_radius, max_radius)
            median_radius = np.median(radii) if radii else 0
            raios.append(num_circles)
            
            print(f"Processado {image_file}: {num_circles} círculos encontrados, Mediana do raio: {median_radius}")
            jooj += 1
            time.sleep(2)
    return raios

def inicializar():
    population = []
    for i in range(10):
        j = 0
        populante = [parametro,parametro]
        param1 = []
        while j < 8:
            param1.append(random.randint(0,1))
            j += 1
        populante[0] = param1
        
        j = 0
        param2 = []
        while j < 8:
            param2.append(random.randint(0,1))
            j += 1
        populante[1] = param2
        population.append(populante)
    return population

def calculo_fitness(populante):
    
    i = 0

    # Converta o vetor em uma string
    param1_aux = populante[0]
    binario_str = ''.join(map(str, param1_aux))
    # Converta a string binária em um número inteiro
    param1 = int(binario_str,2)
    
    param2_aux = populante[1]
    binario_str = ''.join(map(str, param2_aux))
    # Converta a string binária em um número inteiro
    param2 = int(binario_str,2)
    
    circulos = process_images_in_folder(folder_path=pasta, param1=param1, param2= param2, min_radius=30, max_radius=100)
    diferenca = []
    #Penalizar mais quando erra pra baixo
    while i<6: #i<20:
        diferenca.append(circulos[i] - N_Circulos[i])
        if diferenca[i] < 0:
            diferenca[i] = - 3 * diferenca[i]
        i += 1
    return 1/np.linalg.norm(diferenca)


def selecao(population):
    k = 0.75
    pais = []
    
    for i in range(10):#escolha dos pais
        prob = random.uniform(0,1)
        papai = population[random.randint(0,9)]
        mamae = population[random.randint(0,9)]
        aux_mamae = calculo_fitness(mamae)
        aux_papai = calculo_fitness(papai)
        if prob > k :
        #O pior é escolhido
            if(aux_papai<aux_mamae):
                pais.append(papai)
            else:
                pais.append(mamae)
        if prob < k :
        #O melhor é escolhido
            if(aux_papai<aux_mamae):
                pais.append(mamae)
            else:
                pais.append(papai)
    return pais


#reproduz
def crossover(pais):
    filhos = []
    
    for babae in pais:
        filho = [[], []]
        ponto_cross = random.randint(0,7)
        j=0
        papai_2 = pais[random.randint(0,9)]
        m_aux1 = babae[0]
        p_aux1 = papai_2[0]
        m_aux2 = babae[1]
        p_aux2 = papai_2[1]
        while j < 8:
            if(j<ponto_cross):
                filho[0].append(m_aux1[j])
            if(j>=ponto_cross):
                filho[0].append(p_aux1[j])
            j = j+1
        j = 0
        while j < 8:
            if(j<ponto_cross):
                filho[1].append(p_aux2[j])
            if(j>=ponto_cross):
                filho[1].append(m_aux2[j])
            j = j+1
        
        filhos.append(filho)
    
    return filhos

#mutação
def mutacao(population):
    prob = 0.05
    res = []
    for p in population:
        k = random.uniform(0,1)
        l = random.uniform(0,1)
        param1 = p[0]
        param2 = p[1]
        if k<prob:
            i = random.randint(0,7)
            j = random.randint(0,1)
            param1[i] = j
        if l<prob:
            i = random.randint(0,7)
            j = random.randint(0,1)
            param2[i] = j
        res.append(p)
    return res

#####Main

iteracoes = 50
population = inicializar()

it = 1
best = []
best_fitness = 0
fitness_historico = []
time_ = []
while it < iteracoes:
    
    print('Iteração',it)
    it += 1
    pais = selecao(population)

    filhos = crossover(pais)

    population = mutacao(filhos)

    for a in population:
        if best_fitness < calculo_fitness(a):
            best_fitness = calculo_fitness(a)
            best = a
            fitness_historico.append(best_fitness)
            time_.append(it)



tempo_fim = time.time()
print(tempo_fim - tempo_inicio)
print('Melhor genoma:\n',best)
matplotlib.pyplot.plot(time_,fitness_historico)
matplotlib.pyplot.show()
