#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Program: Teste modulo MAX7219 com Raspberry Pi
# Autor: Arduino e Cia
# Baseado no programa exemplo da biblioteca MAX7219
#
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import time
import argparse
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import show_message
from luma.core.legacy.font import proportional, LCD_FONT

def demo(n, block_orientation, rotate):
    """
    Initialize the MAX7219 device and display a scrolling message.
    
    Parameters:
    n (int): Number of cascaded MAX7219 modules.
    block_orientation (int): Block orientation correction (0, 90, -90).
    rotate (int): Rotation of the display (0=0Â°, 1=90Â°, 2=180Â°, 3=270Â°).
    """
    # Initialize SPI communication
    serial = spi(port=0, device=0, gpio=noop())
    # Initialize the MAX7219 device
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation, rotate=rotate or 0)
    
    # Define the message to be displayed
    msg = "Autobotic"
    
    # Display the scrolling message
    show_message(device, msg, fill="white", font=proportional(LCD_FONT), scroll_delay=0.2)

if __name__ == "__main__":
    # Setup argument parser
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 modules')
    parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Block orientation correction')
    parser.add_argument('--rotate', type=int, default=2, choices=[0, 1, 2, 3], help='Rotation of the display (0=0Â°, 1=90Â°, 2=180Â°, 3=270Â°)')

    # Parse arguments
    args = parser.parse_args()

    try:
        # Run the demo with parsed arguments
        demo(args.cascaded, args.block_orientation, args.rotate)
    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Stopping the program...")
        # Additional cleanup actions can be added here if necessary

