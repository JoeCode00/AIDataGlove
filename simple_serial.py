import time
import serial

def main():
    with serial.Serial('COM17') as ser:
        ser.timeout = 1
        time.sleep(2)
        while True:
            string = 'From Windows\n'
            ser.write(string.encode(encoding='utf-8'))
            read = ser.readline()
            if read != b'':
                read_string = read.decode()
                print(f'{time.time_ns()} {read_string}')

main()
