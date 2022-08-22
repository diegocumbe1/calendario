from Database.db import get_connection
from .entities.estacion import Estacion


class estacionModel():
    @classmethod    
    def get_estacion(self):
        try:
            connection = get_connection()
            estaciones = []
            with connection.cursor() as cursor:
                cursor.execute("SELECT idestacion, fechahora, temperatura, humedadrelativa, velviento, radiacion, precipitacion, eto, nombre, latitud, longitud, municipio_idmunicipio FROM mydb.estacion ORDER BY fechahora DESC LIMIT 10")
                result = cursor.fetchall()
                for row in result:
                    estacion = Estacion(row[0], row[1], row[2], row[3], row[4],
                                        row[5], row[6], row[7], row[8], row[9], row[10], row[11])
                    estaciones.append(estacion.to_JSON())
            connection.close()
            return estaciones
        except Exception as ex:
            raise Exception(ex)
