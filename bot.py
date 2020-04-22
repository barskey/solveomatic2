import time
import json
import calibration
from adafruit_servokit import ServoKit

# for convenience in referencing array index
tp = {'ccw': 0, 'center': 1, 'cw': 2}
tpk = ['ccw', 'center', 'cw']

# channels on servo pwm board
GRIP_CHANNEL = {'A': 1, 'B': 3}
TWIST_CHANNEL = {'A': 0, 'B': 2}
SLEEP_TIME = 0.1  # time to sleep after sending servo cmd

cube = None
kit = ServoKit(channels=8)
scan_index = 0
# grip_state is letter o, c, or l
grip_state = {'A': 'o', 'B': 'o'}
# twist_state is int ccw:0, center:1, cw:2
twist_state = {'A': tp['center'], 'B': tp['center']}

cal = calibration.Calibration()


def init_servos():
    # initialize servo pulse ranges
    for g in ['A', 'B']:
        kit.servo[GRIP_CHANNEL[g]].set_pulse_width_range(cal.servo_range['grip' + g]['min'], cal.servo_range['grip' + g]['max'])
        kit.servo[GRIP_CHANNEL[g]].set_pulse_width_range(cal.servo_range['twist' + g]['min'], cal.servo_range['twist' + g]['max'])


def init_grippers():
    # move grippers to initial states of load/center
    for g in ['A', 'B']:
        grip(g, 'l')
        twist(g, 'center')


def set_servo_angle(s, a):
    print(s,a)
    kit.servo[s].angle = a


def grip(gripper, cmd):
    """
    Function to open or close gripper
    gripper = 'A' or 'B'
    cmd = 'o' 'c' or 'l' for load
    """
    set_servo_angle(GRIP_CHANNEL[gripper], cal.grip_pos[gripper][cmd])
    time.sleep(SLEEP_TIME)
    grip_state[gripper] = cmd
    return [0, cmd]


def twist(gripper, dir):
    """
    Function to twist gripper, either twisting face or rotating cube
    gripper = 'A' or 'B'
    dir = 'min' or 'max'
    dir = '+' 90-deg CW, '-' 90-deg CCW
    dir = 'ccw', 'center', 'cw' sets to that position
    returns
        ERROR [-1, 'error msg'] no move or twist
        SUCCESS [0, 'dir'] twisted cube
        SUCCESS [1, 'dir'] twisted face
    """
    other_gripper = 'B' if gripper == 'A' else 'A'
    new_state = None

    if dir == 'min':
        set_servo_angle(TWIST_CHANNEL[gripper], 0)
        return [2, 'min']
    if dir == 'max':
        set_servo_angle(TWIST_CHANNEL[gripper], 180)
        return [2, 'max']
    if dir == '-':
        if twist_state[gripper] == 0:
            return [-1, 'Already at min ccw position.']
        else:
            new_state = twist_state[gripper] - 1
    elif dir == '+':
        if twist_state[gripper] == len(twist_state[gripper]) - 1:
            return [-1, 'Already at max cw position.']
        else:
            new_state = twist_state[gripper] + 1
    elif dir in ['ccw', 'center', 'cw']:
        new_state  = tp[dir]
    
    if new_state is None:
        return [-1, 'Could not twist. Unknown error.']

    if grip_state[gripper] == 'l': # don't twist if gripper is in load position
        return [-1, 'Can\'t twist {}. Gripper {} currently in {} position.'.format(gripper, other_gripper, grip_state[gripper])]
    if grip_state[other_gripper] == 'l': # don't twist if other gripper is in load position
        return [-1, 'Can\'t twist {}. Gripper {} currently in load position.'.format(gripper, other_gripper)]

    set_servo_angle(TWIST_CHANNEL[gripper], cal.twist_pos[gripper][new_state])
    time.sleep(SLEEP_TIME)
    twist_state[gripper] = new_state
    return [0 if grip_state[other_gripper] == 'o' else 1, dir]  # return 0 if this twist moves cube and changes orientation, else return 1
"""
def scan_move():
    if _scan_index >= len(MOVES_FOR_SCAN):
        return 'Done!'

    for move in MOVES_FOR_SCAN[_scan_index]:
        if len(move) > 0:
            gripper = move[0]
            cmd = move[1]
            if cmd in ['+', '-']:
                result = twist(gripper, cmd)
                if result[0] == 0:
                    _cube.set_orientation(gripper, cmd)
            elif cmd in ['o', 'c', 'l']:
                result = grip(gripper, cmd)
    _scan_index = _scan_index + 1
    return [0, 'Move done']
"""
# set up servos and grippers at startup
init_servos()
init_grippers()
