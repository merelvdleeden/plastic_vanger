import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15 import ADS1015, AnalogIn, ads1x15

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
ads.gain = 1
ads.data_rate = 128

# Create single-ended input on channel 0
chan = AnalogIn(ads, 0)

maxOutputVoltage = 5
maxWindSpeed = 30
kalibratieFactor = 3.38

try:
    while True:
        voltage = chan.voltage

        windSpeedMS = (voltage / maxOutputVoltage) * maxWindSpeed * kalibratieFactor
        windSpeedKMH = windSpeedMS * 3.6
        
        if windSpeedMS <0.30:
            windkracht ="0"
        elif 0.3 <= windSpeedMS <1.5:
            windkracht ="1"
        elif 1.5 <= windSpeedMS <3.3:
            windkracht ="2"
        elif 3.3 <= windSpeedMS <5.4:
            windkracht ="3"
        elif 5.4 <= windSpeedMS <7.9:
            windkracht = "4"
        elif 7.9 <= windSpeedMS <10.7:
            windkracht = "5"
        elif 10.7 <= windSpeedMS < 13.8:
            windkracht = "6"
        elif 13.8 <= windSpeedMS <17.1:
            windkracht= "7"
        elif 17.1 <= windSpeedMS <20.7:
            windkracht="8"
        elif 20.7 <= windSpeedMS <24.4:
            windkracht ="9"
        elif 24.4 <= windSpeedMS <28.4:
            windkracht ="10"
        elif 28.4 <= windSpeedMS:
            windkracht = "11"

        print(
            f"Windkracht: {windkracht}  "
            f"Wind speed: {windSpeedMS:6.2f} m/s    "
            f"{windSpeedKMH:6.2f} km/h", end = "\r"
        )

       
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped")

