import json


class Calibration:
    grip_pos = {
        'A': {'o': 0, 'c': 0, 'l': 0},
        'B': {'o': 0, 'c': 0, 'l': 0}
    }
    twist_pos = {
        'A': {'ccw': 0, 'center': 0, 'cw': 0},
        'B': {'ccw': 0, 'center': 0, 'cw': 0}
    }
    servo_range = {
        'gripA': {'min': 520, 'max': 2450},
        'gripB': {'min': 750, 'max': 2250},
        'twistA': {'min': 750, 'max': 2250},
        'twistB': {'min': 680, 'max': 2410}
    }
    color_limits = {
        "sat_W": 0.2,
        "val_W": 0.59,
        "orange_L": 0.02,
        "orange_H": 0.09,
        "yellow_H": 0.2,
        "green_H": 0.39,
        "blue_H": 0.62
    }

    def __init__(self):
        self.load_from_file()
    
    def load_from_file(self):
        caldata = json.load(open('cal.json'))
        self.grip_pos = caldata['grip_pos']
        self.twist_pos = caldata['twist_pos']
        self.servo_range = caldata['servo_range']
        self.color_limits = caldata['color_limits']

    def set_property(self, prop, gripper, param, value):
        new_val = 0
        if prop == "grip_pos":
            new_val = self.grip_pos[gripper][param[0]] + value
            if 0 <= new_val <= 180:
                self.grip_pos[gripper][param[0]] = new_val
            else:
                return self.grip_pos[gripper][param[0]]
        elif prop == "twist_pos":
            new_val = self.twist_pos[gripper][param] + value
            if 0 <= new_val <= 180:
                self.twist_pos[gripper][param] = new_val
            else:
                return self.twist_pos[gripper][param]
        elif prop == "servo_range":
            new_val = self.servo_range['twist' + gripper][param] + value
            if new_val > 0:
                self.servo_range['twist' + gripper][param] = new_val
            else:
                return self.servo_range['twist' + gripper][param]
        elif prop == "color_limits":
            new_val = self.color_limits[param] + value
            if 0 <= new_val <= 1:
                self.color_limits[param] = new_val
            else:
                return self.color_limits[param]
        self.write_to_file()
        return new_val

    def write_to_file(self):
        data = {
            'grip_pos': self.grip_pos,
            'twist_pos': self.twist_pos,
            'servo_range': self.servo_range,
            'color_limits': self.color_limits
        }
        with open('cal.json', 'w') as outfile:
            json.dump(data, outfile)
