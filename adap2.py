import os
import numpy as np
import cv2 as cv
import argparse

# Função para detectar círculos em uma imagem e retornar o número de círculos detectados e seus raios
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
def process_images_in_folder(folder_path, output_txt_path, param1, param2, min_radius, max_radius):
    # Listar todos os arquivos na pasta
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]

    if not image_files:
        print("Nenhuma imagem .jpg encontrada na pasta.")
        return

    with open(output_txt_path, 'w') as output_file:
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            num_circles, radii = count_circles_in_image(image_path, param1, param2, min_radius, max_radius)
            median_radius = np.median(radii) if radii else 0
            output_file.write(f"{image_file}: {num_circles} círculos encontrados, Mediana do raio: {median_radius}\n")
            print(f"Processado {image_file}: {num_circles} círculos encontrados, Mediana do raio: {median_radius}")

# Configurar o parser de argumentos para receber a pasta de entrada, o arquivo de saída e os parâmetros
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Contar círculos em imagens de uma pasta.")
    parser.add_argument("-i", "--input_folder", required=True, help="Caminho para a pasta contendo as imagens .jpg")
    parser.add_argument("-o", "--output_file", required=True, help="Caminho para o arquivo .txt de saída")
    parser.add_argument("--param1", type=int, required=True, help="Primeiro parâmetro para o detector de círculos (param1)")
    parser.add_argument("--param2", type=int, required=True, help="Segundo parâmetro para o detector de círculos (param2)")
    parser.add_argument("--min_radius", type=int, required=True, help="Raio mínimo dos círculos a serem detectados")
    parser.add_argument("--max_radius", type=int, required=True, help="Raio máximo dos círculos a serem detectados")
    
    args = parser.parse_args()

    input_folder = args.input_folder
    output_file = args.output_file
    param1 = args.param1
    param2 = args.param2
    min_radius = args.min_radius
    max_radius = args.max_radius

    if not os.path.exists(input_folder):
        print("Erro: A pasta especificada não existe.")
    else:
        process_images_in_folder(input_folder, output_file, param1, param2, min_radius, max_radius)