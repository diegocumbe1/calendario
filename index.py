from flask import Flask, render_template
# from flask_sqlalchemy import SQLAlchemy
# from flask_paginate import Pagination, get_page_args,
# import numpy as np
import psycopg2
import psycopg2.extras
import datetime
import sqlite3
from decouple import config
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

import os

from config import config

# database connection
from Database.db import get_connection
model_path = "./modelo/LSTM_Riego"
model = tf.keras.models.load_model(model_path)

app = Flask(__name__)

connection = get_connection()
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


@app.route('/', methods=['GET'])
@app.route('/inicio/page/<int:page>')
def inicio(page=1):
   
    # return render_template('inicio.html', list_etapa=list_etapa)
    try:
    # page,per_page,offset = get_page_args(page_parameters="page",per_page_parameters="per_page")
        # estacion_data = "SELECT * FROM mydb.estacion  ORDER BY fechahora DESC limit %s offset %s"
        # limit = 20
        # offset = page
        estacion_data = "SELECT * FROM mydb.estacion  ORDER BY fechahora DESC limit 1000 offset 0"
        
        # paginate = estacion_data.query.paginate(limit=limit, offset=offset)
        # print('limit -->',limit) 
        # print('paginate: ', paginate)
        # cursor.execute(estacion_data ,(limit,offset))  # execute SQL
        cursor.execute(estacion_data)  # execute SQL

        list_etapa = cursor.fetchall()
        # print('fecha inicio',list_etapa)
        # data = list_etapa.query.filter().paginate(page=1, per_page=10)
        # print('listado estacion',list_etapa)
        # print('eto -->',listado_eto) 
            # estacion_data = mydb.estacion.query.order_by(
            #    mydb.estacion.fechahora.desc()
            # ).paginate(page, per_page=USERS_PER_PAGE)
    except sqlite3.OperationalError:
        flash("No users in the database.")
        list_etapa = None

    return render_template(
        'inicio.html',
        list_etapa=list_etapa,
        page=page,
        route='inicio/page'
    )


@app.route('/ETr')
def ETr():
    fecha_eto = "SELECT fechahora,eto FROM mydb.estacion  ORDER BY fechahora DESC limit 1000 offset 0"
    cursor.execute(fecha_eto, (10,))
    list_fecha_eto = cursor.fetchall()
    return render_template('ETr.html', list_etapa=list_fecha_eto)


@app.route('/Kc')
def Kc():

    fecha_kc = "SELECT fechahora,radiacion FROM mydb.estacion  ORDER BY fechahora DESC limit 1000 offset 0"
    cursor.execute(fecha_kc, (10,))
    list_fecha_kc = cursor.fetchall()
    return render_template('Kc.html', list_etapa=list_fecha_kc)


@app.route('/ET')
def ET():
    fecha_kc = "SELECT fechahora,radiacion FROM mydb.estacion  ORDER BY fechahora DESC limit 1000 offset 0"
    cursor.execute(fecha_kc, (10,))
    list_etapa = cursor.fetchall()
    return render_template('ET.html', list_etapa=list_etapa)


@app.route('/Temperatura')
def DAS():

    fecha_tem = "SELECT fechahora,temperatura FROM mydb.estacion  ORDER BY fechahora DESC limit 1000 offset 0"
    cursor.execute(fecha_tem, (10,))
    list_fecha_tem = cursor.fetchall()
    return render_template('DAS.html', list_etapa=list_fecha_tem)


@app.route('/Pr')
def Pr():
    fecha_kc = "SELECT fechahora,radiacion FROM mydb.estacion  ORDER BY fechahora DESC limit 1000 offset 0"
    cursor.execute(fecha_kc, (10,))
    list_etapa = cursor.fetchall()
    return render_template('Pr.html', list_etapa=list_etapa)


@app.route('/NAP')
def NAP():

    fecha_kc = "SELECT fechahora,radiacion FROM mydb.estacion  ORDER BY fechahora DESC limit 1000 offset 0"
    cursor.execute(fecha_kc, (10,))
    list_etapa = cursor.fetchall()    
    return render_template('NAP.html', list_etapa=list_etapa)


@app.route('/Nb')
def Nb():
    fecha_kc = "SELECT fechahora,radiacion FROM mydb.estacion  ORDER BY fechahora DESC limit 1000 offset 0"
    cursor.execute(fecha_kc, (10,))
    list_etapa = cursor.fetchall()
    return render_template('Nb.html', list_etapa=list_etapa)


def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), 0]
		dataX.append(a)
		dataY.append(dataset[i + look_back, 0])
	return np.array(dataX), np.array(dataY)
 
def get_next_7_days(new_data):

  look_back = 30
  scaler = MinMaxScaler(feature_range=(0, 1))
  scaler.fit_transform(new_data)
  input_data, _ = create_dataset(new_data, look_back)
  input_data = np.reshape(input_data, (input_data.shape[0], input_data.shape[1], 1))
  pred = model.predict(input_data)
  pred = scaler.inverse_transform(pred)
  pred = [round(x[0],2 )for x in pred]

  return pred

@app.route('/prediction')
def predict():

    fecha_eto = "SELECT fechahora,eto FROM mydb.estacion  ORDER BY fechahora DESC LIMIT %s"
    cursor.execute(fecha_eto, (38,))
    dato_enviar = cursor.fetchall()   
    #print(respuesta)#Trae el indice del valor más alto que traigamos en la lista "resultado"
    #retormar la prediccion de los siguientes 7 dias
    dato_enviar = [i[1] for i in dato_enviar ]
    





#--------------------------get Prediction-----------------

    # prediccion_eto = [ 2.3, 2.2, 2.3 ,2.4, 2.9, 2.0 ,4.0] # obetener del modelo
    kc = 0.45 #  deberia variar
    dataIn = np.array(dato_enviar)
    dataIn = dataIn.reshape(dataIn.shape[0], 1)
    pred = get_next_7_days(dataIn)
    
    
    start = datetime.datetime.today()
    start = start.replace(microsecond=0)
    periods = 7
    daterange = []
    for i,day in enumerate(range(periods)):
        date = (start + datetime.timedelta(days = day))
        daterange.append([date,pred[i],round(pred[i] *kc,2)])
    return render_template('ETr_predict.html', list_etapa=daterange)


def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.config.from_object(config['development'])

    # Error Handler
    app.errorhandler(404)(page_not_found)
    port = int(os.getenv('PORT',5000))
    print("Starting app on port %d" % port)

    app.run(host='0.0.0.0', port=port)
    cursor.close()

