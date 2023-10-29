from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from rpyc.utils.server import ThreadedServer
from cambio import Cambio


class Moedas:
    def __init__(self, moedas_name_dict, moedas_cambio_dict) -> None:
        self.app = Flask(__name__, static_url_path='', static_folder='.')
        CORS(self.app)
        self.moedas_name_dict = moedas_name_dict
        self.moedas_cambio_dict = moedas_cambio_dict


        @self.app.route('/convert', methods=['GET'])
        def convert():
            try:
                fromCurrency = request.args.get('from', 'BRL')
                toCurrency = request.args.get('to', 'EUR')
                amount = float(request.args.get('amount', 1))

                moeda_check1 = fromCurrency + " / " + toCurrency
                moeda_check2 = toCurrency + " / " + fromCurrency 

                # Verifica se as moedas estão no dicionário
                if moeda_check1 in self.moedas_cambio_dict:
                    converter_valor = amount * moedas_cambio_dict[moeda_check1]
                    return jsonify({
                        'from': fromCurrency,
                        'to': toCurrency,
                        'amount': amount,
                        'converted_amount': converter_valor
                    })
                elif moeda_check2 in self.moedas_cambio_dict:
                    converter_valor = amount * moedas_cambio_dict[moeda_check2]
                    return jsonify({
                        'from': fromCurrency,
                        'to': toCurrency,
                        'amount': amount,
                        'converted_amount': converter_valor
                    })
                else:
                    return jsonify({'error': 'Invalid currency or rate not found'}), 400
            except Exception as e:
                return jsonify({'error': str(e)}), 500  # Em caso de erro de servidor




        @self.app.route('/currencies', methods=['GET'])
        def currencies():
            try:
                moedas = list(self.moedas_name_dict.keys())
                return jsonify(moedas)
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/')
        def index():
            return send_from_directory('.', 'index.html')

if __name__ == '__main__': 
    cambio_instancia = Cambio()
    cambio_moedas = cambio_instancia.scraping()

    nm_moedas = {chave.split(' ')[0]: cambio_moedas[chave] for chave in cambio_moedas}

    cambio = Moedas(nm_moedas, cambio_moedas)
    cambio.app.run(debug=True)