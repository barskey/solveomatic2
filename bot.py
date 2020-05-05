#sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
#sudo python3 -m pip install --force-reinstall adafruit-blinka
from threading import Thread
from queue import Queue

import time
import json
import calibration
from lookups import MOVES_FOR_SCAN, FACES_STR
#import board
#import neopixel
from adafruit_servokit import ServoKit
import rscube

# led light ring
#light = neopixel.NeoPixel(board.D10, 8)
#light.fill((255, 255, 255))

# thread queues for servo moves
move_queue_a = Queue(maxsize=30)
move_queue_b = Queue(maxsize=30)

# for convenience in referencing array index
tp = {'ccw': 0, 'center': 1, 'cw': 2}
tpk = ['ccw', 'center', 'cw']

# channels on servo pwm board
GRIP_CHANNEL = {'A': 1, 'B': 3}
TWIST_CHANNEL = {'A': 0, 'B': 2}
SLEEP_TIME = 0.5  # time to sleep after sending servo cmd

cube = rscube.MyCube()
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
        kit.servo[TWIST_CHANNEL[g]].set_pulse_width_range(cal.servo_range['twist' + g]['min'], cal.servo_range['twist' + g]['max'])


def init_grippers():
    # move grippers to initial states of load/center
    for g in ['A', 'B']:
        grip(g, 'o')
    for g in ['A', 'B']:
        twist(g, 'center')
    for g in ['A', 'B']:
        grip(g, 'l')


def set_servo_angle(s, a):
    #print('servo:{} angle:{}'.format(s, a))
    kit.servo[s].angle = a
    time.sleep(SLEEP_TIME)


def grip(gripper, cmd):
    """
    Function to open or close gripper
    gripper = 'A' or 'B'
    cmd = 'o' 'c' or 'l' for load
    """
    set_servo_angle(GRIP_CHANNEL[gripper], cal.grip_pos[gripper][cmd])
    grip_state[gripper] = cmd
    print('Grip {}:{}'.format(gripper, cmd))
    return 0, cmd


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
        SUCCESS [2, 'min/max'] calibration move
    """
    other_gripper = 'B' if gripper == 'A' else 'A'
    new_state = None

    if dir == 'min':
        init_servos()  # make sure any new settings have been applied
        print('Twist {}:{}'.format(gripper, 0))
        set_servo_angle(TWIST_CHANNEL[gripper], 0)
        return 2, 'min'
    if dir == 'max':
        init_servos()  # make sure any new settings have been applied
        print('Twist {}:{}'.format(gripper, 180))
        set_servo_angle(TWIST_CHANNEL[gripper], 180)
        return 2, 'max'
    if dir == '-':
        if twist_state[gripper] == 0:
            print('Twist {}:already at min position.'.format(gripper))
            return -1, 'Already at min ccw position.'
        else:
            new_state = twist_state[gripper] - 1
    elif dir == '+':
        if twist_state[gripper] == tpk[-1]:
            print('Twist{}: already at max position.'.format(gripper))
            return -1, 'Already at max cw position.'
        else:
            new_state = twist_state[gripper] + 1
    elif dir in ['ccw', 'center', 'cw']:
        new_state = tp[dir]
    
    if new_state is None:
        print('Twist: Unknown error.')
        return -1, 'Could not twist. Unknown error.'

    if grip_state[gripper] == 'l':  # don't twist if gripper is in load position
        print('Twist {}: Gripper {} in load.'.format(gripper, other_gripper))
        return -1, 'Can\'t twist {}. Gripper {} in {} position.'.format(gripper, other_gripper, grip_state[gripper])
    if grip_state[other_gripper] == 'l':  # don't twist if other gripper is in load position
        print('Twist {}: Gripper {} in {} position.'.format(gripper, other_gripper))
        return -1, 'Can\'t twist {}. Gripper {} currently in load position.'.format(gripper, other_gripper)

    print('Twist {}:{}'.format(gripper, dir))
    set_servo_angle(TWIST_CHANNEL[gripper], cal.twist_pos[gripper][tpk[new_state]])
    twist_state[gripper] = new_state

    # return 0 if this twist moves cube and changes orientation, else return 1
    if grip_state[other_gripper] == 'o':
        cube.set_orientation(gripper, dir)  # update cube orientation since this means it changed
        return 0, dir
    else:
        return 1, dir


def move_gripper(cmd):
    """
    Parses cmd from form of Ao, B-, etc.
    Performs grip or twist accordingly
    """
    gripper = cmd[0]
    dir = cmd[1]
    if dir in ['o', 'c']:
        grip(gripper, dir)
    elif dir in ['-', '+']:
        twist(gripper, dir)


def scan():
    print('Scanning...')
    for face, moves in MOVES_FOR_SCAN.items():
        print('Moving to scan face {}...'.format(FACES_STR[face]))
        for move in moves:
            if len(move) > 0:
                move_gripper(move)
        print("face colors:<something> orientation:{}".format(cube.orientation))
        # TODO capture colors here
        time.sleep(2)


def solve():
    print('Solving...')
    cmds = cube.set_solve_string().split()
    for cmd in cmds:
        face = cmd[0]
        dir = []
        if len(cmd) == 1:  # no direction, hence +
            dir = ['+']
        elif cmd[1] == '\'':  # apostrophe means -
            dir = ['-']
        elif cmd[1] == '2':  # 2 means twist twice
            dir = ['+', '+']
        moves, to_gripper = cube.get_moves_to_twist_face(face)
        print('Moving face {} to gripper {}'.format(face, to_gripper))
        for m in moves:  # perform moves to move face to returned gripper
            move_gripper(m)
        for t in dir:  # twist face
            print('Twisting face {} {}'.format(face, t))
            twist(to_gripper, t)
            grip(to_gripper, 'o')
            twist(to_gripper, '+' if t == '-' else '-')  # TODO can this just be 'center'?
            grip(to_gripper, 'c')


# set up servos and grippers at startup
init_servos()
init_grippers()
