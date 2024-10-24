weatherscroller
================
An end-to-end solution to display weather conditions as scrolling text on an Arduin-driven 8x8 LED matrix. Consists of an Arduino program to receive text and a Python server that runs on a connected computer and sends data through serial.

## Arduino Setup ##
This is meant for an 8x8 LED matrix with PNP transistors going to anodes (rows) and current-sinking cathodes (columns). Pin numbers are found in the .ino file and are customizable.

## Using the application ##
Compile the .ino file and upload it to the Arduino.
Run the Python script with the Arduino connected. Make sure Python has permissions to access the serial bus.
