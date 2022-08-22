from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras

from config import config
# import Database.conexion import

# Routes
from routes import estacion

app = Flask(__name__)
# app.secret_key = "cairocoders-ednalan"

# ENV = 'dev'

# if ENV == 'dev':
#     app.debug = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/mydb'
# else:
#     app.debug = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = ''
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db= SQLAlchemy(app)

# class Feedback(db.Model):
#     __tablename__ = 'feedback'
#     id = db.Column(db.Integer, primary_key=True)


DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "123456"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                        password=DB_PASS, host=DB_HOST)
# app.config['SQLALCHEMY_DATABASE_URI'] = ''
# db= SQLAlchemy(app)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
s = "SELECT * FROM mydb.estacion ORDER BY fechahora DESC LIMIT 10"
cursor.execute(s)  # execute SQL
list_etapa = cursor.fetchall()


@app.route('/', methods=['GET'])
def inicio():
    # data = list_etapa.query.filter().paginate(page=1, per_page=10)
    print(list_etapa)
    return render_template('inicio.html', list_etapa=list_etapa)


@app.route('/ETr')
def ETr():

    return render_template('ETr.html', list_etapa=list_etapa)


@app.route('/Kc')
def Kc():

    return render_template('Kc.html', list_etapa=list_etapa)


@app.route('/ET')
def ET():

    return render_template('ET.html', list_etapa=list_etapa)


@app.route('/DAS')
def DAS():

    return render_template('DAS.html', list_etapa=list_etapa)


@app.route('/Pr')
def Pr():

    return render_template('Pr.html', list_etapa=list_etapa)


@app.route('/NAP')
def NAP():

    return render_template('NAP.html', list_etapa=list_etapa)


@app.route('/Nb')
def Nb():

    return render_template('Nb.html', list_etapa=list_etapa)


def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.config.from_object(config['development'])

    # Blueprint
    app.register_blueprint(estacion.main, url_prefix='/estacion')

    # Error Handler
    app.errorhandler(404)(page_not_found)
    app.run(debug=True)
