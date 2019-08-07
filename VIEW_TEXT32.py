from microbit import *
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
     spi.init(baudrate=250000, bits=8, mode=0, sclk=pin13, mosi=pin15, miso=pin14)
     sleep(1000)
     #send setup to the LCD
     spi.write(buf)
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
     #send the display bytes to the LCD
     for textLoop in range (16):
      asciiNumber = text[textLoop]
      buf = bytearray([ord(asciiNumber)])
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

     screenLine = 0
     textLoop = 0
     # if updating single line, show current string on line and next line
     self.clearScreen(self)
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

while True:
    text32 = KitronikText32
    if button_a.is_pressed():
     text32.showString(text32, 'Hello World! :) I am the :VIEW Text32')
    if button_b.is_pressed():
     text32.clearScreen(text32)