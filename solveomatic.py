from threading import Thread
from vision2 import grab_colors

thr = Thread(target=grab_colors, args=())
thr.start()
# Run the opencv code and detect facelet colors

import gui
# Start the GUI with several sliders to configure some opencv parameters
