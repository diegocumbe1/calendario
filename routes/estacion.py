from flask import Blueprint, jsonify, render_template

# models
from models.estacionModel import estacionModel

main = Blueprint('estacion_blueprint', __name__)


@main.route('/')
def get_estacion():
    try:
        list_etapa = estacionModel.get_estacion()
        # return jsonify(estaciones)
        response_json = list_etapa.json()
        print(response_json)
        data1 = response_json['fechahora']
        print(data1)
        return render_template('inicio.html', list_etapa=list_etapa)
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
