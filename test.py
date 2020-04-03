import PySimpleGUI as sg            # Uncomment 1 to run on that framework
# import PySimpleGUIQt as sg        # runs on Qt with no other changes
# import PySimpleGUIWeb as sg       # has a known flicker problem that's being worked
import cv2
from vision2 import grab_colors
from lookups import PATTERNS

# ----- Window setup ----- #
sg.theme('Dark Grey')
#sg.set_options(element_padding=(0, 0))
title = sg.Text('Solve-O-Matic!')

# ----- User Input window layout ----- #
col1 = sg.Column([
        [sg.Frame('Step 1', [
            [sg.Button('GRIP', size=(11,1))],
            [sg.Button('SCAN', size=(11, 1), disabled=True)]
        ], size=(480, 240), pad=(0, 0))],
        [sg.Frame('Step 2', [
            [sg.Combo(list(PATTERNS.keys()), default_value='Solid Cube', key='-SOLVETO-')],
            [sg.Image('images/_solid.png', key='-SOLVETOIMG-')]
        ], size=(480, 240), pad=(0, 0))],
        [sg.Frame('Step 3', [
            [sg.Button('SOLVE!', size=(11, 1), disabled=True)]
        ], size=(480, 240), pad=(0, 0))]
    ], element_justification='center', pad=(0, 0))
col2 = sg.Column([
        [sg.Sizer(200, 1)],  # pads col to 200 pix
        [sg.Graph(canvas_size=(160, 160), graph_bottom_left=(0, 0), graph_top_right=(160, 160), key='-GRAPH-')], #  canvas to display image
        [sg.Quit(), sg.Button('Calibrate')]
    ], element_justification='center')
col3 = sg.Column([
    [sg.Text('Insert cube and GRIP to continue...', font=('Computerfont', 14, ''), key='-INFO-')]
])
layout = [[col1, col2], [col3]]
window = sg.Window('Solve-O-Matic', layout, size=(480, 320), no_titlebar=True, return_keyboard_events=True)

# ----- Calibration window layout ----- #
def cal_layout():
    return ([[
        sg.Column([
            [sg.Sizer(200,1)],
            [sg.Graph(canvas_size=(160, 160), graph_bottom_left=(0, 0), graph_top_right=(160, 160), key='-CALGRAPH-')], #  canvas to display image
            [sg.Quit(), sg.Button('Calibrate')]
        ])
    ]])

def grip(state):
    pass

def scan():
    pass

# ----- Event LOOP Read and display frames, operate the GUI ----- #
while True:
    button, values = window.read(timeout=50)
    if button in (None, 'Quit'):
        break
    elif button == 'Calibrate':
       window_cal = sg.Window('Solve-O-Matic', cal_layout(), size=(480, 320), no_titlebar=True)
       while True:
        calbtn, calvals = window_cal.read(timeout=50)
        if calbtn in (None, 'Quit'):
            window_cal.Close()
            break

    i = 'images/{}'.format(PATTERNS[values['-SOLVETO-']][0])
    window['-SOLVETOIMG-'].Update(filename=i)
    frame = grab_colors()
    img_bytes = cv2.imencode('.png', frame)[1].tobytes()     # Convert the image to PNG Bytes
    window['-GRAPH-'].draw_image(location=(0, 160), data=img_bytes)

window.Close()
