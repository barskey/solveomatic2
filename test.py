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
# ----- Intro Screen window layout | win_intro -----
layout_intro = [[
    sg.Column([
        [sg.Sizer(440, 10)],
        [sg.Text('Solve-O-Matic')],
        [sg.Text('Insert Cube')],
        [sg.Text('to get started...')],
        [sg.Text('')],
        [sg.Button('Go', size=(11,2))]
    ], element_justification='center')
]]
win_intro = sg.Window('Solve-O-Matic', layout_intro, size=(480, 320), no_titlebar=True, keep_on_top=True, return_keyboard_events=True)

# ----- User Input window layout | win_input -----
def win_input_layout():
    return ([[
        sg.Column([
            [sg.Sizer(200, 10)],  # pads col to 200 pix
            [sg.Text('1.'), sg.Button('Scan Cube', size=(11, 1))],
            [sg.Text('2.'), sg.Combo(list(PATTERNS.keys()), default_value='Solid Cube', key='-SOLVETO-')],
            [sg.Text('', size=(3, 1)), sg.Image('images/_solid.png', key='-SOLVETOIMG-')],
            [sg.Text('3.'), sg.Button('Solve!', size=(11, 1), disabled=True)]
        ]),
        sg.Column([
            [sg.Sizer(200, 10)],  # pads col to 200 pix
            [sg.Graph(canvas_size=(160, 160), graph_bottom_left=(0, 0), graph_top_right=(160, 160), key='-GRAPH-')], #  canvas to display image
            [sg.Quit(), sg.Button('Calibrate')]
        ], element_justification='center')
    ]])

#win_input = sg.Window('Solve-O-Matic', layout_input, size=(480, 320), no_titlebar=True, keep_on_top=True, finalize=True)
win_input_active = False

# ----- Calibration window layout | win_cal -----
#layout_cal = [[]]
#win_cal = sg.Window('Solve-O-Matic', layout_cal, size=(480, 320), no_titlebar=True, keep_on_top=True, finalize=True)
win_cal_active = False

# ---===--- Event LOOP Read and display frames, operate the GUI --- #
while True:
    button1, values1 = win_intro.read(timeout=50, timeout_key='timeout')
    
    if button1 in ('Quit', 'Escape:9', None):
        print(button1, 'exiting')
        break

    if button1 == 'Go' and not win_input_active:
        win_input_active = True
        win_intro.hide()
    
        win_input = sg.Window('Solve-O-Matic', win_input_layout(), size=(480, 320), no_titlebar=True, keep_on_top=True)
        while True:
            button2, values2 = win_input.read(timeout=50)
            if button2 in (None, 'Quit'):
                win_input.close()
                win_input_active = False
                win_intro.un_hide()
                win_intro.BringToFront()
                break

            i = 'images/{}'.format(PATTERNS[values2['-SOLVETO-']][0])
            win_input['-SOLVETOIMG-'].Update(filename=i)
            frame = grab_colors()
            img_bytes = cv2.imencode('.png', frame)[1].tobytes()     # Convert the image to PNG Bytes
            win_input['-GRAPH-'].draw_image(location=(0, 160), data=img_bytes)

window.Close()