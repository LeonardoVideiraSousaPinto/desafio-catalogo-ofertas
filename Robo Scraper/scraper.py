from selenium import webdriver
from selenium.webdriver.common.by import By
from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float
from sqlalchemy.orm import declarative_base, sessionmaker
import time
import logging
import traceback
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Configuração do log
logging.basicConfig(filename='log.log',level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração do banco de dados
DATABASE_URL = f"postgresql://{os.getenv("LOGIN_SQL")}:{os.getenv("SENHA_SQL")}@localhost:{os.getenv("ROTA_SQL")}/mercado_livre"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Modelo de dados
class Produto(Base):
    __tablename__ = 'produtos'
    link = Column(String, primary_key=True)
    link_imagem = Column(String)
    nome = Column(String)
    valor = Column(Integer)
    valor_com_desc = Column(Integer)
    pcto_desc = Column(Float)
    opcao_parc = Column(String)
    full = Column(Boolean)
    frete_gratis = Column(Boolean)
    loja_oficial = Column(Boolean)

Base.metadata.create_all(engine)

class MercadoLivreScraper:
    def __init__(self, busca):
        logging.info("Iniciando WebDriver")
        self.driver = webdriver.Chrome()
        self.base_url = 'https://lista.mercadolivre.com.br/'
        self.busca = busca
        self.produtos = []

    def buscar_produtos(self):
        logging.info(f"Buscando produtos para: {self.busca}")
        self.driver.get(self.base_url + self.busca)
        qtd_lote = 1
        while True:
            self.driver.get(self.base_url + self.busca + f'_Desde_{qtd_lote}_NoIndex_True')
            if len(self.driver.find_elements(By.CLASS_NAME, 'ui-search-rescue__info')) == 1:
                logging.info("Nenhum produto encontrado.")
                break
            logging.info(f"Extraindo produtos do lote {qtd_lote}")
            self.extrair_produtos()
            qtd_lote += 48
        self.driver.quit()

    def extrair_produtos(self):
        try:
            time.sleep(3)
            produtos_pagina = self.driver.find_elements(By.CLASS_NAME, 'ui-search-result__wrapper')
            for produto in produtos_pagina:
                self.driver.execute_script("arguments[0].scrollIntoView();", produto)
                    
                link_imagem_produto = produto.find_element(By.XPATH, ".//img[contains(@class, 'poly-component__picture')]").get_attribute('src')
                nome_produto = produto.find_element(By.TAG_NAME, 'h3').text

                if len(produto.find_elements(By.CLASS_NAME,'andes-money-amount__discount')) > 0:
                    valores = produto.find_elements(By.XPATH, ".//div[contains(@class, 'poly-component__price') and not(contains(@class, 'poly-component__buy-box'))]")
                    valor_produto =  int(valores[0].find_element(By.CLASS_NAME,'andes-money-amount__fraction').text.replace('.',''))

                    descontos = valores[0].find_elements(By.CLASS_NAME,'andes-money-amount__discount')
                    if len(descontos) > 0:
                        pcto_desconto_produto = int(descontos[0].text.replace('% OFF','')) / 100
                    else:
                        pcto_desconto_produto = 1

                else:
                    valor_produto =  int(produto.find_elements(By.CLASS_NAME,'poly-component__price')[0].find_element(By.CLASS_NAME,'andes-money-amount__fraction').text.replace('.',''))
                    pcto_desconto_produto = 1

                valor_com_desconto_produto =  int(valor_produto - (valor_produto * pcto_desconto_produto))
                pcto_desconto_produto = (0 if pcto_desconto_produto == 1 else pcto_desconto_produto)
                valor_com_desconto_produto = (valor_produto if valor_com_desconto_produto == 0 else valor_com_desconto_produto)
                pcto_desconto_produto = float(f"{pcto_desconto_produto * 100:.2f}")


                opcao_parc_produto = produto.find_element(By.CLASS_NAME,'poly-price__installments').text
                link_produto = produto.find_element(By.XPATH, './/h3/a').get_attribute('href')
                metodo_full_produto = len(produto.find_elements(By.CLASS_NAME, "poly-component__shipped-from")) > 0 
                frete_gratis_produto = len(produto.find_elements(By.CLASS_NAME,'poly-component__shipping')) > 0
                verificado = len(produto.find_elements(By.CLASS_NAME,'poly-component__seller')) > 0
                
                logging.info(f"Produto encontrado: {nome_produto}, R$ {valor_produto}")

                self.produtos.append(Produto(
                    link=link_produto,
                    link_imagem=link_imagem_produto,
                    nome=nome_produto,
                    valor=valor_produto,
                    valor_com_desc=valor_com_desconto_produto,
                    pcto_desc=pcto_desconto_produto,
                    opcao_parc=opcao_parc_produto,
                    full=metodo_full_produto,
                    frete_gratis=frete_gratis_produto,
                    loja_oficial=verificado
                ))
        except:
            logging.error("Erro ocorrido:", exc_info=True)
    def salvar_no_banco(self):
        logging.info("Salvando produtos no banco de dados")
        session.bulk_save_objects(self.produtos)
        session.commit()
        logging.info("Dados salvos com sucesso!")

if __name__ == "__main__":
    busca = 'Computador Gamer i7 16gb ssd 1tb'
    scraper = MercadoLivreScraper(busca)
    scraper.buscar_produtos()
    scraper.salvar_no_banco()
