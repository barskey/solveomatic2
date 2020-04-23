import PySimpleGUI as sg  # Uncomment 1 to run on that framework
import cv2
import json
from vision2 import grab_colors
from lookups import PATTERNS
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
col1 = sg.Column([
    [sg.Frame('Step 1 | Insert cube', [
        [sg.Sizer(200, 1)],
        [btn('GRIP')],
        [btn('SCAN', True)]
    ], pad=(0, 0), element_justification='center')],
    [sg.Frame('Step 2 | Pick a pattern', [
        [sg.Sizer(200, 1)],
        [sg.Button('', image_filename='images/{}'.format(PATTERNS[SOLVETO][0]), border_width=2, key='-SOLVETOBTN-')],
        [sg.Text(SOLVETO, size=(15, 2), font=('Computerfont', 14, ''), justification='center', key='-SOLVETO-')]
    ], pad=(0, 0), element_justification='center')]
], element_justification='center', pad=(0, 0))
col2 = sg.Column([
    [sg.Frame('Step 3 | Go', [
        [sg.Sizer(220, 1)],  # pads col to 210 pix
        [sg.Graph(canvas_size=(160, 160), graph_bottom_left=(0, 0), graph_top_right=(160, 160), key='-GRAPH-')],
        # canvas to display image
        [btn('SOLVE!', True)]
    ], pad=(0, 0), element_justification='center')]
], element_justification='center')
col3 = sg.Column([
    [sg.Text('Insert cube and GRIP to continue...', font=('Computerfont', 18, ''), text_color='yellow', key='-INFO-'),
     sg.Button('Calibrate')]
])
layout = [[col1, col2], [col3]]
window = sg.Window('Solve-O-Matic', layout, size=(480, 320), no_titlebar=True, return_keyboard_events=True)


# ----- Solve To window layout ----- #
def solveto_layout():
    row = []
    cols = 6
    count = 0
    layout = [[sg.Text('Select a pattern to solve to:', font=('Computerfont', 18))]]
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
    col1 = sg.Column([
        [sg.Frame('Gripper A', [
            [cal_btn('open', 'grip-open-A'), cal_btn('<', 'dec-open-A', 1), sg.T('', size=(4, 1), key='openA'), cal_btn('>', 'inc-open-A', 1)],
            [cal_btn('load', 'grip-load-A'), cal_btn('<', 'dec-load-A', 1), sg.T('', size=(4, 1), key='loadA'), cal_btn('>', 'inc-load-A', 1)],
            [cal_btn('close', 'grip-close-A'), cal_btn('<', 'dec-close-A', 1), sg.T('', size=(4, 1), key='closeA'), cal_btn('>', 'inc-close-A', 1)],
            [cal_btn('ccw', 'twist-ccw-A'), cal_btn('<', 'dec-ccw-A', 1), sg.T('', size=(4, 1), key='ccwA'), cal_btn('>', 'inc-ccw-A', 1)],
            [cal_btn('center', 'twist-center-A'), cal_btn('<', 'dec-center-A', 1), sg.T('', size=(4, 1), key='centerA'), cal_btn('>', 'inc-center-A', 1)],
            [cal_btn('cw', 'twist-cw-A'), cal_btn('<', 'dec-cw-A', 1), sg.T('', size=(4, 1), key='cwA'), cal_btn('>', 'inc-cw-A', 1)],
            [cal_btn('min', 'grip-min-A'), cal_btn('<', 'dec-min-A', 1), sg.T('', size=(4, 1), key='minA'), cal_btn('>', 'inc-min-A', 1)],
            [cal_btn('min', 'grip-max-A'), cal_btn('<', 'dec-max-A', 1), sg.T('', size=(4, 1), key='maxA'), cal_btn('>', 'inc-max-A', 1)]
        ])]
    ])
    col2 = sg.Column([
        [sg.Frame('Gripper B', [
            [cal_btn('open', 'grip-open-B'), cal_btn('<', 'dec-open-B', 1), sg.T('', size=(4, 1), key='openB'), cal_btn('>', 'inc-open-B', 1)],
            [cal_btn('load', 'grip-load-B'), cal_btn('<', 'dec-load-B', 1), sg.T('', size=(4, 1), key='loadB'), cal_btn('>', 'inc-load-B', 1)],
            [cal_btn('close', 'grip-close-B'), cal_btn('<', 'dec-close-B', 1), sg.T('', size=(4, 1), key='closeB'), cal_btn('>', 'inc-close-B', 1)],
            [cal_btn('ccw', 'twist-ccw-B'), cal_btn('<', 'dec-ccw-B', 1), sg.T('', size=(4, 1), key='ccwB'), cal_btn('>', 'inc-ccw-B', 1)],
            [cal_btn('center', 'twist-center-B'), cal_btn('<', 'dec-center-B', 1), sg.T('', size=(4, 1), key='centerB'), cal_btn('>', 'inc-center-B', 1)],
            [cal_btn('cw', 'twist-cw-B'), cal_btn('<', 'dec-cw-B', 1), sg.T('', size=(4, 1), key='cwB'), cal_btn('>', 'inc-cw-B', 1)],
            [cal_btn('min', 'grip-min-B'), cal_btn('<', 'dec-min-B', 1), sg.T('', size=(4, 1), key='minB'), cal_btn('>', 'inc-min-B', 1)],
            [cal_btn('min', 'grip-max-B'), cal_btn('<', 'dec-max-B', 1), sg.T('', size=(4, 1), key='maxB'), cal_btn('>', 'inc-max-B', 1)]
        ])]
    ])
    layout = [[col1, col2], [sg.Text('', font=('Computerfont', 14), size=(20, 1), key='-STATUS-'), cal_btn(('Done', '-DONE-'))]]
    return layout


def scan():
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
                    result = new_val
                    window_cal[pos + gripper].update(new_val)
                window_cal['-STATUS-'].update('Result {}:{}'.format(result[0], result[1]))
    elif button == 'GRIP':
        print('Gripping...')
        grip('A', 'l')
        grip('B', 'l')
        window['GRIP'].update(text='UN-GRIP', button_color=('white', 'red'))
        window['SCAN'].update(disabled=False)
    elif button == 'UN-GRIP':
        print('Un-gripping...')
        grip('A', 'o')
        grip('B', 'o')
        window['GRIP'].update(text='UN-GRIP', button_color=('white', 'red'))
        window['SCAN'].update(disabled=False)
    elif button == 'SCAN':
        # TODO perform scan
        print('Scanning...')
        window['SOLVE!'].update(disabled=False)
    elif button == 'SOLVE!':
        # TODO perform solve
        print('Solving...')

    frame = grab_colors()
    img_bytes = cv2.imencode('.png', frame)[1].tobytes()  # Convert the image to PNG Bytes
    window['-GRAPH-'].draw_image(location=(0, 160), data=img_bytes)

window.Close()
