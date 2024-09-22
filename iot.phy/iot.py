import urllib.request
import threading
import Adafruit_DHT
import RPi.GPIO as GPIO
from rpi_lcd import LCD

def senddata():
    threading.Timer(5, senddata).start()
    global buz, text1, text2, temp, hum
    buz = 0
    text1 = ''
    text2 = ''

    url = "https://api.thingspeak.com/update?api_key="
    API_key = "BXTQ21TYIIA1JONX"
    dht = Adafruit_DHT.DHT11
    hum1, temp1 = Adafruit_DHT.read(dht, 22)

    if temp1 is not None:
        temp = temp1
    if hum1 is not None:
        hum = hum1

    def collision():
        value = GPIO.input(25)
        if value == 0:
            print("Collision occured")
        return value

    def gas():
        value = GPIO.input(18)
        if value == 0:
            global buz, text1, text2
            buz = 1
            text1 = "Toxic gas"
            text2 = "Detected"
            print("Toxic gas detected")
        return value

    def ldr():
        value = GPIO.input(23)
        if value:
            print("No light")
        return value

    def ir():

        value = GPIO.input(24)
        if value == 1:
            global buz, text1
            buz = 1
            text1 = "Wear Helmet"
            print("Helmet removed")
        return value

    def buzzer():
        global text1, text2, buz
        lcd = LCD()
        print(f"buz val = {buz}")
        if buz == 1:
            lcd.text(text1, 1)
            lcd.text(text2, 2)
            GPIO.output(17, True)
        else:
            GPIO.output(17, False)

    Collision = collision()
    Ir = ir()
    LDR = ldr()
    Gas = gas()
    buzzer()

    field_Value = f"&field1={temp}&field2={hum}&field3={Gas}&field4={Collision}&field5={Ir}&field6={LDR}"
    new_url = url + API_key + field_Value
    data = urllib.request.urlopen(new_url)


if _name_ == "_main_":
    buz = 0
    temp = hum = None
    text1 = ''
    text2 = ''
    # print("OUT side fun")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18, GPIO.IN)
    GPIO.setup(23, GPIO.IN)
    GPIO.setup(24, GPIO.IN)
    GPIO.setup(25, GPIO.IN)
    GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
    senddata()