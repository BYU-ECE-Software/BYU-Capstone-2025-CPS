"""
I2C LCD driver for MicroPython on ESP32
Supports 1602 and 2004 LCD displays with PCF8574 I2C backpack
"""

import time
from machine import I2C

# LCD Commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# Flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Flags for display control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# Flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# Flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# Backlight control
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

# Enable bit
En = 0b00000100

# Read/Write bit
Rw = 0b00000010

# Register select bit
Rs = 0b00000001


class LCD_I2C:
    """Class to control I2C LCD displays"""

    def __init__(self, i2c, addr=0x27, cols=16, rows=2):
        """
        Initialize the LCD
        :param i2c: I2C object
        :param addr: I2C address of the LCD (usually 0x27 or 0x3F)
        :param cols: Number of columns (usually 16 or 20)
        :param rows: Number of rows (usually 2 or 4)
        """
        self.i2c = i2c
        self.addr = addr
        self.cols = cols
        self.rows = rows
        self.backlight_state = LCD_BACKLIGHT

        # Initialize display
        self._write(0x03)
        self._write(0x03)
        self._write(0x03)
        self._write(0x02)

        # Set display parameters
        self._write(LCD_FUNCTIONSET | LCD_2LINE | LCD_5x8DOTS | LCD_4BITMODE)
        self._write(LCD_DISPLAYCONTROL | LCD_DISPLAYON)
        self._write(LCD_CLEARDISPLAY)
        self._write(LCD_ENTRYMODESET | LCD_ENTRYLEFT)
        time.sleep_ms(200)

    def _write_byte(self, data):
        """Write byte to I2C"""
        self.i2c.writeto(self.addr, bytes([data]))
        time.sleep_us(100)

    def _toggle_enable(self, data):
        """Toggle enable pin"""
        time.sleep_us(500)
        self._write_byte(data | En | self.backlight_state)
        time.sleep_us(500)
        self._write_byte((data & ~En) | self.backlight_state)
        time.sleep_us(500)

    def _write_four_bits(self, data):
        """Write 4 bits to the LCD"""
        self._write_byte(data | self.backlight_state)
        self._toggle_enable(data)

    def _write(self, cmd, mode=0):
        """Write command or data to LCD"""
        self._write_four_bits(mode | (cmd & 0xF0))
        self._write_four_bits(mode | ((cmd << 4) & 0xF0))

    def clear(self):
        """Clear the display"""
        self._write(LCD_CLEARDISPLAY)
        time.sleep_ms(2)

    def home(self):
        """Return cursor to home position"""
        self._write(LCD_RETURNHOME)
        time.sleep_ms(2)

    def set_cursor(self, col, row):
        """Set cursor position"""
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        if row >= self.rows:
            row = self.rows - 1
        self._write(LCD_SETDDRAMADDR | (col + row_offsets[row]))

    def print(self, text):
        """Print text at current cursor position"""
        for char in text:
            self._write(ord(char), Rs)

    def display_on(self):
        """Turn display on"""
        self.display_ctrl |= LCD_DISPLAYON
        self._write(LCD_DISPLAYCONTROL | self.display_ctrl)

    def display_off(self):
        """Turn display off"""
        self.display_ctrl &= ~LCD_DISPLAYON
        self._write(LCD_DISPLAYCONTROL | self.display_ctrl)

    def backlight_on(self):
        """Turn backlight on"""
        self.backlight_state = LCD_BACKLIGHT
        self._write_byte(0)

    def backlight_off(self):
        """Turn backlight off"""
        self.backlight_state = LCD_NOBACKLIGHT
        self._write_byte(0)

    def cursor_on(self):
        """Show cursor"""
        self.display_ctrl |= LCD_CURSORON
        self._write(LCD_DISPLAYCONTROL | self.display_ctrl)

    def cursor_off(self):
        """Hide cursor"""
        self.display_ctrl &= ~LCD_CURSORON
        self._write(LCD_DISPLAYCONTROL | self.display_ctrl)

    def blink_on(self):
        """Enable cursor blinking"""
        self.display_ctrl |= LCD_BLINKON
        self._write(LCD_DISPLAYCONTROL | self.display_ctrl)

    def blink_off(self):
        """Disable cursor blinking"""
        self.display_ctrl &= ~LCD_BLINKON
        self._write(LCD_DISPLAYCONTROL | self.display_ctrl)

    def scroll_left(self):
        """Scroll display left"""
        self._write(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVELEFT)

    def scroll_right(self):
        """Scroll display right"""
        self._write(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | LCD_MOVERIGHT)

    def create_char(self, location, charmap):
        """
        Create custom character
        :param location: Character location (0-7)
        :param charmap: List of 8 bytes defining the character
        """
        location &= 0x07
        self._write(LCD_SETCGRAMADDR | (location << 3))
        for byte in charmap:
            self._write(byte, Rs)