from serial import Serial
from serial.tools import list_ports
from time import sleep
import geocoder
import requests

# prompt user to select serial port
print("Select Serial Port:")
ports = list_ports.comports()
for i in range(len(ports)):
    print(i, ":", ports[i].name)

selected = ports[int(input("Type port and press ENTER to continue: "))]
baud = int((x:=input("Type baudrate (or press ENTER for 115200): "), "115200" if x=="" else x)[1])

print("Starting connection to", selected.name,"with baud rate",baud)

arduino = Serial(selected.device) # dummy connection to receive all the watchdog gibberish (unplug + replug) and properly reset the arduino
with arduino: # the reset part is actually optional but the sleep is nice to have either way.
  arduino.setDTR(False)
  sleep(1)
  arduino.flushInput()
  arduino.setDTR(True)

# reopen the serial, but this time with proper baudrate. This is the correct and working connection.
arduino = Serial(selected.device,baudrate=baud)

with arduino:
    # wait until arduino is connected and data is recieved
    while not arduino.read_all():
       pass
    sleep(0.5)
    print("Arduino connected.")

    # acknowledge to arduino that we are connected
    arduino.write(str.encode("Connected\n"))

    while(True):
        x = input("Enter Location (press ENTER for current location, or q to quit): ")
        if x == "q":
           break
        unp = str(geocoder.ip('me').latlng)[1:-1] if x=="" else x
        print("Making request to weather API from", unp)

        query = {"key":"035dc28364d5460eb5d223931232505", "q":unp, "aqi":"no"}
        response = requests.get("http://api.weatherapi.com/v1/current.json", query).json()

        print("Location:", response["location"]["name"], ",", response["location"]["region"], ",", response["location"]["country"])
        print("Temperature:", response["current"]["temp_f"],"deg F")
        print("Conditions:", response["current"]["condition"]["text"])
        arduino.write(str.encode(response["current"]["condition"]["text"]+", "+str(response["current"]["temp_f"])+"F\n"))

        sleep(0.1)
    
    # clear the display before quitting
    arduino.write(str.encode("\n"))
    

