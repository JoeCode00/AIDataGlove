import struct
from src.threaded_queue import ComThread


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