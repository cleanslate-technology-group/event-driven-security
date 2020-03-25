import time
import board
import neopixel
import busio
import digitalio

num_chars_read = 32
uart = busio.UART(board.TX, board.RX, baudrate=9600)
pixel_pin = board.NEOPIXEL
num_pixels = 10
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels,
                           brightness=0.2, auto_write=False, pixel_order=ORDER)

good_color = (0, 255, 0)
bad_color = (255, 0, 0)
neutral_color = (66, 33, 99)
active_color = neutral_color

while True:

    data = uart.read(32)

    if data is not None:
        data = data.splitlines()
        for lines in data:
            line = ''.join([chr(b) for b in lines])
            if line == "ALERT:HIGH":
                print("Got alert signal, color should be red")
                active_color = bad_color
            elif line == "ALERT:LOW":
                print("Got alert signal, color should be green")
                active_color = good_color
            elif line == "ALERT:RESET":
                print("Got alert signal, color should be neutral")
                active_color = neutral_color

    pixels.fill(active_color)
    pixels.show()
