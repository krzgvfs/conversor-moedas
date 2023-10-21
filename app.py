from flask import Flask, request, jsonify, send_from_directory
import requests
from flask_cors import CORS
from rpyc.utils.server import ThreadedServer

class Cambio:
    def __init__(self) -> None:
        self.API_URL = "https://open.er-api.com/v6/latest"
        self.app = Flask(__name__, static_url_path='', static_folder='.')
        CORS(self.app)

        @self.app.route('/convert', methods=['GET'])
        def convert():
            try:
                de_moeda = request.args.get('de', 'BRL')
                para_moeda = request.args.get('para', 'EUR')
                valor = float(request.args.get('valor', 1))

                # Verifica a taxa de cambio
                response = requests.get(f"{self.API_URL}/{de_moeda}")
                # Registra taxa de cambio em json
                dados = response.json()

                # Conversão
                if 'rates' in dados and para_moeda in dados['rates']:
                    rate = dados['rates'][para_moeda]
                    converter_valor = rate * valor
                    return jsonify({
                        'from': de_moeda,
                        'to': para_moeda,
                        'amount': valor,
                        'converted_amount': converter_valor
                    })
                else:
                    return jsonify({'error': 'Invalid currency or rate not found'}), 400
            except Exception as e:
                return jsonify({'error': str(e)}), 500 # Em caso de erro de servidor

        @self.app.route('/currencies', methods=['GET'])
        def currencies():
            try:
                response = requests.get(f"{self.API_URL}/USD")
                data = response.json()

                if 'rates' in data:
                    return jsonify(list(data['rates'].keys()))
                else:
                    return jsonify({'error': 'Failed to retrieve currencies'}), 500

            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/')
        # Rota padrão
        def index():
            return send_from_directory('.', 'index.html')

if __name__ == '__main__': # Executa apenas se o script for executado diretamente.
    cambio = Cambio() # Instanciando Classe.
    cambio.app.run(debug=True)
