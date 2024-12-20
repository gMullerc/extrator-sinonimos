import PyPDF2
import re
import csv

def extrair_sinonimos_intervalo(arquivo_pdf, inicio_pagina, fim_pagina):
    with open(arquivo_pdf, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        resultados = {}
        for numero_pagina in range(inicio_pagina, fim_pagina + 1):
            texto_pagina = leitor_pdf.pages[numero_pagina - 1].extract_text()
            texto_pagina = re.sub(r'\b([A-ZÇÃÕÂÊÍÓÚ]+)-\n([A-ZÇÃÕÂÊÍÓÚ]+)\b', r'\1\2', texto_pagina)
            texto_pagina = re.sub(r'-\n', '', texto_pagina)
            padrao = re.compile(r'(\d+)\s+([A-ZÇÃÕÂÊÍÓÚ]+),\s*([^\.]+)\.', re.MULTILINE)
            correspondencias = padrao.findall(texto_pagina)
            for _, palavra, sinonimos in correspondencias:
                palavra_limpa = palavra.strip()
                sinonimos_limpos = re.sub(r'\([^\)]*\)', '', sinonimos.strip())
                sinonimos_limpos = re.sub(r'\s+|\n', ' ', sinonimos_limpos).replace(';', ',')
                resultados[palavra_limpa] = sinonimos_limpos.strip()
        return resultados

if __name__ == "__main__":    
    caminho_arquivo = "cams-10-dicionario_de_sinonimos_da_lingua_portuguesa-para_internet (2).pdf"
    inicio_pagina = 12
    fim_pagina = 490
    resultado = extrair_sinonimos_intervalo(caminho_arquivo, inicio_pagina, fim_pagina)
    with open("sinonimos.csv", "w", newline="", encoding="utf-8") as csvfile:
        escritor_csv = csv.writer(csvfile)
        escritor_csv.writerow(["Palavra", "Sinônimos"])
        for palavra, sinonimos in resultado.items():
            escritor_csv.writerow([palavra, sinonimos])
    print("Extração concluída. Arquivo 'sinonimos.csv' criado.")
