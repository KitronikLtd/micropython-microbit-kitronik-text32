# microbit-module: KitronikText32@1.0.0
# Copyright (c) Kitronik Ltd 2022. 
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.from microbit import *
from microbit import spi

class KitronikText32:
    #defines of commands and
    initalised = False
    FUNCTION_SET1_CMD = 0x38
    FUNCTION_SET2_CMD = 0x3C
    DISPLAY_ON = 0x0C
    CLEAR_DISPLAY = 0x01
    LCD_LINE1 = 0x80
    LCD_LINE2 = 0xC0	
    LCD_LINE_LENGTH = 16
    BLANK_SPACE = 0x20 		

    def init(self):	
     #set buf with setup commands, turn on display, clear display and make ready for commands
     buf = bytearray([self.FUNCTION_SET1_CMD, self.DISPLAY_ON, self.CLEAR_DISPLAY, 0x06])
     #set the spi pins and frequency
     pin14.write_digital(0)
     spi.init(baudrate=230000, bits=8, mode=0, sclk=pin13, mosi=pin15, miso=pin12)
     pin14.write_digital(1)
     sleep(1000)
     #send setup to the LCD
     spi.write(buf)
     print('startup')
     self.initalised = True

    def clearScreen(self):
     if self.initalised is False:
        self.init(self)
     #send a blank string to the display
     self.displayStringOnLine(self, self.LCD_LINE1, '')
     self.displayStringOnLine(self, self.LCD_LINE2, '')

    def displayStringOnLine(self, lcdLineAddr, text):  # display string on a selected line of the LCD
     textLoop = 0
     lengthOfText = len(text)
     #if the text is less than 16 charectors, fill the rest with white spaces
     if lengthOfText < 16:
        lcdLengthToAdd = 16 - lengthOfText
        for textLoop in range (0, lcdLengthToAdd):
         text = text + ' '
        textLoop = 0
     #Send command byte and set which line of the LCD is being written to
     buf = bytearray([self.FUNCTION_SET1_CMD, lcdLineAddr])
     spi.write(buf)
     #Send command byte and set how many bytes are being sent
     buf = bytearray([self.FUNCTION_SET2_CMD, 0x8F])
     spi.write(buf)
     #send all string letters into byte array as int to send all together
     buf = bytearray([ord(text[0]),ord(text[1]),ord(text[2]),ord(text[3]),ord(text[4]),ord(text[5]),ord(text[6]),ord(text[7]),ord(text[8]),ord(text[9]),ord(text[10]),ord(text[11]),ord(text[12]),ord(text[13]),ord(text[14]),ord(text[15])])
     #print(buf)
     spi.write(buf)
      

    def showString(self, text):
     if self.initalised is False:
        self.init(self)
     textLoop = 0
     numberOfStrings = 0
     singleWords = text.split()
     numberOfWords = len(singleWords)
     lcdString = ''
     displayStrings = []
     currentScreenLineLength = 0
     for textLoop in range (0, (numberOfWords+1)):
        #check if at the last word
        if textLoop == numberOfWords:
         #save string to list of strings and add to number of strings
         displayStrings.append(lcdString)
         numberOfStrings = numberOfStrings + 1
         lcdString = ''
        else:
         #get the next word and length of the next word
         nextWord = singleWords[textLoop]
         nextWordLength = len(nextWord)
         if (currentScreenLineLength + nextWordLength) <= 16:  # check the current string length plus the next word legnth will fit on the LCD line
          #add new word on to lcd string being built and update its length
          lcdString = lcdString + singleWords[textLoop] + ' '
          currentScreenLineLength = len(lcdString)
         else:
          #save string to list of strings, add to number of strings, make lcdstring start with the new word
          displayStrings.append(lcdString)
          numberOfStrings = numberOfStrings + 1
          lcdString = singleWords[textLoop] + ' '
          screenLine = len(lcdString)
          currentScreenLineLength = 0

     screenLine = 0
     textLoop = 0
     # if updating single line, show current string on line and next line
     #self.clearScreen(self)
     if numberOfStrings <= 2:
        self.displayStringOnLine(self, self.LCD_LINE1, displayStrings[0])
        if numberOfStrings == 1:
         self.displayStringOnLine(self, self.LCD_LINE2, '')
        else:
         self.displayStringOnLine(self, self.LCD_LINE2, displayStrings[1])
     else:
        #loop around will all of the strings have been displayed
        for textLoop in range(numberOfStrings - 1):
         self.displayStringOnLine(self, self.LCD_LINE1, displayStrings[textLoop])
         self.displayStringOnLine(self, self.LCD_LINE2, displayStrings[textLoop + 1])
         sleep(2000)
         
text32 = KitronikText32

while True:
    if button_a.is_pressed():
     sleep(500)
     text32.showString(text32, 'Hello World! :) I am the :VIEW Text32')
    if button_b.is_pressed():
     sleep(500)
     text32.clearScreen(text32)
