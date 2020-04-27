from threading import Thread
from vision2 import grab_colors
img_bytes = b''

class imgThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        while True:
            img_bytes = grab_colors()


imgThread()
import gui
# Start the GUI
