# micropython-microbit-kitronik-text32
Example MicroPython example code for the Kitronik RTC ( www.kitronik.co.uk/5650 )

## Operation

This package contains a function to display a string. If the string is more than 32 charectors the string will scroll on the display:
```blocks
text32.showString(text32, 'Hello World! :) I am the :VIEW Text32')
```

This package contains a function to clear the display
```blocks
text32.clearScreen(text32)
```

## License

MIT

## Supported Targets

BBC micro:bit
