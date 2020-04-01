import time
import PySimpleGUI as sg            # Uncomment 1 to run on that framework
# import PySimpleGUIQt as sg        # runs on Qt with no other changes
# import PySimpleGUIWeb as sg       # has a known flicker problem that's being worked
import cv2
from vision2 import grab_colors
from lookups import PATTERNS

# ----- Window setup -----
sg.theme('Dark Grey')
#sg.set_options(element_padding=(0, 0))
title = sg.Text('Solve-O-Matic!')
window = None

# ----- Intro Screen window layout -----
layout_intro = [[
    sg.Column([
        [sg.Text('Solve-O-Matic')],
        [sg.Text('Insert Cube')],
        [sg.Text('to get started...')],
        [sg.Text('')],
        [sg.Button('Go', size=(11,2))]
    ], element_justification='center')
]]

# ----- User Input window layout -----
solveto_img = sg.Image('images/_solid.png', size=(50, 50), key='-SOLVETOIMG-')
col_left = sg.Column([
    [sg.Sizer(200, 10)],
    [sg.Text('1.'), sg.Button('Scan Cube', size=(11, 1))],
    [sg.Text('2.'), sg.Combo(list(PATTERNS.keys()), default_value='Solid Cube', key='-SOLVETO-')],
    [sg.Text('', size=(3, 1)), solveto_img],
    [sg.Text('3.'), sg.Button('Solve!', size=(11, 1), disabled=True)]
])
# define the canvas (graph) for showing camera and color boxes
g = sg.Graph(canvas_size=(160, 160), graph_bottom_left=(0, 0), graph_top_right=(160, 160), key='graph')

col_right = sg.Column([
    [sg.Sizer(200, 10)],
    [g],
    [sg.Quit(), sg.Button('Calibrate')]
], element_justification='center')

layout_input = [[col_left, col_right]]

# ----- Calibration window layout -----
# layout_calibrate = 

def change_state(newstate):
    window.Close()  # close old window
    state = newstate
    window = sg.Window('Solve-O-Matic', layouts[state], size=(480, 320), no_titlebar=True, keep_on_top=True, finalize=True)

state = 0 # intro
layouts = [layout_intro, layout_input]

# start in state 0
window = sg.Window('Solve-O-Matic', layouts[state], size=(480, 320), no_titlebar=True, keep_on_top=True, finalize=True)

# ---===--- Event LOOP Read and display frames, operate the GUI --- #
while True:
    button, values = window.Read(timeout=50, timeout_key='timeout')
    
    if button in ('Quit', None):
        break
    elif button is 'Go':
        change_state(1)
    elif button is 'Calibrate':
        change_state(2)

    if state is 0:
        pass
    elif state is 1:
        i = 'images/{}'.format(PATTERNS[values['-SOLVETO-']][0])
        window.Element('-SOLVETOIMG-').Update(filename=i)
        frame = grab_colors()

        img_bytes = cv2.imencode('.png', frame)[1].tobytes()     # Convert the image to PNG Bytes
        g.draw_image(location=(0, 160), data=img_bytes)

window.Close()