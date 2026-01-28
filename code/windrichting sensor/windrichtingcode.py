import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

#Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
ads.gain = 1
ads.data_rate = 128

#Create single-ended input on channel 0
chan = AnalogIn(ads,  0)

#Known resistor value in ohms
resistor= 200.0

try:
    while True:
        voltage = chan.voltage
        #Calculate current in milliamps (mA)
        current_mA = (voltage / resistor) * 1000.0

        if current_mA <7.50:
            richting ="noord"
        elif 7.50 <= current_mA <11.06:
            richting ="oost"
        elif 11.06 <= current_mA <14.62:
            richting ="zuid"
        elif 14.62 <= current_mA <20.0:
            richting ="west"

        print(
            f"Richting: {richting} | "
            f"Current: {current_mA:6.2f} mA",
            end="\r"
        )

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nStopped.")