import bme280
import time 
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

client = mqtt.Client()
client.connect("mqtt.thingspeak.com", 1883, 60)

ldr_pin = 4

channelId = "763754"
apiKey = 'AM8ODVQTXJF9TDTX'

#GPIO.setup(17,GPIO.IN)
#p = GPIO.PWM(17,1000) 
#p.start(0)

def RCtime (ldr_pin):
    reading = 0
    GPIO.setup(ldr_pin, GPIO.OUT)
    GPIO.output(ldr_pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(ldr_pin, GPIO.IN)
    
    while (GPIO.input(ldr_pin) == GPIO.LOW):
        reading += 1
    return reading
 
while True:
    temperature,pressure,humidity = bme280.readBME280All()
    check_ldrread = RCtime(4)
    if(0<check_ldrread<5000):
        LDRReading = check_ldrread
        
    print ("Light Intensity : ",LDRReading)
    print ("Temperature : ", temperature, "C")
    print ("Pressure : ", pressure, "hPa")
    print ("Humidity : ", humidity, "%")
#    p.ChangeDutyCycle(x) 
    publish_path = "channels/" + channelId + "/publish/" + apiKey
    publish_data = "field1=" + str(LDRReading) + "&field2=" + str(temperature)+ "&field3=" + str(pressure)+ "&field4=" + str(humidity)
    client.publish(publish_path, publish_data)
#    client.loop(1)
    time.sleep(1)

 
