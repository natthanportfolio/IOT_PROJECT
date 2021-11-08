import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import socket
import Adafruit_ADS1x15

mode ="OF" #default mode
def on_connect(self, client, userdata, rc):
        print("MQTT Connected.")

def on_message(client, userdata, message):
        global mode
        a=str(message.payload)
        b=a[2:4]
        print("topic",str(message.topic),"received message = ",b)
        if message.topic == "mode":
                if b == "OF":
                        print("mode = manual")
                        mode="OF"
                        GPIO.output(22, 0)
                        GPIO.output(29, 0)
                        GPIO.output(31, 0)
                        GPIO.output(33, 0)
                        GPIO.output(35, 0)
                        GPIO.output(36, 0)
                if b == "ON":
                        print("mode = auto")
                        mode = "ON"
        if mode == "OF":
                if message.topic == "valveM1":
                        if b == "ON":
                                
                                GPIO.output(22,1)
                        elif b == "OF":
                                GPIO.output(22, 0)
                                
                if message.topic == "valveM2":
                        if b == "ON":
                                GPIO.output(29, 1)
                                
                        elif b == "OF":
                                GPIO.output(29, 0)
                                
                if message.topic == "valveM3":
                        if b == "ON":
                                GPIO.output(31, 1)
                                
                        elif b == "OF":
                                GPIO.output(31, 0)
                                
                if message.topic == "valveM4":
                        if b == "ON":
                                GPIO.output(33, 1)
                                
                        elif b == "OF":
                                GPIO.output(33, 0)
                                
                if message.topic == "valveM5":
                        if b == "ON":
                                GPIO.output(35, 1)
                                
                        elif b == "OF":
                                GPIO.output(35, 0)
                                
                if message.topic == "motor":
                        if b == "ON":
                                GPIO.output(36, 1)
                                
                        elif b == "OF":
                                GPIO.output(36, 0)
                                
GPIO.setwarnings(False)
GPIO.setmode (GPIO.BOARD)

GPIO.setup(37,GPIO.IN,pull_up_down=GPIO.PUD_UP) # switch
GPIO.setup(22,GPIO.OUT)
GPIO.setup(29,GPIO.OUT)
GPIO.setup(31,GPIO.OUT)
GPIO.setup(33,GPIO.OUT)
GPIO.setup(35,GPIO.OUT)
GPIO.setup(36,GPIO.OUT)

client = mqtt.Client()
client.username_pw_set(username="mvmmwqiq",password="i9wpB79zENJg")
client.connect("tailor.cloudmqtt.com",12106,60)
client.subscribe([("valveM1",0),("valveM2",0),("valveM3",0),("valveM4",0), ("valveM5",0),("motor",0),("mode",0),("volt0",0),("volt1",0)])
client.on_connect=on_connect
client.on_message=on_message
client.loop_start()
adc= Adafruit_ADS1x15.ADS1115()
GAIN=1
while True:
        values_ch0 = adc.read_adc(0, gain=GAIN)
        Volt0 = values_ch0 * 0.000125
        values_ch1 = adc.read_adc(1, gain=GAIN)
        Volt1 = values_ch1 * 0.000125
        print ( "volt0 =" ,Volt0)
        print ( "volt1 =" ,Volt1)
        if(Volt0<2):
                client.publish("volt0",str(Volt0)+" V")
        if(Volt1>0):
                client.publish("volt1",str(Volt1)+" V")
        time.sleep(2)
        state = GPIO.input(37)
        if(state == False):
                client.publish("mode","ON")
        if mode == "ON" or state == False:
                GPIO.output(22, 1)
                GPIO.output(29, 1)
                GPIO.output(31, 1)
                GPIO.output(33, 1)
                GPIO.output(35, 1)
                GPIO.output(36, 1)
                time.sleep(1)
                GPIO.output(22, 0)
                GPIO.output(29, 0)
                GPIO.output(31, 0)
                GPIO.output(33, 0)
                GPIO.output(35, 0)
                GPIO.output(36, 0)

        time.sleep(2)
