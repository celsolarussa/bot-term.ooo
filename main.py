import random
import string
import re
from time import sleep
from unidecode import unidecode
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = 'https://term.ooo/'

with open('novas_palavras.txt', 'r') as f:
    palavras_str = f.read()
    palavras = palavras_str.split(' ')

options = Options()
options.add_argument('--start-maximized')
driver = Remote(command_executor='http://127.0.0.1:4444/wd/hub', options=options)

driver.get(url)

pagina_ajuda = 'help'
primeira_letra = '//*[@id="board"]/div[1]/div[1]'
enter = 'kbd_enter'
boardarea = '//*[@id="board"]/div[?]'
letters = '//*[@id="board"]/div[?]/div[?]'

letras_posicao_correta = {}
letras_posicao_errada = {}
letras_erradas = {}

WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, pagina_ajuda))).click()

for linha in range(1, 7):
    palavra = unidecode(random.choice(palavras))

    for coluna, letra in zip(range(1, 6), palavra):
        driver.find_element_by_xpath(f'//*[@id="board"]/div[{linha}]/div[{coluna}]').send_keys(letra)
    driver.find_element_by_id(enter).click()
    palavras.remove(palavra)
    sleep(0.2)
    for coluna in range(1, 6):
        elemento = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, f'//*[@id="board"]/div[{linha}]/div[{coluna}]')))
        WebDriverWait(driver, 1).until(lambda x:  elemento.get_attribute('aria-label'))
        resultado = elemento.get_attribute('aria-label')
        elemento = unidecode(elemento.text.lower())
        print(elemento)
        posicao = coluna - 1
        if 'outro local' in resultado:
            letras_posicao_errada[posicao] = elemento
            palavras = list(filter(lambda x: elemento in x and x[posicao] != elemento, palavras.copy()))
        elif 'correta' in resultado:
            letras_posicao_correta[posicao] = elemento
            palavras = list(filter(lambda x: x[posicao] == elemento, palavras.copy()))
        elif 'errada' in resultado:
            letras_erradas[posicao] = elemento
            # letras_erradas.append([elemento, coluna])
    for posicao, letra in letras_erradas.items():
        if letra not in letras_posicao_correta.values() and letra not in letras_posicao_errada.values():
            palavras = list(filter(lambda x: letra not in x, palavras.copy()))
        else:
            quantidade = len([value for value in letras_posicao_correta.values() if value == letra])
            if quantidade:
                palavras = list(filter(lambda x: x.count(letra) == quantidade, palavras.copy()))
                # letras = string.ascii_letters
                # index = 25 if letra == 'z' else letras.index(letra) + 1
                # prox = letras[index]
                # aux = [f'[{prox}-z]'] * 5
                # aux[list(letras_posicao_correta.keys())[list(letras_posicao_correta.values()).index(letra)]] = f'{letra}'
                # pattern = ''.join(aux)
                # comp = re.compile(pattern)
                # palavras = list(filter(comp.match, palavras.copy()))
    print(f'{linha} - {palavra}, {palavras}')
breakpoint()
driver.quit()


