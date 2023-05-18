from Libs.Jessie import Detection
from threading import Thread

#Threading to check for incomming input
class checkAiInput(Thread):
    def __init__(self, trigger):
        Thread.__init__(self)
        self.trigger = trigger

    def run(self):
        while True:
            if self.trigger:
                