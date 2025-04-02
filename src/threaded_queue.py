from time import sleep
from queue import Queue, Empty
from threading import Thread
from src.handle_serial import TeensySerial


class ComThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.teensy = TeensySerial(port="COM17", baudrate=115200)
        self.write = Queue(maxsize=0)
        self.read = Queue(maxsize=0)
        self.daemon = True

    # receives a name, then prints "Hello, name!"
    def run(self):
        while True:
            self.queue_writer()
            self.queue_reader()

    def queue_writer(self):
        try:

            data = self.write.get(block=False, timeout=0.05)
            self.teensy.write(data)
        except Empty:
            pass

    def queue_reader(self):
        bytes_read = self.teensy.read()
        self.read.put(bytes_read)

    def writer(self, data):
        sleep(0.001)
        self.write.put(data)

    def reader(self):
        sleep(0.001)
        try:
            data = self.read.get(block=False, timeout=0.05)
            return data
        except Empty:
            pass
