import struct
import time
from src.threaded_queue import ComThread
from src.handle_time import Timer
from src.position_integrator import dynamics
import numpy as np

np.set_printoptions(suppress=True)

def communicate(com:ComThread, data_write:bytes|tuple, struct_pattern:str, disable_read:bool=False):
    if data_write is not None:
        if isinstance(data_write, tuple):
            if struct_pattern is None:
                raise Exception('Must pass in a struct pattern with tuple to be packed')
            data_write = struct.pack(struct_pattern, *data_write)
        com.writer(data_write)
    
    data_read = None
    if not disable_read:
        data_read = com.reader()
        if data_read is not None:
            struct_size = struct.calcsize(struct_pattern)
            if len(data_read) != struct_size:
                return
            data_read = struct.unpack(struct_pattern, data_read) 
            
    return data_read
        

def main():
    com = ComThread()
    time = Timer()
    pos = dynamics()
    com.start()
    data_write = (0,0,0,0,0,0,0,0)

    bias_timer = Timer()
    bias_set = False

    while True:
        data_read= communicate(com, data_write, struct_pattern='8d')
        if data_read is not None:
            # print(f'Recieved {data_read} {time.now()}')
            data_write = data_read
            accelerometer_x, accelerometer_y, accelerometer_z, *_ = data_read  # pylint: disable=unpacking-non-sequence3
            pos.get(time.now(), accelerometer_x, accelerometer_y, accelerometer_z)
            
            if bias_timer.current() > bias_timer.origin + 5 and not bias_set:
                pos.bias()
                bias_set = True

if __name__ == '__main__':
    main()