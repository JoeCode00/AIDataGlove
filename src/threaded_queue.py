from time import time_ns, sleep
from queue import Queue, Empty
from threading import Thread
import struct
from handle_serial import TeensySerial


class ComThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.teensy = TeensySerial(port='COM17', baudrate=115200)
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



def main():
    com = ComThread()
    com.start()
    while True:
        struct_pattern = '8d'
        data = com.reader()
        if data is not None:
            struct_size = struct.calcsize(struct_pattern)
            if len(data) != struct_size:
                continue
            data_tuple = struct.unpack(struct_pattern, data) # pylint: disable=unpacking-non-sequence
            print(f'Recieved {data_tuple}')
            com.writer(data)
            

if __name__ == '__main__':
    main()
