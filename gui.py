import PySimpleGUI as sg  # Uncomment 1 to run on that framework
import vision_params
from lookups import PATTERNS, MOVES_FOR_SCAN
from bot import *

# ----- Globals ----- #
SOLVETO = 'Solid Cube'

# ----- Window setup ----- #
sg.theme('Dark Grey')
# sg.set_options(element_padding=(0, 0))
title = sg.Text('Solve-O-Matic!')


def btn(name, state=False):
    return sg.Button(name, size=(11, 1), disabled=state)


# ----- User Input window layout ----- #
col1 = sg.Col([
    [sg.Frame('Step 1 | Insert cube', [
        [sg.Sizer(200, 1)],
        [sg.Button('GRAB', size=(11, 1), key='-GRAB-')],
        [btn('SCAN', True)]
    ], pad=(0, 0), element_justification='center')],
    [sg.Frame('Step 2 | Pick a pattern', [
        [sg.Sizer(200, 1)],
        [sg.Button('', image_filename='images/{}'.format(PATTERNS[SOLVETO][0]), border_width=2, key='-SOLVETOBTN-')],
        [sg.T(SOLVETO, size=(15, 2), font=('Computerfont', 14, ''), justification='center', key='-SOLVETO-')]
    ], pad=(0, 0), element_justification='center')]
], element_justification='center', pad=(0, 0))
col2 = sg.Col([
    [sg.Frame('Step 3 | Go', [
        [sg.Sizer(220, 1)],  # pads col to 220 pix
        [sg.Graph(canvas_size=(160, 160), graph_bottom_left=(0, 0), graph_top_right=(160, 160), key='-GRAPH-')],
        [btn('SOLVE!', True)]
    ], pad=(0, 0), element_justification='center')]
], element_justification='center')
col3 = sg.Col([
    [sg.T('Insert cube and GRAB to continue...', font=('Computerfont', 18, ''), text_color='yellow', key='-INFO-')],
    [sg.Sizer(200, 1), sg.Button('Calibrate'), sg.Button('Colors')]
])
layout = [[col1, col2], [col3]]
window = sg.Window('Solve-O-Matic', layout, size=(480, 320), no_titlebar=True, return_keyboard_events=True)


# ----- Solve To window layout ----- #
def solveto_layout():
    row = []
    cols = 6
    count = 0
    layout = [[sg.T('Select a pattern to solve to:', font=('Computerfont', 18))]]
    for p, l in PATTERNS.items():
        if not count % cols:
            layout += [row]
            row = []
        row += [sg.Button('', image_filename='images/{}'.format(l[0]), border_width=0, key=p)]
        count += 1
    if row:
        layout += [row]
    return layout


def cal_btn(name, key, wid=5):
    return sg.Button(name, size=(wid, 1), key=key)


# ----- Calibration window layout ----- #
def cal_layout():
    col1 = sg.Col([
        [sg.Frame('Gripper A', [
            [cal_btn('Open', 'grip-open-A'), cal_btn('<', 'dec-open-A', 1), sg.T(cal.grip_pos['A']['o'], size=(4, 1), key='openA'), cal_btn('>', 'inc-open-A', 1)],
            [cal_btn('Load', 'grip-load-A'), cal_btn('<', 'dec-load-A', 1), sg.T(cal.grip_pos['A']['l'], size=(4, 1), key='loadA'), cal_btn('>', 'inc-load-A', 1)],
            [cal_btn('Close', 'grip-close-A'), cal_btn('<', 'dec-close-A', 1), sg.T(cal.grip_pos['A']['c'], size=(4, 1), key='closeA'), cal_btn('>', 'inc-close-A', 1)],
            [cal_btn('CCW', 'twist-ccw-A'), cal_btn('<', 'dec-ccw-A', 1), sg.T(cal.twist_pos['A']['ccw'], size=(4, 1), key='ccwA'), cal_btn('>', 'inc-ccw-A', 1)],
            [cal_btn('Center', 'twist-center-A'), cal_btn('<', 'dec-center-A', 1), sg.T(cal.twist_pos['A']['center'], size=(4, 1), key='centerA'), cal_btn('>', 'inc-center-A', 1)],
            [cal_btn('CW', 'twist-cw-A'), cal_btn('<', 'dec-cw-A', 1), sg.T(cal.twist_pos['A']['cw'], size=(4, 1), key='cwA'), cal_btn('>', 'inc-cw-A', 1)],
            [cal_btn('Min', 'twist-min-A'), cal_btn('<', 'dec-min-A', 1), sg.T(cal.servo_range['twistA']['min'], size=(4, 1), key='minA'), cal_btn('>', 'inc-min-A', 1)],
            [cal_btn('Max', 'twist-max-A'), cal_btn('<', 'dec-max-A', 1), sg.T(cal.servo_range['twistA']['max'], size=(4, 1), key='maxA'), cal_btn('>', 'inc-max-A', 1)]
        ])]
    ])
    col2 = sg.Col([
        [sg.Frame('Gripper B', [
            [cal_btn('Open', 'grip-open-B'), cal_btn('<', 'dec-open-B', 1), sg.T(cal.grip_pos['B']['o'], size=(4, 1), key='openB'), cal_btn('>', 'inc-open-B', 1)],
            [cal_btn('Load', 'grip-load-B'), cal_btn('<', 'dec-load-B', 1), sg.T(cal.grip_pos['B']['l'], size=(4, 1), key='loadB'), cal_btn('>', 'inc-load-B', 1)],
            [cal_btn('Close', 'grip-close-B'), cal_btn('<', 'dec-close-B', 1), sg.T(cal.grip_pos['B']['c'], size=(4, 1), key='closeB'), cal_btn('>', 'inc-close-B', 1)],
            [cal_btn('CCW', 'twist-ccw-B'), cal_btn('<', 'dec-ccw-B', 1), sg.T(cal.twist_pos['B']['ccw'], size=(4, 1), key='ccwB'), cal_btn('>', 'inc-ccw-B', 1)],
            [cal_btn('Center', 'twist-center-B'), cal_btn('<', 'dec-center-B', 1), sg.T(cal.twist_pos['B']['center'], size=(4, 1), key='centerB'), cal_btn('>', 'inc-center-B', 1)],
            [cal_btn('CW', 'twist-cw-B'), cal_btn('<', 'dec-cw-B', 1), sg.T(cal.twist_pos['B']['cw'], size=(4, 1), key='cwB'), cal_btn('>', 'inc-cw-B', 1)],
            [cal_btn('Min', 'twist-min-B'), cal_btn('<', 'dec-min-B', 1), sg.T(cal.servo_range['twistB']['min'], size=(4, 1), key='minB'), cal_btn('>', 'inc-min-B', 1)],
            [cal_btn('Max', 'twist-max-B'), cal_btn('<', 'dec-max-B', 1), sg.T(cal.servo_range['twistB']['max'], size=(4, 1), key='maxB'), cal_btn('>', 'inc-max-B', 1)]
        ])]
    ])
    layout = [
        [col1, col2],
        [sg.Text('', font=('Computerfont', 14), size=(20, 1), key='-STATUS-')],
        [cal_btn('Done', '-DONE-')]
    ]
    return layout


# ----- Colors window layout ----- #
def colors_layout():
    rows = []
    for param, val in cal.color_limits.items():
        rows += [[sg.T(param, size=(8, 1)), cal_btn('<', 'dec-' + param, 1), sg.T(val, size=(4, 1), key=param), cal_btn('>', 'inc-' + param, 1)]]
    col1 = sg.Col(rows)
    col2 = sg.Col([
        [sg.Sizer(220, 1)],  # pads col to 220 pix
        [sg.Graph(canvas_size=(160, 160), graph_bottom_left=(0, 0), graph_top_right=(160, 160), key='-GRAPH-')]
    ], element_justification='center')
    layout = [
        [col1, col2],
        [cal_btn('Done', '-DONE-')]
    ]
    return layout


def scan():
    for face, moves in MOVES_FOR_SCAN.items():
        print('Scanning face {}...'.format(face))
        for move in moves:
            if len(move) > 0:
                g = move[0]
                c = move[1]
                if c in ['+', '-']:
                    r = twist(g, c)
                    print("Result:{}, {}".format(r[0], r[1]))
                    #if r[0] == 0:
                        #_cube.set_orientation(g, c)
                elif c in ['o', 'c', 'l']:
                    r = grip(g, c)
                    print("Result:{}, {}".format(r[0], r[1]))
        print("face colors:<something>")
        # TODO capture colors here
        time.sleep(2)


def solve():
    # TODO make solve function
    pass


# ----- Event LOOP Read and display frames, operate the GUI ----- #
while True:
    button, values = window.read(timeout=50)
    if button in (None, 'Quit', 'Escape:9'):
        break
    elif button == '-SOLVETOBTN-':
        window_solveto = sg.Window('Solve To', solveto_layout(), size=(480, 320), no_titlebar=True, return_keyboard_events=True)
        solvebtn, solvevals = window_solveto.read(close=True)
        SOLVETO = solvebtn
        window['-SOLVETO-'].update(SOLVETO)
        window['-SOLVETOBTN-'].update(image_filename='images/{}'.format(PATTERNS[SOLVETO][0]))
    elif button == 'Calibrate':
        window_cal = sg.Window('Solve-O-Matic', cal_layout(), size=(480, 320), no_titlebar=True, return_keyboard_events=True)
        while True:
            calbtn, calvals = window_cal.read(timeout=50)
            if calbtn in (None, '-DONE-', 'Escape:9'):
                window_cal.Close()
                break
            elif calbtn != '__TIMEOUT__':
                result = ''
                cmd,pos,gripper = calbtn.split('-')
                if cmd == 'grip':
                    result = grip(gripper, pos[0])
                elif cmd == 'twist':
                    result = twist(gripper, pos)
                elif cmd in ('inc', 'dec'):
                    val = 1 if cmd == 'inc' else -1
                    prop = ''
                    if pos in ['open', 'load', 'close']:
                        prop = 'grip_pos'
                    elif pos in ['ccw', 'center', 'cw']:
                        prop = 'twist_pos'
                    elif pos in ['min', 'max']:
                        prop = 'servo_range'
                        val *= 10
                    new_val = cal.set_property(prop, gripper, pos, val)
                    result = ['Success', new_val]
                    window_cal[pos + gripper].update(new_val)
                window_cal['-STATUS-'].update('Result {}:{}'.format(result[0], result[1]))
    elif button == 'Colors':
        window_colors = sg.Window('Solve-O-Matic', colors_layout(), size=(480, 320), no_titlebar=True, return_keyboard_events=True)
        while True:
            colbtn, colvals = window_colors.read(timeout=50)
            if colbtn in (None, '-DONE-', 'Escape:9'):
                window_colors.Close()
                break
            elif colbtn != '__TIMEOUT__':
                cmd,param = colbtn.split('-')
                val = 0.01 if cmd == 'inc' else -0.01
                new_val = cal.set_property(None, None, param, val)
                window_colors[param].update(new_val)

            window_colors['-GRAPH-'].draw_image(location=(0, 160), data=vision_params.img_bytes)

    elif button == '-GRAB-':
        if button.button_text == 'GRAB':
            print('Gripping...')
            grip('A', 'c')
            grip('B', 'c')
            window['-GRAB-'].update(text='UN-GRAB', button_color=('white', 'red'))
            window['SCAN'].update(disabled=False)
        elif button.button_text == 'UN-GRAB':
            print('Un-gripping...')
            grip('A', 'o')
            grip('B', 'o')
            window['-GRIP-'].update(text='UN-GRAB', button_color=('white', 'red'))
            window['SCAN'].update(disabled=True)
    elif button == 'SCAN':
        print('Scanning...')
        scan()
        window['SOLVE!'].update(disabled=False)
    elif button == 'SOLVE!':
        print('Solving...')
        solve()
    #print(vision_params.img_bytes)
    window['-GRAPH-'].draw_image(location=(0, 160), data=vision_params.img_bytes)

window.Close()
