from flask import Flask, request, render_template
import os
import glob
import numpy as np
import tensorflow as tf 
# from keras.preprocessing.image import load_img, img_to_array 
# from pymongo import MongoClient
import psycopg2

app = Flask(__name__)



#----------------------Load Model-------------------------

# modelo = "models/model_DenseNet_50.h5"   
# pesos = "models/weights_DenseNet_50.h5"     
# model = tf.keras.models.load_model(modelo)
# model.load_weights(pesos) 


#----------------------Get Connection Postgres----------------------
conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="postgres",
    user="postgres",
    password="1234")

#----------------------Get Connection Mongo----------------------
"""def get_connection():
    client = MongoClient()
    client = MongoClient('localhost', 27017)
    db = client['AlzheimerIA']
    collection = db['datos_pacientes']
    return collection"""


#--------------------------Make Prediction-----------------
def predict(file):
    
    x = load_img(file, target_size=(longitud, altura))  #A la variable x le vamos a cargar la imagen que queremos predecir
    x = img_to_array(x)     #LA variable x se vuelve un arreglo de valores que representa la imagen
    x = np.expand_dims(x, axis=0)   #En nuestro eje 0 queremos añadir una dimension extra. Esto para poder procesar la informacion sin problema

    arreglo = model.predict(x)    #Predice x y devuelve un arreglo de dos dimensiones ( [[1, 0, 0]] ) el 1 es la prediccion
    resultado = arreglo[0]  #Elegimos la dimension que nos interesa
    respuesta = np.argmax(resultado) 
    
    #print(respuesta)#Trae el indice del valor más alto que traigamos en la lista "resultado"
    
    return None#respuesta
        

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/prediction", methods=["POST"])
def prediction():
    
    #-----------------------Load Image ----------------------
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    image = request.files['inputFile']
    image.save(os.path.join('static/MRImages', image.filename))
    namefile = image.filename
    
    full_filename = glob.glob("static/MRImages/"+namefile)
    full_filename = full_filename[0]
    
    result = predict(full_filename)
    #result = " Alzheimer Disease (AD)"

    """data = {"name":name, "phone":phone, "email":email, "image":namefile, "result":result}
    post = get_connection()
    post.insert_one(data).inserted_id"""
    

    return render_template('predict.html', file=full_filename ,result=result)



if __name__ == '__main__':
    app.run(debug=True)