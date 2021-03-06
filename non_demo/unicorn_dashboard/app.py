import time
from reporter import Reporter
import os
import unicornhat as UH

host = os.environ["REDIS_HOST"]

if(host== None):
    host = "localhost"

UH.clear()
UH.show()

r = Reporter(host, "6379")

def on(r,g,b):
    for x in range(0,4):
        for y in range(0,11):
            UH.set_pixel(x,y,r,g,b)

def on_sensor_data(channel, data):
    print(channel, data)
    motion = r.get_key(data+".motion")
    if(motion != None and float(motion) > 0):
        on(0,0,255)
        UH.show()
        return

    value = r.get_key(data+".temp")
    baseline = r.get_key(data+".temp.baseline")
    print(baseline,value)
    if(baseline != None and value != None):
        baseline = round(float(baseline), 2)
        value = round(float(value), 2)

        diff = abs(value - baseline)
        print(str(value) + " ~ " + str(baseline) + " = " + str(diff))

        if(diff < 1.5):
            on(0,255,0)
        else:
            on(255,0,0)

        UH.show()


r.set_on_sensor_data(on_sensor_data)
r.subscribe()

while True:
    print (r.find_members())
    time.sleep(5)
