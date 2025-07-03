class WeatherInfo:
    def __init__(self, ville, pays, temperature, condition, vent, latitude=None, longitude=None):
        self.ville = ville
        self.pays = pays
        self.temperature = temperature
        self.condition = condition
        self.vent = vent
        self.latitude = latitude
        self.longitude = longitude 