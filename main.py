import cv2
import threading
import time

def aplicarfiltro(img, tipo_filtro):
    if tipo_filtro == 'gray':
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    elif tipo_filtro == 'blur':
        return cv2.blur(img, (5, 5))
    elif tipo_filtro == 'canny':
        return cv2.Canny(img, 100, 200)

def processar_imagem(img, tipo_filtro, num_threads):
    height, width, _ = img.shape
    resultados = [None] * num_threads
    threads = []

    def aplicar_filtro_em_thread(img, tipo_filtro, thread_index):
        start = time.time()
        resultado = aplicarfiltro(img, tipo_filtro)
        end = time.time()
        print(f"Tempo de processamento da thread {thread_index}: {end - start:.3f} segundos")
        resultados[thread_index] = resultado

    for i in range(num_threads):
        y_start = int(i * height / num_threads)
        y_end = int((i + 1) * height / num_threads)
        thread_img = img[y_start:y_end, :]
        thread = threading.Thread(target=aplicar_filtro_em_thread, args=(thread_img, tipo_filtro, i))
        thread.start()
        threads.append(thread)

    start = time.time()
    for thread in threads:
        thread.join()
    end = time.time()
    print(f"Tempo de processamento total: {end - start:.3f} segundos")

    return cv2.vconcat(resultados)

def main():
    img_path = input("Digite o caminho da imagem: ")
    img = cv2.imread(img_path)

    tipo_filtro = input("Digite o tipo de filtro (gray, blur ou canny): ")

    num_threads = input("Digite o número de threads: ")
    num_threads = int(num_threads)

    resultado = processar_imagem(img, tipo_filtro, num_threads)

    cv2.imshow("Resultado", resultado)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
