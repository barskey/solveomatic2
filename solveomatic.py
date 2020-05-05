from threading import Thread
from vision2 import grab_colors
import vision_params

class imgThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            vision_params.img_bytes = grab_colors()


#imgThread()
import gui
# Start the GUI
