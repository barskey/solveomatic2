import PySimpleGUI as sg  # Uncomment 1 to run on that framework
# import PySimpleGUIQt as sg        # runs on Qt with no other changes
# import PySimpleGUIWeb as sg       # has a known flicker problem that's being worked
import cv2
from vision2 import grab_colors
from lookups import PATTERNS

# ----- Window setup ----- #
sg.theme('Dark Grey')
# sg.set_options(element_padding=(0, 0))
title = sg.Text('Solve-O-Matic!')


def btn(name, state):
    return sg.Button(name, size=(11, 1), disabled=state)


# ----- User Input window layout ----- #
col1 = sg.Column([
    [sg.Frame('Step 1 | Insert cube', [
        [sg.Sizer(220, 1)],
        [sg.Button('GRIP', size=(11, 1))],
        [sg.Button('SCAN', size=(11, 1), disabled=True)]
    ], pad=(0, 0), element_justification='center')],
    [sg.Frame('Step 2 | Pick a pattern:', [
        [sg.Sizer(220, 1)],
        [sg.Combo(list(PATTERNS.keys()), default_value='Solid Cube', key='-SOLVETO-')],
        [sg.Image('images/_solid.png', key='-SOLVETOIMG-')]
    ], pad=(0, 0), element_justification='center')]
], element_justification='center', size=(240, 240), pad=(0, 0))
col2 = sg.Column([
    [sg.Frame('Step 3 | Go', [
        [sg.Sizer(220, 1)],  # pads col to 220 pix
        [sg.Graph(canvas_size=(160, 160), graph_bottom_left=(0, 0), graph_top_right=(160, 160), key='-GRAPH-')],
        # canvas to display image
        [sg.Button('SOLVE!', size=(11, 1), disabled=True)]
    ], pad=(0, 0))]
], element_justification='center', size=(240, 220))
col3 = sg.Column([
    [sg.Text('Insert cube and GRIP to continue...', font=('Computerfont', 18, ''), key='-INFO-'), sg.Quit(),
     sg.Button('Calibrate')]
])
layout = [[col1, col2], [col3]]
window = sg.Window('Solve-O-Matic', layout, size=(480, 320), no_titlebar=True, return_keyboard_events=True)

# ----- Solve To window layout ----- #
solveto_row = []
cols = 6
count = 1
solveto_layout = [[sg.Text('Select a pattern to solve to:', font=('Computerfont', 18))]]
for p, l in PATTERNS.items():
    if not count % cols:
        solveto_layout += [solveto_row]
        solveto_row = []
    solveto_row += [sg.Button(p, button_color=(sg.theme_background_color(), sg.theme_background_color()),
                              image_filename='images/{}'.format(l[0]), image_size=(40, 40), image_subsample=2,
                              border_width=0)]
    count += 1
if solveto_row:
    solveto_layout += [solveto_row]
solveto_window = sg.Window('Solve To', solveto_layout, size=(400, 300), no_titlebar=True)
solveto_window.read()
solveto_window.close()


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
    img_bytes = cv2.imencode('.png', frame)[1].tobytes()  # Convert the image to PNG Bytes
    window['-GRAPH-'].draw_image(location=(0, 160), data=img_bytes)

window.Close()
