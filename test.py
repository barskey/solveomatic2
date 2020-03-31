import PySimpleGUI as sg            # Uncomment 1 to run on that framework
# import PySimpleGUIQt as sg        # runs on Qt with no other changes
# import PySimpleGUIWeb as sg       # has a known flicker problem that's being worked
import cv2
from vision2 import grab_colors
import vision_params

sg.theme('Dark Grey')
#sg.set_options(element_padding=(0, 0))

title = sg.Text('Solve-O-Matic!')

# define the canvas for showing camera and color boxes
col_left = sg.Column([
    [sg.Text('')],
    [sg.Text('1.'), sg.Button('Scan Cube', size=(11, 1))],
    [sg.Text('2.'), sg.Button('Solve To', size=(11, 1))],
    [sg.Text('', size=(3, 1)), sg.Image('img/bg.png', size=(60, 60))],
    [sg.Text('3.'), sg.Button('Solve!', size=(11, 1), disabled=True)]
])

g = sg.Graph(canvas_size=(160, 160), graph_bottom_left=(0, 0), graph_top_right=(160, 160), key='graph')

col_right = sg.Column([
    [sg.Text('')],
    [g],
    [sg.Text('', size=(11, 1)), sg.Button('Calibrate')]
])

layout = [[col_left, col_right]]

# create the window and show it without the plot
window = sg.Window('Solve-O-Matic', layout, size=(480, 320))

# ---===--- Event LOOP Read and display frames, operate the GUI --- #
cap = cv2.VideoCapture(0)                               # Setup the OpenCV capture device (webcam)

while True:
    event, values = window.Read(timeout=20, timeout_key='timeout')
    if event is None:
        break
    ret, frame = cap.read()                               # Read image from capture device (camera)
    #print(frame.shape)
    # crop frame to square, then resize
    y = frame.shape[0]
    x = frame.shape[1]
    edge = int((x - y) / 2)
    frame_crop = frame[0:y, edge:(x - edge)]  # [starty:endy, startx:endx]
    frame_resize = cv2.resize(frame_crop, (160, 160))  # resize to 160x160

    grab_colors(frame_resize)
    print(vision_params.face_col)
    
    img_bytes = cv2.imencode('.png', frame_resize)[1].tobytes()     # Convert the image to PNG Bytes
    g.draw_image(location=(0, 160), data=img_bytes)
