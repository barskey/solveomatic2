import time
import PySimpleGUI as sg            # Uncomment 1 to run on that framework
# import PySimpleGUIQt as sg        # runs on Qt with no other changes
# import PySimpleGUIWeb as sg       # has a known flicker problem that's being worked
import cv2
from vision2 import grab_colors
from lookups import PATTERNS

sg.theme('Dark Grey')
#sg.set_options(element_padding=(0, 0))

title = sg.Text('Solve-O-Matic!')

solveto_img = sg.Image('img/bg.png', size=(60, 60), key='__SOLVETOIMG__')
col_left = sg.Column([
    [sg.Sizer(200, 10)],
    [sg.Text('1.'), sg.Button('Scan Cube', size=(11, 1))],
    [sg.Text('2.'), sg.Combo(list(PATTERNS.keys()), key='__SOLVETO__')],
    [sg.Text('', size=(3, 1)), solveto_img],
    [sg.Text('3.'), sg.Button('Solve!', size=(11, 1), disabled=True)]
], element_justification='center')
# define the canvas (graph) for showing camera and color boxes
g = sg.Graph(canvas_size=(160, 160), graph_bottom_left=(0, 0), graph_top_right=(160, 160), key='graph')

col_right = sg.Column([
    [sg.Sizer(200, 10)],
    [g],
    [sg.Quit(), sg.Button('Calibrate', key='__CALIBRATE__')]
], element_justification='center')

layout = [[col_left, col_right]]

# create the window and show it without the plot
window = sg.Window('Solve-O-Matic', layout, size=(480, 320), no_titlebar=True, keep_on_top=True, finalize=True)

# ---===--- Event LOOP Read and display frames, operate the GUI --- #
while True:
    event, values = window.Read(timeout=20, timeout_key='timeout')
    if event in ('Quit', None):
        break

    i = 'images/{}'.format('_solid.png')
    solveto_img.Update(filename=i)

    frame = grab_colors()

    img_bytes = cv2.imencode('.png', frame)[1].tobytes()     # Convert the image to PNG Bytes
    g.draw_image(location=(0, 160), data=img_bytes)

    if event == '__CALIBRATE__':
        frame_grab()
