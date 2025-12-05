#!/usr/bin/env python3
import serial
import time
import sys
import glob

BAUDRATE = 115200
# Pas aan als je Arduino op een andere seriële device verschijnt:
# vaak /dev/ttyACM0 (Arduino UNO over USB) of /dev/ttyUSB0
# Je kunt automatisch zoeken op /dev/ttyACM* en /dev/ttyUSB*
def find_arduino_port():
    ports = glob.glob('/dev/ttyACM*') + glob.glob('/dev/ttyUSB*')
    if not ports:
        raise FileNotFoundError("Geen Arduino-seriële poort gevonden (controleer USB-kabel / verbinding).")
    return ports[0]

def open_serial(port):
    return serial.Serial(port, BAUDRATE, timeout=1)

def parse_line(line):
    # verwacht vorm: timestamp_ms,adc_value,voltage,windSpeed
    parts = line.strip().split(",")
    if len(parts) < 4:
        raise ValueError("Onverwachte seriële regel: " + line)
    t = int(parts[0])
    adc = float(parts[1])
    voltage = float(parts[2])
    wind = float(parts[3])
    return t, adc, voltage, wind

def main():
    try:
        port = find_arduino_port()
        print("Open serial op:", port)
        ser = open_serial(port)
    except Exception as e:
        print("Fout bij openen serial:", e)
        sys.exit(1)

    try:
        # optioneel: logfile
        with open("wind_log.csv", "a") as logfile:
            # schrijf header als nieuw bestand
            if logfile.tell() == 0:
                logfile.write("timestamp_ms,adc,voltage,wind_mps,received_time\n")

            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if not line:
                    continue
                try:
                    t, adc, voltage, wind = parse_line(line)
                    # laat huidige tijd zien (menselijk leesbaar)
                    now = time.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{now}] Windsnelheid: {wind:.2f} m/s (spanning: {voltage:.3f} V, adc: {adc:.1f})")
                    logfile.write(f"{t},{adc:.2f},{voltage:.3f},{wind:.3f},{now}\n")
                    logfile.flush()
                except Exception as pe:
                    # als parsing faalt, print de ruwe regel voor debug
                    print("Parsing error:", pe, "| raw:", line)

    except KeyboardInterrupt:
        print("Gestopt door gebruiker.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()