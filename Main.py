from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import csv
import time

jobs = []

#Classe responsavel por abrir e fechar o chromdedriver (browser)
s = Service("C:/Users/bruno/Downloads/chromedriver-win64/chromedriver.exe")

#Opcoes de inicializacao
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

#Permite o controle do driver
driver = webdriver.Chrome(service=s, options=options)

#Verificar a altura do scroll
last_height = driver.execute_script("return document.body.scrollHeight")

#Carrega a web page
driver.get("https://www.linkedin.com/jobs/search?keywords=IT&location=Brazil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0")

#Espera para carregar a web page
driver.implicitly_wait(30)


def lista_de_elementos():
    # Encontra elementos no XPATH fornecido e retorna uma lista de WebElements(representa um DOM)
    job_section = driver.find_elements(By.XPATH, '//*[@id="main-content"]/section[2]/ul/li')
    try:
        for job in job_section:
            # Iteracao para achar o titulo, local e link da vaga de emprego
            job_title = job.find_element(By.CSS_SELECTOR, 'h3.base-search-card__title')
            job_location = job.find_element(By.CSS_SELECTOR, 'span.job-search-card__location')
            anchor_tag = job.find_element(By.XPATH, './/div[1]/a | .//a')
            job_link = anchor_tag.get_attribute('href')
            print(job_title.text, job_location.text, job_link)
            # Adiciona a lista
            jobs.append((job_title.text, job_location.text, job_link))

    except Exception as e:
        print("\n Erro ao procurar elemento")
    print("*" * 50)


def scrollar(last_height):
    while True:
        #Scrolla para o ponto mais baixo
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Espera para carregar a web page
        time.sleep(2)

        #Verifica a nova altura e compara com a anterior
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


scrollar(last_height)

"""
while True:
    #Clicar no botao
    clicar = input("Quer clicar no botao?")

    if clicar == "s":
        driver.find_element(By.XPATH, '//button[@aria-label="See more jobs"]').click()
        scrollar(last_height)
    if clicar != "s":
        break
"""

vezes = input("quantas vezes voce quer scrollar?")

for i in range(int(vezes)):
    driver.find_element(By.XPATH, '//button[@aria-label="See more jobs"]').click()
    scrollar(last_height)

#Procurar os elementos e adiciona-los na lista jobs
lista_de_elementos()

#Coloca as informacoes em um CSV
with open('job_links.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Job Location', 'Job Link'])  # Write the header
    for job in jobs:
        writer.writerow(job)

