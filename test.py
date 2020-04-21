import PySimpleGUI as sg  # Uncomment 1 to run on that framework
# import PySimpleGUIQt as sg        # runs on Qt with no other changes
# import PySimpleGUIWeb as sg       # has a known flicker problem that's being worked
import cv2
from vision2 import grab_colors
from lookups import PATTERNS

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
    [sg.Frame('Step 2 | Pick a pattern:', [
        [sg.Sizer(200, 1)],
        [sg.Button('', image_filename='images/{}'.format(PATTERNS[SOLVETO][0]), key='-SOLVETOBTN-')],
        [sg.Text(SOLVETO, font=('Computerfont', 18, ''), key='-SOLVETO-')]
    ], pad=(0, 0), element_justification='center')]
], element_justification='center', pad=(0, 0))
col2 = sg.Column([
    [sg.Frame('Step 3 | Go', [
        [sg.Sizer(210, 1)],  # pads col to 210 pix
        [sg.Graph(canvas_size=(160, 160), graph_bottom_left=(0, 0), graph_top_right=(160, 160), key='-GRAPH-')],
        # canvas to display image
        [sg.Button('SOLVE!', size=(11, 1), disabled=True)]
    ], pad=(0, 0))]
], element_justification='center')
col3 = sg.Column([
    [sg.Text('Insert cube and GRIP to continue...', font=('Computerfont', 18, ''), key='-INFO-'), sg.Quit(),
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
        row += [sg.Button('', button_color=(sg.theme_background_color(), sg.theme_background_color()),
                                  image_filename='images/{}'.format(l[0]),
                                  border_width=0)]
        count += 1
    if row:
        layout += [row]
    return layout


# ----- Calibration window layout ----- #
def cal_layout():
    return ([[
        sg.Column([
            [sg.Sizer(200, 1)],
            [sg.Graph(canvas_size=(160, 160), graph_bottom_left=(0, 0), graph_top_right=(160, 160), key='-CALGRAPH-')],
            # canvas to display image
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
    elif button == '=SOLVETOBTN-':
        print('yay')
        window_solveto = sg.Window('Solve To', solveto_layout(), size=(400, 300), no_titlebar=True)
        while True:
            solvebtn, solvevals = window_solveto.read()
            print(solvebtn)
            window_solveto.close()
    elif button == 'Calibrate':
        window_cal = sg.Window('Solve-O-Matic', cal_layout(), size=(480, 320), no_titlebar=True)
        while True:
            calbtn, calvals = window_cal.read(timeout=50)
            if calbtn in (None, 'Quit'):
                window_cal.Close()
                break

    frame = grab_colors()
    img_bytes = cv2.imencode('.png', frame)[1].tobytes()  # Convert the image to PNG Bytes
    window['-GRAPH-'].draw_image(location=(0, 160), data=img_bytes)

window.Close()
