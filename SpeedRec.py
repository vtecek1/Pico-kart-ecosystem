from machine import Pin,SPI,PWM
import framebuf
import time
import os

LCD_DC   = 8
LCD_CS   = 9
LCD_SCK  = 10
LCD_MOSI = 11
LCD_MISO = 12
LCD_BL   = 13
LCD_RST  = 15
TP_CS    = 16
TP_IRQ   = 17

class LCD_3inch5(framebuf.FrameBuffer):

    def __init__(self):
        self.RED   =   0x07E0
        self.GREEN =   0x001f
        self.BLUE  =   0xf800
        self.WHITE =   0xffff
        self.BLACK =   0x0000
        
        self.rotate = 90   # Set the rotation Angle to 0°, 90°, 180° and 270°
        
        if self.rotate == 0 or self.rotate == 180:
            self.width = 320
            self.height = 240
        else:
            self.width = 480
            self.height = 160
            
        self.cs = Pin(LCD_CS,Pin.OUT)
        self.rst = Pin(LCD_RST,Pin.OUT)
        self.dc = Pin(LCD_DC,Pin.OUT)
        
        self.tp_cs =Pin(TP_CS,Pin.OUT)
        self.irq = Pin(TP_IRQ,Pin.IN)
        
        self.cs(1)
        self.dc(1)
        self.rst(1)
        self.tp_cs(1)
        self.spi = SPI(1,6_000_000)
        print(self.spi)  
        self.spi = SPI(1,baudrate=40_000_000,sck=Pin(LCD_SCK),mosi=Pin(LCD_MOSI),miso=Pin(LCD_MISO))
        print(self.spi)      
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()

        
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
        #self.spi.write(bytearray([0X00]))
        self.spi.write(bytearray([buf]))
        self.cs(1)


    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        time.sleep_ms(5)
        self.rst(0)
        time.sleep_ms(10)
        self.rst(1)
        time.sleep_ms(5)
        self.write_cmd(0x21)
        
        self.write_cmd(0xC2)
        self.write_data(0x33)
        
        self.write_cmd(0XC5)
        self.write_data(0x00)
        self.write_data(0x1e)
        self.write_data(0x80)
        
        self.write_cmd(0xB1)
        self.write_data(0xB0)
        
        self.write_cmd(0XE0)
        self.write_data(0x00)
        self.write_data(0x13)
        self.write_data(0x18)
        self.write_data(0x04)
        self.write_data(0x0F)
        self.write_data(0x06)
        self.write_data(0x3a)
        self.write_data(0x56)
        self.write_data(0x4d)
        self.write_data(0x03)
        self.write_data(0x0a)
        self.write_data(0x06)
        self.write_data(0x30)
        self.write_data(0x3e)
        self.write_data(0x0f)
        
        self.write_cmd(0XE1)
        self.write_data(0x00)
        self.write_data(0x13)
        self.write_data(0x18)
        self.write_data(0x01)
        self.write_data(0x11)
        self.write_data(0x06)
        self.write_data(0x38)
        self.write_data(0x34)
        self.write_data(0x4d)
        self.write_data(0x06)
        self.write_data(0x0d)
        self.write_data(0x0b)
        self.write_data(0x31)
        self.write_data(0x37)
        self.write_data(0x0f)
        
        self.write_cmd(0X3A)
        self.write_data(0x55)
        
        self.write_cmd(0x11)
        time.sleep_ms(120)
        self.write_cmd(0x29)
        
        self.write_cmd(0xB6)
        self.write_data(0x00)
        self.write_data(0x62)
        
        self.write_cmd(0x36) # Sets the memory access mode for rotation
        if self.rotate == 0:
            self.write_data(0x88)
        elif self.rotate == 180:
            self.write_data(0x48)
        elif self.rotate == 90:
            self.write_data(0xe8)
        else:
            self.write_data(0x28)
    def show_up(self):
        if self.rotate == 0 or self.rotate == 180:
            self.write_cmd(0x2A)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x01)
            self.write_data(0x3f)
             
            self.write_cmd(0x2B)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0xef)
        else:
            self.write_cmd(0x2A)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x01)
            self.write_data(0xdf)
            
            self.write_cmd(0x2B)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x9f)
            
            
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    def show_down(self):
        if self.rotate == 0 or self.rotate == 180:
            self.write_cmd(0x2A)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x01)
            self.write_data(0x3f)
             
            self.write_cmd(0x2B)
            self.write_data(0x00)
            self.write_data(0xf0)
            self.write_data(0x01)
            self.write_data(0xdf)
        else:
            self.write_cmd(0x2A)
            self.write_data(0x00)
            self.write_data(0x00)
            self.write_data(0x01)
            self.write_data(0xdf)
            
            self.write_cmd(0x2B)
            self.write_data(0x00)
            self.write_data(0xA0)
            self.write_data(0x01)
            self.write_data(0x3f)
            
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
    def bl_ctrl(self, duty):
        pwm = PWM(Pin(LCD_BL))
        pwm.freq(1000)
        if(duty>=100):
            pwm.duty_u16(65535)
        else:
            pwm.duty_u16(655*duty)
#function for lines
#Full straight left vertical
def FullL(x, y):
    LCD.text("|",x - 11,y, LCD.BLACK)
    LCD.text("|",x - 11,y - 2,LCD.BLACK)
    LCD.text("|",x - 11,y - 10,LCD.BLACK)
    LCD.text("|",x - 11,y - 18,LCD.BLACK)
    LCD.text("|",x - 11,y + 8,LCD.BLACK)
    LCD.text("|",x - 11,y + 16,LCD.BLACK)
    LCD.text("|",x - 11,y + 24,LCD.BLACK)

#Full straight right vertical
def FullR(x, y):
    LCD.text("|",x + 11,y,LCD.BLACK)
    LCD.text("|",x + 11,y - 2,LCD.BLACK)
    LCD.text("|",x + 11,y - 10,LCD.BLACK)
    LCD.text("|",x + 11,y - 18,LCD.BLACK)
    LCD.text("|",x + 11,y + 8,LCD.BLACK)
    LCD.text("|",x + 11,y + 16,LCD.BLACK)
    LCD.text("|",x + 11,y + 24,LCD.BLACK)

#Top half left straight vertical
def TopL(x, y):
    LCD.text("|",x - 11,y - 2,LCD.BLACK)
    LCD.text("|",x - 11,y - 10,LCD.BLACK)
    LCD.text("|",x - 11,y - 18,LCD.BLACK)

#Bottom half left straight vertical
def BottomL(x, y):
    LCD.text("|",x - 11,y + 8,LCD.BLACK)
    LCD.text("|",x - 11,y + 16,LCD.BLACK)
    LCD.text("|",x - 11,y + 24,LCD.BLACK)
#Top half right straight vertical
def TopR(x, y):
    LCD.text("|",x + 11,y - 2,LCD.BLACK)
    LCD.text("|",x + 11,y - 10,LCD.BLACK)
    LCD.text("|",x + 11,y - 18,LCD.BLACK)
#Bottom half right straight vertical
def BottomR(x, y):
    LCD.text("|",x + 11,y + 8,LCD.BLACK)
    LCD.text("|",x + 11,y + 16,LCD.BLACK)
    LCD.text("|",x + 11,y + 24,LCD.BLACK)
#Top straight horizontal
def Top(x, y):
    LCD.text("_",x,y - 24,LCD.BLACK)
    LCD.text("_",x + 8,y - 24,LCD.BLACK)
    LCD.text("_",x - 8,y - 24,LCD.BLACK)
#centre straight horizontal
def Centre(x, y):
    LCD.text("_",x,y,LCD.BLACK)
    LCD.text("_",x + 8,y,LCD.BLACK)
    LCD.text("_",x - 8,y,LCD.BLACK)
#bottom straight horizontal
def Bottom(x, y):
    LCD.text("_",x,y + 24,LCD.BLACK)
    LCD.text("_",x + 8,y + 24,LCD.BLACK)
    LCD.text("_",x - 8,y + 24,LCD.BLACK)




#function for the numbers
#num 1
def one(x, y):
    #the middle line, vertical
    LCD.text("|",x,y,LCD.BLACK)
    LCD.text("|",x,y + 8,LCD.BLACK)
    LCD.text("|",x,y + 16,LCD.BLACK)
    LCD.text("|",x,y + 24,LCD.BLACK)
    LCD.text("|",x,y - 8,LCD.BLACK)
    LCD.text("|",x,y - 16,LCD.BLACK)
    
    Bottom(x, y)
    
    #the diagonal line on top
    LCD.text("/",x-4,y - 16,LCD.BLACK)
    LCD.text("/",x-9,y - 11,LCD.BLACK)
#num 2
def two(x, y):
    Centre(x, y)
    BottomL(x, y)
    Bottom(x, y)
    TopR(x, y)
    Top(x, y)
#num 3
def three(x, y):
    Centre(x, y)
    Top(x, y)
    Bottom(x, y)
    FullR(x, y)
#num 4
def four(x, y):
    Centre(x, y)
    TopL(x, y)
    FullR(x, y)
#num 5
def five(x, y):
    Centre(x, y)
    TopL(x, y)
    Top(x, y)
    BottomR(x, y)
    Bottom(x, y)
#num 6
def six(x, y):
    Centre(x, y)
    Bottom(x, y)
    BottomR(x, y)
    FullL(x, y)
#num 7
def seven(x,y):
    FullR(x, y)
    Top(x, y)
#num 8
def eight(x,y):
    FullR(x, y)
    FullL(x, y)
    Top(x, y)
    Centre(x, y)
    Bottom(x, y)
#num 9
def nine(x, y):
    Top(x, y)
    Centre(x, y)
    TopL(x, y)
    FullR(x, y)
#num 0
def zero(x, y):
    FullR(x, y)
    FullL(x, y)
    Bottom(x, y)
    Top(x, y)

#Main body
LCD = LCD_3inch5()
LCD.bl_ctrl(100)

#top row
LCD.fill(LCD.WHITE)
#all numbers
one(20, 110)
two(60, 110)
three(100, 110)
four(140, 110)
five(180, 110)
six(220, 110)
seven(260, 110)
eight(300, 110)
nine(340, 110)
zero(380, 110)

LCD.show_up()
#bottom row
LCD.fill(LCD.BLACK)
LCD.show_down()
time.sleep(0.1)