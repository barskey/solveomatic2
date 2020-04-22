import json


class Calibration():
    def __init__(self):
        self.load_from_file()
    
    def load_from_file(self):
        caldata = json.load(open('cal.json'))
        self.gripa = caldata['gripa']
        self.gripb = caldata['gripb']
        self.twista = caldata['twista']
        self.twistb = caldata['twistb']
        self.color_limits = caldata['color_limits']

    def get_property(self, prop, param):
        value = None
        if prop == "gripa":
            value = self.gripa[param]
        elif prop == "gripb":
            value = self.gripb[param]
        elif prop == "twista":
            value = self.twista[param]
        elif prop == "twistb":
            value = self.twistb[param]
        elif prop == "color_limits":
            value = self.color_limits[param]
        return value

    def set_property(self, prop, param, value):
        if prop == "gripa":
            self.gripa[param] = value
        elif prop == "gripb":
            self.gripb[param] = value
        elif prop == "twista":
            self.twista[param] = value
        elif prop == "twistb":
            self.twistb[param] = value
        elif prop == "color_limits":
            self.color_limits[param] = value
        self.write_to_file()

    def write_to_file(self):
        data = {
            'gripa': self.gripa,
            'gripb': self.gripb,
            'twista': self.twista,
            'twistb': self.twistb,
            'color_limits': self.color_limits
        }
        with open('app/cal.json', 'w') as outfile:
            json.dump(data, outfile)
