import requests
from bs4 import BeautifulSoup

class Cambio:
    def __init__(self) -> None:
        self.url = 'https://www.google.com/finance/markets/currencies'
        self.response = requests.get(self.url)

    def scraping(self):
        if self.response.status_code == 200:
            soup = BeautifulSoup(self.response.text, 'html.parser')

            # Captura o conteúdo
            moedas_class = "ZvmM7"
            cambio_class = "Bu4oXd"

            moedas_elements = soup.find_all(class_=moedas_class)
            cambio_elements = soup.find_all(class_=cambio_class)

            moedas_cambio_dict = {}

            for moeda_element, cambio_element in zip(moedas_elements, cambio_elements):
                moeda = moeda_element.text
                cambio_text = cambio_element.text.replace(',', '')
                valor_cambio = float(cambio_text)
                moedas_cambio_dict[moeda] = valor_cambio
                
            return moedas_cambio_dict
        else:
            print("Falha na solicitação HTTP. Código de status:", self.response.status_code)
            return None
