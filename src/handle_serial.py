"""_summary_

Raises:
    Exception: _description_
"""

import serial


class TeensySerialError(ValueError):
    """A custom wrapper for generating errors related to serail communications with the Teensy

    Args:
        ValueError (_type_): Normal built-in error
    """


class TeensySerial:
    """Creates a wrapper for serial.Serial communications with the Teensy 4.1"""

    def __init__(self, port: str, baudrate: int):
        """Initializes serial object with default settings.

        Args:
            port (str): System-sepecific COM port used for serial communications.
            baudrate (int): The number of signal changes or symbols transmitted per second
        """
        self.ser = serial.Serial(port, baudrate=baudrate)
        self.ser.timeout = 1

    def open(self):
        """Opens the serial connection to the Teensy

        Raises:
            TeensySerialError: Raised if the connection cannot be opened.
        """
        try:
            self.ser.open()
        except Exception as e:
            raise TeensySerialError(
                f"Serial connection was not opened due to {repr(e)}"
            ) from e

    def close(self):
        """Immediately closes the serial connection if it is open.

        Raises:
            TeensySerialError: Raised if the connection is not open.
            TeensySerialError: Raised if there was an error when closing the connection.
        """
        if not self.ser.is_open:
            raise TeensySerialError("Serial port is not opened, so it cannot be closed")
        try:
            self.ser.close()
        except Exception as e:
            raise TeensySerialError(
                f"Serial connection was not closed due to {repr(e)}"
            ) from e

    def write(self, data: bytes | str, encode: str = "UTF-8"):
        """Writes bytes to the serial interface.

        Args:
            data (bytes): A python bytes object of arbitrary length.

        Raises:
            TeensySerialError: Raises if there was an error during writing to the Teensy.
        """

        if isinstance(data, str):
            data = data.encode(encode)
        try:
            self.ser.write(data)
        except Exception as e:
            raise TeensySerialError(f"Connection timed out due to {repr(e)}") from e

    def read(self, size: int = None, expected: str = ""):
        """Reads until an expected character is seen. If there is no expected character or the
            reading times out, all read characters will return, up to the integer size of bytes.

        Args:
            size (int, optional): Number of bytes to read. Size of bytes to read must be > 1.
            expected (str, optional): _description_. Defaults to None.

        Returns:
            bytes: Size-number of bytes sent by the serial device.
        """

        if isinstance(size, int) and not size >= 1:
            raise TeensySerialError("Size of bytes to read must be > 1.")

        if not self.ser.is_open:
            self.open()

        if expected != "":
            try:
                bytes_read = self.ser.read_until(expected=expected, size=size)
            except Exception as e:
                raise TeensySerialError(
                    f"Reading until {expected} failed due to {repr(e)}"
                ) from e

        elif size is not None:

            try:
                bytes_read = self.ser.read(size=size)
            except Exception as e:
                raise TeensySerialError(
                    f"Reading {size} bytes failed due to {repr(e)}"
                ) from e

            if len(bytes_read) != size:
                raise TeensySerialError(
                    f"Only {len(bytes_read)} of {size} bytes were read."
                )

        else:

            try:

                bytes_read = self.ser.readline()[:-1]  # Removes b'\n'
            except Exception as e:
                raise TeensySerialError(f"Reading line failed due to {repr(e)}") from e

        if bytes_read is None:
            raise TeensySerialError("No bytes were read")

        return bytes_read
