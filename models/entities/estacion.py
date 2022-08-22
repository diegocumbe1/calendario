from utils.Dateformat import DateFormat


class Estacion():

    def __init__(self, idestacion=None, fechahora=None, temperatura=None,
                 humedadrelativa=None, velviento=None, radiacion=None, precipitacion=None,
                 eto=None, nombre=None, latitud=None, longitud=None, municipio_idmunicipio=None) -> None:
        self.idestacion = idestacion
        self.fechahora = fechahora
        self.temperatura = temperatura
        self.humedadrelativa = humedadrelativa
        self.velviento = velviento
        self.radiacion = radiacion
        self.precipitacion = precipitacion
        self.eto = eto
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.municipio_idmunicipio = municipio_idmunicipio

    def to_JSON(self):
        return {
            'idestacion': self.idestacion,
            'fechahora': DateFormat.convert_date(self.fechahora),
            'temperatura': self.temperatura,
            'humedadrelativa': self.humedadrelativa,
            'velviento': self.velviento,
            'radiacion': self.radiacion,
            'precipitacion': self.precipitacion,
            'eto': self.eto,
            'nombre': self.nombre,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'municipio_idmunicipio': self.municipio_idmunicipio
        }