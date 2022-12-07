from machine import Pin,SPI
import framebuf
import time

DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

class LCD_ATM0130B3(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
#         self.spi = SPI(1)
#         self.spi = SPI(1,1000_000)
        self.spi = SPI(1,8000000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        

        self.WHITE =   0xFFFF
        self.BLACK  =  0x0000
        self.GREEN   =  0x001F
        self.BLUE    =  0xF800
        self.RED   = 0x07E0

        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x11)
        
        time.sleep_ms(100)
        
        self.write_cmd(0x36)
        self.write_data(0x00)
        
        self.write_cmd(0x3A)
        self.write_data(0x55)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        time.sleep_ms(2)
        
        self.write_cmd(0xB7)
        self.write_data(0x75)

        time.sleep_ms(2)
        
        self.write_cmd(0xC2)
        self.write_data(0x01)

        time.sleep_ms(2)
        
        self.write_cmd(0xC3)
        self.write_data(0x10)

        time.sleep_ms(2)
        
        self.write_cmd(0xC4)
        self.write_data(0x20)

        time.sleep_ms(2)
        
        self.write_cmd(0xC6)
        self.write_data(0x0F)

        self.write_cmd(0xB0)
        self.write_data(0x00)
        self.write_data(0xF0)

        time.sleep_ms(2)
        
        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        time.sleep_ms(2)

        # gamma
        self.write_cmd(0x21)

        time.sleep_ms(2)

        self.write_cmd(0xBB)
        self.write_data(0x3B)

        time.sleep_ms(2)

        self.write_cmd(0xE0)
        self.write_data(0xF0)
        self.write_data(0x0B)
        self.write_data(0x11)
        self.write_data(0x0E)
        self.write_data(0x0D)
        self.write_data(0x19)
        self.write_data(0x36)
        self.write_data(0x33)
        self.write_data(0x4B)
        self.write_data(0x07)
        self.write_data(0x14)
        self.write_data(0x14)
        self.write_data(0x2C)
        self.write_data(0x2E)
        
        time.sleep_ms(2)

        # Set Gamma
        self.write_cmd(0xE1)
        self.write_data(0xF0)
        self.write_data(0x0D)
        self.write_data(0x12)
        self.write_data(0x0B)
        self.write_data(0x09)
        self.write_data(0x03)
        self.write_data(0x32)
        self.write_data(0x44)
        self.write_data(0x48)
        self.write_data(0x39)
        self.write_data(0x16)
        self.write_data(0x16)
        self.write_data(0x2D)
        self.write_data(0x30)

        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)

        #Turn on the LCD display
        self.write_cmd(0x29);
        
        time.sleep_ms(2)

        self.write_cmd(0x2C)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)

        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
  
    def toColor(self, r, g, b):
        return ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
