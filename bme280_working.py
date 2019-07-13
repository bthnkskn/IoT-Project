import bme280
import time 
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import urllib
import urllib.request
import json
import numpy as np

ldr_pin = 4
LDRReading = 0
temp_val = 0
number_of_results = 1
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
pwm = GPIO.PWM(17,100) 
pwm.start(0)

client = mqtt.Client()
client.connect("mqtt.thingspeak.com", 1883, 60)

conn_url = 'https://api.thingspeak.com/channels/'
channelId = "763754"
writeapiKey = 'AM8ODVQTXJF9TDTX'

field1 = []

def RCtime (ldr_pin):
    reading = 0
    GPIO.setup(ldr_pin, GPIO.OUT)
    GPIO.output(ldr_pin, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(ldr_pin, GPIO.IN)
    
    while (GPIO.input(ldr_pin) == GPIO.LOW):
        reading += 1
    return reading
def my_map(x, in_min, in_max, out_min, out_max):
    mapped_value = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return mapped_value

try:
    while True:
        temperature,pressure,humidity = bme280.readBME280All()
        check_ldrread = RCtime(4)
        if(0<check_ldrread<5000):
            LDRReading = check_ldrread
        if(abs(LDRReading - temp_val)<200):
            LDRReading = temp_val
        temp_val = LDRReading
        print ("Light Intensity : ",LDRReading)
        print ("Temperature : ", temperature, "C")
        print ("Pressure : ", pressure, "hPa")
        print ("Humidity : ", humidity, "%")
        pwm.ChangeDutyCycle(my_map(LDRReading, 0, 5000, 0, 100)) 
        publish_path = "channels/" + channelId + "/publish/" + writeapiKey
        publish_data = "field1=" + str(LDRReading) + "&field2=" + str(temperature)+ "&field3=" + str(pressure)+ "&field4=" + str(humidity)
        client.publish(publish_path, publish_data)
    
        url = conn_url + str(channelId) + '/fields/' + str(1) + '.json?results=' + str(number_of_results)
        conn = urllib.request.urlopen(url)
        s = conn.read()
        y = json.loads(s.decode('utf-8'))
        for j in range(number_of_results):
            field1.append([y["feeds"][j]['field1']])
        conv_field1 = np.array(field1,dtype=float)
        mean_lux = sum(conv_field1)/len(conv_field1)
        time.sleep(1)
except KeyboardInterrupt:
    pass
pwm.stop()
GPIO.cleanup() 
