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


def cal_btn(name, key):
    return sg.Button(name, size=(5, 1), key=key)


# ----- Calibration window layout ----- #
def cal_layout():
    col1 = sg.Column([
        [sg.Frame('Gripper A', [
            [cal_btn('Open', 'grip-OPEN-A'), cal_btn('<', 'DEC-OPEN-A'), sg.Text('', size=(2, 1), key='OPENA'), cal_btn('>', 'INC-OPEN-A')],
            [cal_btn('Load', 'grip-LOAD-A'), cal_btn('<', 'DEC-LOAD-A'), sg.Text('', size=(2, 1), key='LOADA'), cal_btn('>', 'INC-LOAD-A')],
            [cal_btn('Close', 'grip-CLOSE-A'), cal_btn('<', 'DEC-CLOSE-A'), sg.Text('', size=(2, 1), key='CLOSEA'), cal_btn('>', 'INC-CLOSE-A')],
            [cal_btn('CCW', 'twist-CCW-A'), cal_btn('<', 'DEC-CCW-A'), sg.Text('', size=(2, 1), key='CCWA'), cal_btn('>', 'INC-CCW-A')],
            [cal_btn('Center', 'twist-CENTER-A'), cal_btn('<', 'DEC-CENTER-A'), sg.Text('', size=(2, 1), key='CENTERA'), cal_btn('>', 'INC-CENTER-A')],
            [cal_btn('CW', 'twist-CW-A'), cal_btn('<', 'DEC-CW-A'), sg.Text('', size=(2, 1), key='CWA'), cal_btn('>', 'INC-CW-A')]
        ])]
    ])
    col2 = sg.Column([
        [sg.Frame('Gripper A', [
            [cal_btn('Open', 'grip-OPEN-B'), cal_btn('<', 'DEC-OPEN-B'), sg.Text('', size=(2, 1), key='OPENB'), cal_btn('>', 'INC-OPEN-B')],
            [cal_btn('Load', 'grip-LOAD-B'), cal_btn('<', 'DEC-LOAD-B'), sg.Text('', size=(2, 1), key='LOADB'), cal_btn('>', 'INC-LOAD-B')],
            [cal_btn('Close', 'grip-CLOSE-B'), cal_btn('<', 'DEC-CLOSE-B'), sg.Text('', size=(2, 1), key='CLOSEB'), cal_btn('>', 'INC-CLOSE-B')],
            [cal_btn('CCW', 'twist-CCW-B'), cal_btn('<', 'DEC-CCW-B'), sg.Text('', size=(2, 1), key='CCWB'), cal_btn('>', 'INC-CCW-B')],
            [cal_btn('Center', 'twist-CENTER-B'), cal_btn('<', 'DEC-CENTER-B'), sg.Text('', size=(2, 1), key='CENTERB'), cal_btn('>', 'INC-CENTER-B')],
            [cal_btn('CW', 'twist-CW-B'), cal_btn('<', 'DEC-CW-B'), sg.Text('', size=(2, 1), key='CWB'), cal_btn('>', 'INC-CW-B')]
        ])]
    ])
    layout = [[col1, col2], [sg.Text('', font=('Computerfont', 14), size=(20, 1), key='-STATUS-')]]
    return layout


def scan():
    pass


# read cal.json file and get saved calibration data
import_caldata()

# ----- Event LOOP Read and display frames, operate the GUI ----- #
while True:
    button, values = window.read(timeout=50)
    if button in (None, 'Quit', 'Escape:9'):
        break
    elif button == '-SOLVETOBTN-':
        window_solveto = sg.Window('Solve To', solveto_layout(), size=(480, 320), no_titlebar=True)
        solvebtn, solvevals = window_solveto.read(close=True)
        SOLVETO = solvebtn
        window['-SOLVETO-'].update(SOLVETO)
        window['-SOLVETOBTN-'].update(image_filename='images/{}'.format(PATTERNS[SOLVETO][0]))
    elif button == 'Calibrate':
        window_cal = sg.Window('Solve-O-Matic', cal_layout(), size=(480, 320), no_titlebar=True)
        while True:
            calbtn, calvals = window_cal.read(timeout=50)
            if calbtn in (None, 'Quit'):
                window_cal.Close()
                break
            elif calbtn != 'TIMEOUT':
                cmd,pos,gripper = calbtn.split('-')
                if cmd == 'grip':
                    grip(gripper, pos[0].lower())
                elif cmd == 'twist':
                    twist(gripper, pos.lower())
                elif cmd in ('INC', 'DEC'):
                    # TODO update params
                    pass
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
